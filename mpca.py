# Test for PIL
try:
	from PIL import Image
except:
	print("PIL is not installed. Do not use the -Image() methods on RasterCircles!")
# Pixel Class
class Pixel:
	def __init__(self, y, x, v):
		self.y = int(y)
		self.x = int(x)
		self.val = v
	def __str__(self):
		return ("{" if self.val else "(") + str(self.x) + ", " + str(self.y) + ("}" if self.val else ")")
	def __repr__(self):
		return self.__str__()
	# Below was for in operator when imaging a circle, unneeded for now
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
	# Given a list of neighbors, a circle radius, and a tolerance,
	# Return a neighboring Pixel that best fits a circle of the given radius
	# within range of the tolerance
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
		return neighbors[maxIndex]
# Rasterized Circle Class
class RasterCircle:
	def __init__(self, r, t = -1):
		self.radius = abs(int(r))
		if t == -1:
			self.tolerance = int(self.radius ** 0.5)
		else:
			self.tolerance = t
		self.pixels = []
		# LUT: LookUp Table
		# This makes imaging fast instead of
		# using the in operator in nested for-loops.
		# See generateValueArray() and getImage()
		self.LUT = [ \
			[False for a in range(2 * self.radius + 1)] \
			for b in range(2 * self.radius + 1) \
		]
		self.generatePixels()
	def __str__(self):
	#	return str(tuple([self.radius, self.pixels]))
		return "A raster-circle of radius " + str(self.radius) + "."
	def __repr__(self):
		return self.__str__()
	# Generate an array representative of the pixel values.
	# Can be converted to a 8-bit grayscale image
	def generateValueArray(self):
		if not hasattr(self, "valArr"):
			print("Generating image value array...")
			valArr = []
			for y in range(-self.radius, self.radius + 1):
				for x in range(-self.radius, self.radius + 1):
					if self.LUT[y][x]:
						valArr.append(0x00)
					else:
						valArr.append(0xFF)
			self.valArr = valArr
			print("Done!")
		return self.valArr
	# Use the PIL Image module to create an 8-bit grayscale image of the circle
	def getImage(self):
		return Image.frombytes( \
			"L", (self.radius * 2 + 1, self.radius * 2 + 1), \
			bytes(self.generateValueArray()) \
		)
	# Wrapper for PIL.Image.save()
	def saveImage(self, filename):
		self.getImage().save(filename, "png")
	# Set a string containing an ASCII-art representation of the circle
	def setASCII(self, on = "[]", off = "  "):
		self.ASCII = ""
		for y in range(-self.radius, self.radius + 1):
			for x in range(-self.radius, self.radius + 1):
			#	if Pixel(y, x, True) in self.pixels:
				if self.LUT[y][x]:
					self.ASCII += on
				else:
					self.ASCII += off
			self.ASCII += "\n"
		print("ASCII Art representation set.")
	# Wrappers for a few common ASCII styles
	def setASCIIMinimal(self):
		self.setASCII("#", " ")
	def setASCIIInverted(self):
		self.setASCII("  ", "[]")
	def printASCII(self):
		if not hasattr(self, "ASCII"):
			self.setASCII()
		print(self.ASCII)
	def writeOutASCII(self, filename):
		file = open(filename, "w")
		if not hasattr(self, "ASCII"):
			self.setASCII()
		file.write(self.ASCII)
		file.close()
		print("ASCII Art file written.")
	# Called in __init__(), finds all pixels that best fit the circle
	def generatePixels(self):
		p = Pixel(0, self.radius, True)
		while p.x > 0:
			self.LUT[p.y][p.x] = True
			self.pixels.append(p)
			p = p.findBest(p.getULNeighbors(), self.radius, self.tolerance)
		#	print(p)
		while p.y > 0:
			self.LUT[p.y][p.x] = True
			self.pixels.append(p)
			p = p.findBest(p.getLLNeighbors(), self.radius, self.tolerance)
		#	print(p)
		while p.x < 0:
			self.LUT[p.y][p.x] = True
			self.pixels.append(p)
			p = p.findBest(p.getLRNeighbors(), self.radius, self.tolerance)
		#	print(p)
		while p.y < 0:
			self.LUT[p.y][p.x] = True
			self.pixels.append(p)
			p = p.findBest(p.getURNeighbors(), self.radius, self.tolerance)
		#	print(p)
		print("Pixels generated for radius " + str(self.radius) + ".")

