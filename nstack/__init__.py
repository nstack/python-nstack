import six

modules = {}

class Module_(object):
    def __init__(self, name):
        modules[name] = self
        self.methods = {}

    def expose(self, name=None, func=None):
        def decorator(func):
            if name is None:
                name = func.__name__
            self.methods[name] = func
        if func is None:
            return decorator
        decorator(func)

class Registry(type):
    modules = {}
    def __init__(cls, name, bases, dict_):
        try:
            Module
        except NameError:
            pass
        else:
            print(dict_)
            Registry.modules[name] = cls

@six.add_metaclass(Registry)
class Module(object):
    pass
