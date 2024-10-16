import builtins

def my_import(name, *args, builtin_imp=__import__):
    print("Importing ", name)
    return builtin_imp(name, *args)

builtins.__import__ = my_imp