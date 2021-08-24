class classproperty:
    def __init__(self, func):
        self._func = func

    def __get__(self, instance, cls):
        return self._func(cls)
