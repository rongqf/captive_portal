# coding: utf-8

        
class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

class SingletonMate(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMate, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
if __name__ == '__main__':
    @Singleton
    class T:
        pass

    print(T(), T())
