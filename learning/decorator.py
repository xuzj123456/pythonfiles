# coding=utf-8


def func_name(func):
    def wrapper(*args, **kwargs):
        print('Running function:', func.__name__)
        result = func(*args, **kwargs)
        return result   # 这两行令原函数正常运行
    return wrapper


@func_name
def add_num(*args):
    return sum(args)


a = add_num(3, 6)
