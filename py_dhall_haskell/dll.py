from ctypes import CDLL, c_void_p, c_char_p, c_int, Structure, POINTER, byref

hs_expr_p = c_void_p

dhallffi = CDLL('libdhallffi.so')

for name, (argtypes, restype) in {
    'hs_init': ([c_void_p, c_void_p], None),
    'unlink': ([c_void_p], None),

    'exprFromText': ([c_char_p], hs_expr_p),
    'exprGetConstr': ([hs_expr_p], c_int),
    'exprGetData': ([hs_expr_p], c_void_p),
}.items():
    func = getattr(dhallffi, name)
    func.argtypes = argtypes
    func.restype = restype

dhallffi.hs_init(None, None)
