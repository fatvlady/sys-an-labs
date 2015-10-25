__author__ = 'vlad'

class a(object):
    def __init__(self):
        self.x = 5
        return

    def t(self,a):
        print(type(self))
        return a + 1

a = a()
print(a.t(5))