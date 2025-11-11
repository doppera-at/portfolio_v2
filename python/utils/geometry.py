import math

class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def add(self, x=0, y=0):
		self.x += x
		self.y += y
	def add_tuple(self, pos=(0, 0)):
		self.add(pos[0], pos[1])
	def add_vector(self, vector):
		if vector == None: return None
		self.add_tuple(vector.tuple())

	def subtract(self, x=0, y=0):
		self.x -= x
		self.y -= y
	def subtract_tuple(self, pos=(0, 0)):
		self.subtract(pos[0], pos[1])
	def subtract_vector(self, vector):
		if vector == None: return None
		self.subtract_tuple(vector.tuple())

	def multiply(self, num):
		self.x *= num
		self.y *= num
	def divide(self, num):
		self.x /= num
		self.y /= num

	def distance(self, x=0, y=0):
		return math.sqrt((x - self.x)**2 + (y - self.y)**2)
	def distance_tuple(self, pos=(0, 0)):
		return self.distance(pos[0], pos[1])
	def distance_vector(self, vector):
		if vector == None: return None
		vector_tuple = vector.tuple()
		return self.distance_tuple(vector_tuple)

	def point_at(self, vector):
		if vector == None: return None
		point = vector.copy()
		point.subtract(self.x, self.y)
		return Vector(point.x, point.y)

	def tuple(self):
		return (self.x, self.y)
	def tuple_int(self):
		return (int(self.x), int(self.y))

	def copy(self):
		return Vector(self.x, self.y)

	def normalize(self, min_val, max_val):
		self.x = (x-min_val)/(max_val-min_val)
		self.y = (y-min_val)/(max_val-min_val)

	def __str__(self):
		return "Vector {x=" + str(self.x) + ", y=" + str(self.y) + "}"

class Line:
	def __init__(self, vector1, vector2, color=(255, 255, 255)):
		self.vector1 = vector1
		self.vector2 = vector2
		self.color = color
	def p1(self):
		return self.vector1
	def p2(self):
		return self.vector2
	def __str__(self):
		return "Line {p1=" + str(self.vector1) + ", p2=" + str(self.	vector2) + "}"

class Circle:
	def __init__(self, x=0, y=0, radius=0, color=(255, 255, 255), width=0):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.width = width
	def pos(self):
		return (self.x, self.y)
	def vector(self):
		return Vector(self.x, self.y)

	def __str__(self):
		return "Circle {x=" + str(self.x) + ", y=" + str(self.y) + ", radius=" + str(self.radius) + ", color=" + str(self.color) + ", width=" + str(self.width) + "}"

class Polygon:
	def __init__(self, points=[]):
		self.points = points

	def __str__(self):
		return "Polygon {" + str(self.points) + "}"