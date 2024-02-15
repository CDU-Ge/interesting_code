import dis
import types


def default_literal_variables(func):
    def wrapper(*args, **kwargs):
        # dis.dis(func)
        local_vars = {}
        bytecode = dis.Bytecode(func)
        for instruction in bytecode:
            if instruction.opname == 'LOAD_GLOBAL':
                var_name = instruction.argval
                if var_name not in func.__globals__.keys() and var_name not in getattr(types, '__builtins__'):
                    local_vars[var_name] = var_name
        local_vars.update(func.__globals__)
        return exec(func.__code__, local_vars)
    return wrapper


def _test():
    print(u, v, w)


@default_literal_variables
def my_func():
    print(x, z, y, 15235)  # x is not defined
    _test()


if __name__ == '__main__':
    try:
        my_func()
    except NameError as e:
        print('---------------------------------------')
        print(e)
    print(globals().keys())
