"""Teste le datapack sur un serveur Minecraft 1.21.1 vanilla sans interface.

Prérequis (non committés, dans tools/.server/) :
  server.jar  le serveur officiel 1.21.1
  eula.txt    créé par l'utilisateur après avoir accepté la licence Minecraft

Usage :
  python tools/server_test.py --java <java.exe> --seed rlm-1
  python tools/server_test.py --java <java.exe> --seed rlm-1 --biome minecraft:the_void
  python tools/server_test.py --java <java.exe> --seed rlm-1 --existing-world
"""
import argparse
import json
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
import zipfile
from pathlib import Path

from build_jar import build_jar
from convert_spawn_base import RENAMED
from litematic import load_litematic, trim
from nbtio import read_nbt_file

REPO_ROOT = Path(__file__).resolve().parents[1]
SERVER_DIR = REPO_ROOT / "tools/.server"
BIOME_TAG = "data/rlm_spawn/tags/worldgen/biome/has_structure/spawn_lot.json"
STATE_RE = r"#state has (-?\d+) \[rlm_spawn\]|Can't get value of rlm_spawn for #state"


class Server:
    def __init__(self, java, run_dir: Path):
        self.java = java
        self.run_dir = run_dir
        self.lines = queue.Queue()
        self.proc = None
        self.log = open(run_dir / "console.log", "a", encoding="utf-8")

    def _pump(self):
        for line in self.proc.stdout:
            self.log.write(line)
            self.log.flush()
            self.lines.put(line.rstrip("\n"))
        self.lines.put(None)

    def start(self, timeout=900):
        self.proc = subprocess.Popen(
            [self.java, "-Xmx3G", "-jar", str(SERVER_DIR / "server.jar"), "nogui"],
            cwd=self.run_dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        threading.Thread(target=self._pump, daemon=True).start()
        self.wait_for(r"Done \(", timeout)

    def wait_for(self, pattern, timeout):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                line = self.lines.get(timeout=1)
            except queue.Empty:
                continue
            if line is None:
                raise RuntimeError("le serveur s'est arrêté (voir %s)" % (self.run_dir / "console.log"))
            m = re.search(pattern, line)
            if m:
                return m
        raise TimeoutError("pas de réponse « %s » en %d s" % (pattern, timeout))

    def command(self, cmd, pattern, timeout=120):
        while not self.lines.empty():
            if self.lines.get_nowait() is None:
                raise RuntimeError("le serveur s'est arrêté")
        self.proc.stdin.write(cmd + "\n")
        self.proc.stdin.flush()
        return self.wait_for(pattern, timeout)

    def state(self):
        m = self.command("scoreboard players get #state rlm_spawn", STATE_RE)
        return int(m.group(1)) if m.group(1) is not None else None

    def score(self, holder):
        m = self.command("scoreboard players get %s rlm_spawn" % holder,
                         r"%s has (-?\d+) \[rlm_spawn\]|Can't get value of rlm_spawn for %s" % (holder, holder))
        return int(m.group(1)) if m.group(1) is not None else None

    def storage(self):
        m = self.command("data get storage rlm_spawn:data", r"Storage rlm_spawn:data has the following contents: (.*)$")
        return parse_storage(m.group(1))

    def test(self, cmd):
        return self.command(cmd, r"Test (passed|failed)").group(1) == "passed"

    def forceloaded(self):
        m = self.command("execute in minecraft:overworld run forceload query",
                         r"(No force loaded chunks were found|force loaded chunks? (?:was|were) found)")
        return not m.group(1).startswith("No ")

    def gametime(self):
        return int(self.command("time query gametime", r"The time is (\d+)").group(1))

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.stdin.write("stop\n")
            self.proc.stdin.flush()
            self.proc.wait(timeout=180)
        self.log.close()


def parse_storage(text):
    out = {}
    for key in ("lot", "spawn"):
        m = re.search(r"\b%s: \{(.*?)\}" % key, text)
        if not m:
            continue
        fields = {}
        for k, v in re.findall(r'(\w+): ("[^"]*"|-?[\d.]+[dfbsL]?)', m.group(1)):
            fields[k] = v.strip('"') if v.startswith('"') else float(v.rstrip("dfbsL"))
        out[key] = fields
    return out


def remove_tree(path, attempts=10):
    """Windows verrouille parfois un fichier un instant (antivirus, indexation) : on réessaie."""
    for i in range(attempts):
        if not path.exists():
            return
        try:
            shutil.rmtree(path)
        except OSError:
            if i == attempts - 1:
                raise
            time.sleep(2)


def prepare_run(name, seed, with_pack, biome=None):
    run_dir = SERVER_DIR / name
    try:
        remove_tree(run_dir, attempts=3)
    except OSError:
        # Un fichier reste « en cours de suppression » tant qu'un autre programme le tient
        # ouvert : on prend un dossier neuf, l'ancien se libérera plus tard.
        run_dir = SERVER_DIR / ("%s-%d" % (name, int(time.time())))
    run_dir.mkdir(parents=True)
    shutil.copy(SERVER_DIR / "eula.txt", run_dir / "eula.txt")
    (run_dir / "server.properties").write_text("\n".join([
        "level-seed=%s" % seed, "level-name=world", "online-mode=false", "server-port=25599",
        "view-distance=4", "simulation-distance=4", "spawn-protection=0", "max-players=1", ""]),
        encoding="utf-8")
    if with_pack:
        install_pack(run_dir, biome)
    return run_dir


def install_pack(run_dir, biome=None):
    packs = run_dir / "world/datapacks"
    packs.mkdir(parents=True, exist_ok=True)
    jar = build_jar(REPO_ROOT, run_dir / "build")
    target = packs / "rlm.zip"
    if biome is None:
        shutil.copy(jar, target)
        return
    with zipfile.ZipFile(jar) as src, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == BIOME_TAG:
                data = json.dumps({"values": [biome]}).encode("utf-8")
            dst.writestr(item, data)


def wait_final_state(server, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        s = server.state()
        if s not in (1, 2):
            return s
        time.sleep(5)
    return server.state()


class Report:
    def __init__(self):
        self.ok = True

    def check(self, label, cond, detail=""):
        self.ok &= bool(cond)
        print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  (%s)" % detail) if detail else ""), flush=True)


def datapack_errors(run_dir):
    log = (run_dir / "logs/latest.log").read_text(encoding="utf-8", errors="replace")
    return [line for line in log.splitlines()
            if "/ERROR]" in line and ("rlm_spawn" in line or "Failed to load" in line)]


def spawn_level_dat(run_dir):
    data = read_nbt_file(run_dir / "world/level.dat")["Data"]
    return int(data["SpawnX"]), int(data["SpawnY"]), int(data["SpawnZ"])


def expected_from_config():
    """Bloc attendu sous le spawn et décalage spawn -> bloc de surface, d'après les réglages."""
    cfg = json.loads((REPO_ROOT / "tools/spawn_base.json").read_text(encoding="utf-8"))
    build = trim(load_litematic(REPO_ROOT / cfg["litematic"]))
    x, y, z = cfg["spawn"]
    floor = build.block_name(x, y - 1, z)
    return RENAMED.get(floor, floor), y - cfg["ground_layer"], cfg["ground_layer"]


def run_normal(java, seed, report):
    floor, spawn_rise, ground_layer = expected_from_config()
    run_dir = prepare_run("run-%s" % seed, seed, True)
    server = Server(java, run_dir)
    try:
        server.start()
        errors = datapack_errors(run_dir)
        report.check("datapack chargé sans erreur", not errors, "; ".join(errors[:3]))
        state = wait_final_state(server)
        report.check("état final = 3", state == 3, "état %s" % state)
        report.check("échantillon du build en place", server.score("#verified") == 1)
        st = server.storage()
        lot, spawn = st.get("lot", {}), st.get("spawn", {})
        report.check("stockage lot et spawn présents", lot and spawn, str(st))
        if not (lot and spawn):
            return
        pos = "%s %s %s" % (spawn["x"], spawn["y"], spawn["z"])
        print("      rotation %s, repère %d %d, spawn %s" % (lot.get("rotation"), lot["x"], lot["z"], pos))
        report.check("spawn dans le biome",
                     server.test("execute in minecraft:overworld positioned %s if biome ~ ~ ~ "
                                 "#rlm_spawn:has_structure/spawn_lot" % pos))
        report.check("plancher sous le spawn (%s)" % floor,
                     server.test("execute in minecraft:overworld positioned %s if block ~ ~-1 ~ %s" % (pos, floor)))
        if ground_layer < 0:
            report.check("surface (eau ou sol) intacte sous le build",
                         server.test("execute in minecraft:overworld positioned %s unless block ~ ~-%d ~ #minecraft:air"
                                     % (pos, spawn_rise)))
        m = server.command("locate structure rlm_spawn:spawn_lot",
                           r"is at \[(-?\d+), [^,]+, (-?\d+)\]|Could not find")
        report.check("/locate trouve le repère", m.group(1) is not None
                     and (int(m.group(1)), int(m.group(2))) == (int(lot["x"]), int(lot["z"])), m.group(0))
        report.check("aucun chunk chargé de force", not server.forceloaded())
    finally:
        server.stop()
    server = Server(java, run_dir)
    try:
        server.start()
        report.check("redémarrage : état 3 conservé", server.state() == 3)
        report.check("redémarrage : spawn inchangé", server.storage().get("spawn") == spawn)
    finally:
        server.stop()


def run_void(java, seed, biome, report):
    run_dir = prepare_run("run-%s-biome" % seed, seed, True, biome)
    server = Server(java, run_dir)
    try:
        server.start()
        state = wait_final_state(server)
        report.check("biome introuvable : état -2", state == -2, "état %s" % state)
        report.check("biome introuvable : aucun chunk chargé de force", not server.forceloaded())
    finally:
        server.stop()


def run_existing(java, seed, report):
    run_dir = prepare_run("run-%s-existing" % seed, seed, False)
    server = Server(java, run_dir)
    try:
        server.start()
        while server.gametime() < 700:
            time.sleep(5)
    finally:
        server.stop()
    before = spawn_level_dat(run_dir)
    install_pack(run_dir)
    server = Server(java, run_dir)
    try:
        server.start()
        report.check("monde existant : état -1", server.state() == -1)
        report.check("monde existant : aucun chunk chargé de force", not server.forceloaded())
    finally:
        server.stop()
    after = spawn_level_dat(run_dir)
    report.check("monde existant : spawn inchangé", before == after, "%s -> %s" % (before, after))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--java", required=True)
    ap.add_argument("--seed", required=True)
    ap.add_argument("--biome")
    ap.add_argument("--existing-world", action="store_true")
    args = ap.parse_args()
    if not (SERVER_DIR / "server.jar").is_file():
        print("Manque %s" % (SERVER_DIR / "server.jar"), file=sys.stderr)
        return 2
    eula = SERVER_DIR / "eula.txt"
    if not eula.is_file() or "eula=true" not in eula.read_text(encoding="utf-8"):
        print("Manque %s avec eula=true (à créer par l'utilisateur)" % eula, file=sys.stderr)
        return 2
    report = Report()
    if args.existing_world:
        run_existing(args.java, args.seed, report)
    elif args.biome:
        run_void(args.java, args.seed, args.biome, report)
    else:
        run_normal(args.java, args.seed, report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
