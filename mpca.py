class Pixel:
	def __init__(self, y, x, v):
		self.y = int(y)
		self.x = int(x)
		self.val = v
	def __str__(self):
		return ("{" if self.val else "(") + str(self.x) + ", " + str(self.y) + ("}" if self.val else ")")
	def __repr__(self):
		return self.__str__()
	def __eq__(self, other):
		return self.x  == other.x and self.y == other.y and self.val == other.val
	def getNeighbors(self):
		neighbors = []
		for y in (self.y - 1, self.y, self.y + 1):
			for x in (self.x - 1, self.x, self.x + 1):
				if y != self.y or x != self.x:
					neighbors.append(Pixel(y, x, False))
		return neighbors
	def getUpperNeighbors(self):
		all = self.getNeighbors()
		upper = []
		for n in all:
			if n.y >= self.y:
				upper.append(n)
		return upper
	def getLowerNeighbors(self):
		all = self.getNeighbors()
		lower = []
		for n in all:
			if n.y <= self.y:
				lower.append(n)
		return lower
	def getULNeighbors(self):
		all = self.getUpperNeighbors()
		UL = []
		for n in all:
			if n.x <= self.x:
				UL.append(n)
		return UL
	def getURNeighbors(self):
		all = self.getUpperNeighbors()
		UR = []
		for n in all:
			if n.x >= self.x:
				UR.append(n)
		return UR
	def getLLNeighbors(self):
		all = self.getLowerNeighbors()
		LL = []
		for n in all:
			if n.x <= self.x:
				LL.append(n)
		return LL
	def getLRNeighbors(self):
		all = self.getLowerNeighbors()
		LR = []
		for n in all:
			if n.x >= self.x:
				LR.append(n)
		return LR
	def findBest(self, neighbors, radius, tolerance):
		values = tuple(map(lambda p: (p.x * p.x) + (p.y * p.y), neighbors))
		maxIndex = values.index(min(values))
		neighbors[maxIndex].val = True
		rSquared = radius ** 2
		for i in range(len(neighbors)):
			if values[i] <= rSquared + tolerance and values[i] > values[maxIndex]:
				neighbors[maxIndex].val = False
				neighbors[i].val = True
				maxIndex = i
		#print(values[maxIndex], end = "\t")
		return neighbors[maxIndex]
	
class RasterCircle:
	def __init__(self, r, t = 0):
		self.radius = abs(int(r))
		self.tolerance = int(t)
		self.pixels = []
		self.generatePixels()
		self.setASCII()
	def __str__(self):
	#	return str(tuple([self.radius, self.pixels]))
		return "A raster-circle of radius " + str(self.radius) + "."
	def __repr__(self):
		return self.__str__()
	def setASCII(self, on = "[]", off = "  "):
		self.ASCII = ""
		for y in range(-self.radius, self.radius + 1):
			for x in range(-self.radius, self.radius + 1):
				if Pixel(y, x, True) in self.pixels:
					self.ASCII += on
				else:
					self.ASCII += off
			self.ASCII += "\n"
		print("ASCII Art representation set.")
	def setASCIIMinimal(self):
		self.setASCII("#", " ")
	def setASCIIInverted(self):
		self.setASCII("  ", "[]")
	def printASCII(self):
		print(self.ASCII)
	def writeOut(self, filename):
		file = open(filename, "w")
		file.write(self.ASCII)
		file.close()
		print("ASCII Art file written.")
	def generatePixels(self):
		p = Pixel(0, self.radius, True)
		while p.x > 0:
			self.pixels.append(p)
			p = p.findBest(p.getULNeighbors(), self.radius, self.tolerance)
		#	print(p)
		while p.y > 0:
			self.pixels.append(p)
			p = p.findBest(p.getLLNeighbors(), self.radius, self.tolerance)
		#	print(p)
		while p.x < 0:
			self.pixels.append(p)
			p = p.findBest(p.getLRNeighbors(), self.radius, self.tolerance)
		#	print(p)
		while p.y < 0:
			self.pixels.append(p)
			p = p.findBest(p.getURNeighbors(), self.radius, self.tolerance)
		#	print(p)
		print("Pixels generated for radius " + str(self.radius) + ".")

