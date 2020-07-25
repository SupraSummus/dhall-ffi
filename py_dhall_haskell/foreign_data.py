from functools import cached_property

from .dll import dhallffi


def FieldForeign(i, cls):
    def f(self):
        raw = self._get_raw_foreign_field(i)
        print('pos', i, 'raw', raw)
        return cls.from_foreign(raw)
    return cached_property(f)


def FieldForeignDirect(i, constructor):
    def f(self):
        raw = self._get_raw_direct_foreign_field(i)
        return constructor(raw)
    return cached_property(f)


class ForeignData:
    _fields = ()

    @classmethod
    def from_foreign(cls, ptr):
        return cls(ptr)

    def __init__(self, ptr):
        self._ptr = ptr

    def __del__(self):
        dhallffi.unlink(self._ptr)

    """
    def as_plain(self):
        return {
            '_ptr': self._ptr,
        }
    """

    def __repr__(self):
        args = ', '.join(
            repr(getattr(self, field_name))
            for field_name in self._fields
        )
        return f'{self.__class__.__name__}({args})'


class Text(ForeignData):
    pass


class ByteString(ForeignData, bytes):
    pass


def FieldText(i):
    return FieldForeign(i, Text)


def FieldIntegral(i):
    return FieldForeignDirect(i, int)
