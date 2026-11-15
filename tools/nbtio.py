"""Lecture et écriture de fichiers NBT compressés (gzip), types conservés.

Un compound est un dict, une liste un list, une chaîne un str. Les autres types
NBT sont représentés par les classes ci-dessous pour être réécrits à l'identique.
"""
import gzip
import struct


class Byte(int): pass
class Short(int): pass
class Int(int): pass
class Long(int): pass
class Float(float): pass
class Double(float): pass
class ByteArray(list): pass
class IntArray(list): pass
class LongArray(list): pass  # entiers non signés 0..2^64-1


TAG_END, TAG_BYTE, TAG_SHORT, TAG_INT, TAG_LONG, TAG_FLOAT, TAG_DOUBLE = range(7)
TAG_BYTE_ARRAY, TAG_STRING, TAG_LIST, TAG_COMPOUND, TAG_INT_ARRAY, TAG_LONG_ARRAY = range(7, 13)

_SCALARS = {
    TAG_BYTE: (">b", Byte), TAG_SHORT: (">h", Short), TAG_INT: (">i", Int),
    TAG_LONG: (">q", Long), TAG_FLOAT: (">f", Float), TAG_DOUBLE: (">d", Double),
}
_TYPE_IDS = {Byte: TAG_BYTE, Short: TAG_SHORT, Int: TAG_INT, Long: TAG_LONG, Float: TAG_FLOAT,
             Double: TAG_DOUBLE, ByteArray: TAG_BYTE_ARRAY, str: TAG_STRING, list: TAG_LIST,
             dict: TAG_COMPOUND, IntArray: TAG_INT_ARRAY, LongArray: TAG_LONG_ARRAY}


class _Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def unpack(self, fmt):
        val = struct.unpack_from(fmt, self.data, self.pos)
        self.pos += struct.calcsize(fmt)
        return val[0]

    def string(self):
        n = self.unpack(">H")
        s = self.data[self.pos:self.pos + n].decode("utf-8")
        self.pos += n
        return s

    def payload(self, tag):
        if tag in _SCALARS:
            fmt, cls = _SCALARS[tag]
            return cls(self.unpack(fmt))
        if tag == TAG_STRING:
            return self.string()
        if tag == TAG_LIST:
            item = self.unpack(">b")
            n = self.unpack(">i")
            return [self.payload(item) for _ in range(n)]
        if tag == TAG_COMPOUND:
            out = {}
            while True:
                t = self.unpack(">b")
                if t == TAG_END:
                    return out
                name = self.string()
                out[name] = self.payload(t)
        if tag in (TAG_BYTE_ARRAY, TAG_INT_ARRAY, TAG_LONG_ARRAY):
            n = self.unpack(">i")
            fmt, cls = {TAG_BYTE_ARRAY: ("b", ByteArray), TAG_INT_ARRAY: ("i", IntArray),
                        TAG_LONG_ARRAY: ("Q", LongArray)}[tag]
            vals = struct.unpack_from(">%d%s" % (n, fmt), self.data, self.pos)
            self.pos += n * struct.calcsize(fmt)
            return cls(vals)
        raise ValueError("type NBT inconnu : %d" % tag)


def _type_id(value) -> int:
    try:
        return _TYPE_IDS[type(value)]
    except KeyError:
        raise TypeError("valeur sans type NBT explicite : %r (%s)" % (value, type(value).__name__))


def _write_string(out: bytearray, s: str):
    b = s.encode("utf-8")
    out += struct.pack(">H", len(b)) + b


def _write_payload(out: bytearray, value):
    tag = _type_id(value)
    if tag in _SCALARS:
        out += struct.pack(_SCALARS[tag][0], value)
    elif tag == TAG_STRING:
        _write_string(out, value)
    elif tag == TAG_LIST:
        item = _type_id(value[0]) if value else TAG_END
        if any(_type_id(v) != item for v in value):
            raise TypeError("liste NBT de types mélangés")
        out += struct.pack(">bi", item, len(value))
        for v in value:
            _write_payload(out, v)
    elif tag == TAG_COMPOUND:
        for name, v in value.items():
            out += struct.pack(">b", _type_id(v))
            _write_string(out, name)
            _write_payload(out, v)
        out += struct.pack(">b", TAG_END)
    else:
        fmt = {TAG_BYTE_ARRAY: "b", TAG_INT_ARRAY: "i", TAG_LONG_ARRAY: "Q"}[tag]
        out += struct.pack(">i%d%s" % (len(value), fmt), len(value), *value)


def read_nbt_file(path) -> dict:
    with gzip.open(path, "rb") as f:
        r = _Reader(f.read())
    tag = r.unpack(">b")
    if tag != TAG_COMPOUND:
        raise ValueError("la racine NBT n'est pas un compound")
    r.string()
    return r.payload(tag)


def write_nbt_file(path, root: dict) -> None:
    out = bytearray(struct.pack(">b", TAG_COMPOUND))
    _write_string(out, "")
    _write_payload(out, root)
    # mtime=0 et sans nom de fichier : même contenu => mêmes octets (diffs git propres).
    with open(path, "wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as f:
        f.write(bytes(out))
