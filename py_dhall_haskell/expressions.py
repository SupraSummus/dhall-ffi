from .foreign_data import ForeignData, FieldForeign, FieldText, FieldIntegral
from .dll import dhallffi


expr_classes = {}  # contructor id -> class


class Expr(ForeignData):
    @classmethod
    def from_foreign(cls, ptr):
        constr = dhallffi.exprGetConstr(ptr)
        return expr_classes[constr](ptr)

    def _get_raw_foreign_field(self, i):
        return dhallffi.exprGetData(self._ptr, i)

    def _get_raw_direct_foreign_field(self, i):
        return dhallffi.exprGetDirect(self._ptr, i)

    """
    def as_plain(self):
        return {
            name: getattr(self, name)
            for name in self._expr_fields
        }
    """


def FieldExpr(i):
    return FieldForeign(i, Expr)


class Var(ForeignData):
    name = FieldText(0)
    scope = FieldIntegral(1)

    def as_plain(self):
        return {
            'name': self.name,
            'scope': self.scope,
        }

    def _get_raw_direct_foreign_field(self, i):
        return dhallffi.varGetDirect(self._ptr, i)

    def _get_raw_foreign_field(self, i):
        return dhallffi.varGetData(self._ptr, i)


def FieldVar(i):
    return FieldForeign(i, Var)


for construtor_id, (name, fields) in enumerate([
    ('__invalid__', []),
    ('Const', []),
    ('Var', [('var', FieldVar)]),
    ('Lam', []),
    ('Pi', (
        ('name', FieldText),
        ('arg', FieldExpr),
        ('body', FieldExpr),
    )),
    ('App', []), # 5: app
    ('Let', []), # 6: let
    ('', []), # 7: Annot (Expr s a) (Expr s a)
    ('Bool', []),
    ('', []), # 9 BoolLit Bool
    ('', []), # 10 BoolAnd (Expr s a) (Expr s a)
    ('', []), # 11 BoolOr (Expr s a) (Expr s a)
    ('', []), # 12 BoolEQ (Expr s a) (Expr s a)
    ('', []), # 13 BoolNE (Expr s a) (Expr s a)
    ('', []), # 14 BoolIf (Expr s a) (Expr s a) (Expr s a)
    ('Natural', []),
    ('NaturalLit', [('value', FieldIntegral)]),
    ('NaturalFold', []),
    ('NaturalBuild', []),
    ('NaturalIsZero', []),
    ('NaturalEven', []),
    ('NaturalOdd', []),
    ('NaturalToInteger', []),
    ('NaturalShow', []),
    ('NaturalSubtract', []),
    ('NaturalPlus', [
        ('a', FieldExpr),
        ('b', FieldExpr),
    ]),
    ('', []), # 26 NaturalTimes (Expr s a) (Expr s a)
    ('Integer', []),
    ('IntegerLit', [('value', FieldIntegral)]),
    ('IntegerClamp', []),
    ('IntegerNegate', []),
    ('IntegerShow', []),
    ('IntegerToDouble', []),
    ('Double', []),
    ('', []), # 34 DoubleLit DhallDouble
    ('DoubleShow', []),
    ('Text', []),
    ('', []), # 37 TextLit (Chunks s a)
    ('', []), # 38 TextAppend (Expr s a) (Expr s a)
    ('', []), # 39 TextShow
    ('', []), # 40 List
    ('', []), # 41 ListLit (Maybe (Expr s a)) (Seq (Expr s a))
    ('', []), # 42 ListAppend (Expr s a) (Expr s a)
    ('', []), # 43 ListBuild
    ('', []), # 44 ListFold
    ('', []), # 45 ListLength
    ('', []), # 46 ListHead
    ('', []), # 47 ListLast
    ('', []), # 48 ListIndexed
    ('', []), # 49 ListReverse
    ('', []), # 50 Optional
    ('', []), # 51 Some (Expr s a)
    ('', []), # 52 None
    ('', []), # 53 OptionalFold
    ('', []), # 54 OptionalBuild
    ('', []), # 55 Record (Map Text (Expr s a))
    ('', []), # 56 RecordLit (Map Text (Expr s a))
    ('', []), # 57 Union (Map Text (Maybe (Expr s a)))
    ('', []), # 58 Combine (Maybe Text) (Expr s a) (Expr s a)
    ('', []), # 59 CombineTypes (Expr s a) (Expr s a)
    ('', []), # 60 Prefer (PreferAnnotation s a) (Expr s a) (Expr s a)
    ('', []), # 61 RecordCompletion (Expr s a) (Expr s a)
    ('', []), # 62 Merge (Expr s a) (Expr s a) (Maybe (Expr s a))
    ('', []), # 63 ToMap (Expr s a) (Maybe (Expr s a))
    ('', []), # 64 Field (Expr s a) Text
    ('', []), # 65 Project (Expr s a) (Either (Set Text) (Expr s a))
    ('', []), # 66 Assert (Expr s a)
    ('', []), # 67 Equivalent (Expr s a) (Expr s a)
    ('', []), # 68 With (Expr s a) (NonEmpty Text) (Expr s a)
    ('Note', [
        ('src', FieldText),
        ('expr', FieldExpr),
    ]),
    ('', []), # 70 ImportAlt (Expr s a) (Expr s a)
    ('', []), # 71 Embed a
]):
    if not name:
        continue

    class_name = 'Expr' + name

    field_dict = {
        field_name: field_type(i)
        for i, (field_name, field_type) in enumerate(fields)
    }
    field_dict['_fields'] = Expr._fields + tuple(field_dict.keys())

    cls = type(class_name, (Expr,), field_dict)
    globals()[class_name] = cls
    expr_classes[construtor_id] = cls
