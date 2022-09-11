
# inheritance_example.py

class Parent:
    def __init__(self, x, y, z, f):
        self._x = x
        self._y = y
        self._z = z
        self._f = f

    def __str__(self):
        return ('x: ' + str(self._x) + ', y: ' + str(self._y)
                                     + ', z: ' + str(self._z))

    def do_something(self):
        return self._f(self._x, self._y, self._z)

class Child1(Parent):
    def fun(a, b, c):    # ordinary function, NOT instance method
        return a + b + c
    
    def __init__(self, x, y, z):
        super().__init__(x, y, z, Child1.fun)

    def __str__(self):
        return 'parent: ' + super().__str__()

class Child2(Parent):
    def fun(a, b, c):    # ordinary function, NOT instance method
        return max([a, b, c])
    
    def __init__(self, x, y, z):
        super().__init__(x, y, z, Child2.fun)

    def __str__(self):
        return 'parent: ' + super().__str__()

    
# testing code

p1 = Child1(1, 2, 3)

print(p1.do_something())  # call Parent method

p2 = Child2(1, 2, 3)

print(p2.do_something())  # call Parent method




    
