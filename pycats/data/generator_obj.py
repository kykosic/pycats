"""
    Provide a concrete type for the python builtin `generator`.

    We need this to construct typeclass instances on generators,
    but the Python standard library does not provide it for direct import.
"""
_gen_obj = (_ for _ in range(0))
generator = type(_gen_obj)
