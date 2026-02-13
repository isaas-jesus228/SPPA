from PyQt6.QtCore import QPointF
from math import cos, sin, radians, sqrt

class Circle:
    def __init__(self):
        self.params = [0]
        self.ab_mode = False
    
    def set_a(self, val):
        self.params[0] = val

    def get_point(self, deg):
        r = self.params[0] * 10
        rad = radians(deg)

        if self.ab_mode:
            x = r * cos(deg)+1000
            y = 1000 - r * sin(deg)
            point = QPointF(x, y)
            return point
        else:
            x = r * cos(rad)+1000
            y = 1000 - r * sin(rad)
            point = QPointF(x, y)
            return point
        
class PolarRose:
    def __init__(self):
        self.params = [0, 0]
        self.ab_mode = False
    
    def set_a(self, val):
        self.params[0] = val

    def set_b(self, val):
        self.params[1] = val

    def get_point(self, deg):
        rad = radians(deg)
        r = 10 * (self.params[0] * sin(self.params[1]*rad))

        if self.ab_mode:
            x = r * cos(deg)+1000
            y = 1000 - r * sin(deg)
            point = QPointF(x, y)
            return point
        else:
            x = r * cos(rad)+1000
            y = 1000 - r * sin(rad)
            point = QPointF(x, y)
            return point
        
class SnailPascal:
    def __init__(self):
        self.params = [0, 0]
        self.ab_mode = False
    
    def set_a(self, val):
        self.params[0] = val

    def set_b(self, val):
        self.params[1] = val

    def get_point(self, deg):
        rad = radians(deg)
        r = 10 * ((2 * self.params[0] * cos(rad)) + self.params[1])

        if self.ab_mode:
            x = r * cos(deg)+1000
            y = 1000 - r * sin(deg)
            point = QPointF(x, y)
            return point
        else:
            x = r * cos(rad)+1000
            y = 1000 - r * sin(rad)
            point = QPointF(x, y)
            return point
        
class Dekart:
    def __init__(self):
        self.params = [0]
        self.ab_mode = False
        self.max_radius = 1500
    
    def set_a(self, val):
        self.params[0] = val

    def get_point(self, deg):
        a = self.params[0]
        rad = radians(deg)

        den = cos(rad)**3 + sin(rad)**3
        
        if den == 0:
            return None
        
        r = 10 * (3 * a * cos(rad) * sin(rad) / den)

        if abs(r) > self.max_radius:
            return None

        if self.ab_mode:
            x = r * cos(deg)+1000
            y = 1000 - r * sin(deg)
            point = QPointF(x, y)
            return point
        else:
            x = r * cos(rad)+1000
            y = 1000 - r * sin(rad)
            point = QPointF(x, y)
            return point
        
class Spiral:
    def __init__(self):
        self.params = [0, 0]
        self.ab_mode = False
    
    def set_a(self, val):
        self.params[0] = val

    def set_b(self, val):
        self.params[1] = val

    def get_point(self, deg):
        rad = radians(deg)
        b = self.params[0]
        a = self.params[1]

        r = 10*(a*rad + b)

        if self.ab_mode:
            x = r * cos(deg)+1000
            y = 1000 - r * sin(deg)
            point = QPointF(x, y)
            return point
        else:
            x = r * cos(rad)+1000
            y = 1000 - r * sin(rad)
            point = QPointF(x, y)
            return point
        
class Anyez:
    def __init__(self):
        self.params = [0, 0]
        self.ab_mode = False
    
    def set_a(self, val):
        self.params[0] = val

    def set_b(self, val):
        self.params[1] = val

    def get_point(self, x):
        a = self.params[0]
        b = self.params[1]

        den = b**2 + x**2

        if den == 0:
            return None

        y = 1000 - 10*a**3/den
        x = 10*x + 1000
        point = QPointF(x, y)
        return point
    
class PolarAstroid:
    def __init__(self):
        self.params = [0, 0]
        self.ab_mode = False
    
    def set_a(self, val):
        self.params[0] = val

    def set_b(self, val):
        self.params[1] = val

    def get_point(self, deg):
        a = self.params[0]
        b = self.params[1]

        rad = radians(deg)
        sq = a*cos(rad)**6 + b*sin(rad)**6

        if sq < 0:
            return None

        r = 10*sqrt(sq)

        if self.ab_mode:
            x = r * cos(deg)+1000
            y = 1000 - r * sin(deg)
            point = QPointF(x, y)
            return point
        
        else:
            x = r * cos(rad)+1000
            y = 1000 - r * sin(rad)
            point = QPointF(x, y)
            return point
        
class Astroid:
    def __init__(self):
        self.params = [0, 0]
        self.ab_mode = False
    
    def set_a(self, val):
        self.params[0] = val

    def set_b(self, val):
        self.params[1] = val

    def get_point(self, deg):
        a = self.params[0]
        b = self.params[1]

        rad = radians(deg)

        x = 10*a*cos(rad)**3+1000
        y = 1000 - 10*b*sin(rad)**3

        point = QPointF(x, y)
        return point
    
class Epicycloid:
    def __init__(self):
        self.params = [0, 0]
        self.ab_mode = False
    
    def set_a(self, val):
        self.params[0] = val

    def set_b(self, val):
        self.params[1] = val

    def get_point(self, deg):
        a = self.params[0]
        b = self.params[1]

        rad = radians(deg)

        if a == 0:
            return None
        
        first_mult = a + b
        sec_mult = (a+b)/a

        rad_mult = sec_mult*rad

        x = 10*(first_mult*cos(rad) - a*cos(rad_mult))+1000
        y = 1000 - 10*(first_mult*sin(rad) - a*sin(rad_mult))

        point = QPointF(x, y)
        return point
    
class Hypocycloid:
    def __init__(self):
        self.params = [0, 0]
        self.ab_mode = False
    
    def set_a(self, val):
        self.params[0] = val

    def set_b(self, val):
        self.params[1] = val

    def get_point(self, deg):
        a = self.params[0]
        b = self.params[1]

        rad = radians(deg)

        if a == 0:
            return None
        
        first_mult = b-a
        sec_mult = (b-a)/a

        rad_mult = sec_mult*rad

        x = 10*(first_mult*cos(rad) + a*cos(rad_mult))+1000
        y = 1000 - 10*(first_mult*sin(rad) - a*sin(rad_mult))

        point = QPointF(x, y)
        return point