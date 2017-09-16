class ClassRegister(dict):
    def register_class(self, cls):
        return self.setdefault(cls.__name__, cls)


class ClassRegisterMeta(type):
    register = None

    def __new__(mcs, name, bases, namespace):
        new_class = super().__new__(mcs, name, bases, namespace)
        mcs.register.register_class(new_class)
        return new_class
