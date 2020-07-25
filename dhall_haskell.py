from py_dhall_haskell import dhallffi, Expr

expr = dhallffi.exprFromText(b"(a -> a@3 + 5)")
expr_v = Expr.from_foreign(expr)
print(expr_v)

del expr_v

# apparently safe to call
dhallffi.unlink(None)

print(dhallffi.exprFromText(b"}"))
