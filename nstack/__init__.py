import collections
import six
import threading

modules = {}

class LocalConfig(threading.local):
    def __init__(self):
        self.stack = collections.deque([{}])

    def push(self, config):
        self.stack.appendleft(config)

    def pop(self):
        self.stack.popleft()

    def peek(self):
        try:
            return self.stack[0]
        except LookupError:
            raise LookupError("Empty config")

    def __getitem__(self, name):
        return self.peek()[name]

    def get(self, name, default=None):
        return self.peek().get(name, default)

config = LocalConfig()

def with_config(conf, f=None):
    def decorator(f):
        def decorated(*a, **k):
            config.push(conf)
            try:
                return f(*a, **k)
            finally:
                config.pop()
        return decorated
    if f is not None:
        return decorator(f)
    return decorator

def use_config(config):
    config.push(config)

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
    def __init__(self):
        self.args = config
