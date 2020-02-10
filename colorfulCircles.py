import mpca
from PIL import Image

# Naive approach to colorizing a circle.
def colorize(rcImage, offset = 0x00):
	if not rcImage.mode == "HSV":
		print("ColorSpace Error: Argument must be in HSV mode.")
		return None
	radius = rcImage.width // 2
	color = (radius + offset) % 0x100
	for x in range(rcImage.size[0]):
		for y in range(rcImage.size[1]):
			if rcImage.getpixel((x, y)) == (0, 0, 0):
				rcImage.putpixel((x, y), (color, 0xFF, 0xFF))
	return rcImage

# Relies on list of pixels that make up the circle to quickly color them.
# Can be used to insert a smaller circle into a larger image.
def colorizeQuick(rcImage, pixels, offset, radius):
	if not rcImage.mode == "HSV":
		return None
	maxRadius = rcImage.width // 2
	color = (radius + offset) % 0x100
	for p in pixels:
		rcImage.putpixel((p.x + maxRadius, p.y + maxRadius), (color, 0xFF, 0xFF))
	return rcImage

# Naive but best approach to cutting out transparency for an image
def alphize(rcImage, fromHSV = False):
	if not rcImage.mode == "RGBA":
		print("ColorSpace Error: Argument must be in RGBA mode.")
		return None
	for x in range(rcImage.size[0]):
		for y in range(rcImage.size[1]):
			if fromHSV:
				if rcImage.getpixel((x, y)) == (0x00, 0x00, 0x00, 0xFF):
					rcImage.putpixel((x, y), (0x00, 0x00, 0x00, 0x00))
			elif rcImage.getpixel((x, y)) == (0xFF, 0xFF, 0xFF, 0xFF):
				rcImage.putpixel((x, y), (0x00, 0x00, 0x00, 0x00))
	return rcImage

# Naive algorithm based on alpha-composition
def makeRainbowDisc(maxRadius):
	if maxRadius < 1:
		print("Argument Error: value must be positive and non-zero")
		return None
	disc = alphize( \
		colorize( \
			mpca.RasterCircle(1).getImage().convert("HSV") \
		).convert("RGBA") \
	)
	for r in range(2, maxRadius + 1):
		next = alphize( \
			colorize( \
				mpca.RasterCircle(r).getImage().convert("HSV") \
			).convert("RGBA") \
		)
		next.alpha_composite( \
			disc, ( (next.width - disc.width) // 2, (next.height - disc.height) // 2) \
		)
		disc = next
	return disc

# Better algorithm based on pixelArrays
def makeRainbowDiscQuick(maxRadius):
	if maxRadius < 1:
		print("Argument Error: value must be positive-non-zero.")
		return None
	pixelArrays = []
	for r in range(1, maxRadius + 1):
		d = mpca.RasterCircle(r)
		pixelArrays.append(d.pixels)
	largestDisc = d.getImage()
	rainbow = colorizeQuick( \
		largestDisc.convert("HSV"), pixelArrays[maxRadius - 1], \
		0, maxRadius \
	)
	for i in range(maxRadius - 2, -1, -1):
		rainbow = colorizeQuick(rainbow, pixelArrays[i], 0, i + 1)
	return alphize(rainbow.convert("RGBA"))

# Makes animated discs where the colors phase inward
def makeRainbowGif(maxRadius, fullSpectrum = False, outward = False):
	if maxRadius < 1:
		print("Argument Error: value must be positive-non-zero.")
		return None
	# Generate the discs
	pixelArrays = []
	for r in range(1, maxRadius + 1):
		d = mpca.RasterCircle(r)
		pixelArrays.append(d.pixels)
	largestDisc = d.getImage()
	# See how many frames we need
	if fullSpectrum:
		numFrames = 0x100
	else:
		numFrames = min(maxRadius, 0x100)
	frames = []
	# Determine animation direction
	if outward:
		frameIterator = range(numFrames - 1, -1, -1)
	else:
		frameIterator = range(numFrames)
	# Make the frames
	for f in frameIterator:
		# Start from the largest disc and use the pixelArrays to put in
		# the colors on one image instead of alpha-composing
		tempFrame = colorizeQuick( \
			largestDisc.convert("HSV"), \
			pixelArrays[maxRadius - 1], \
			f, maxRadius \
		)
		for i in range(maxRadius - 2, -1, -1):
			tempFrame = colorizeQuick(tempFrame, pixelArrays[i], f, i + 1)
		frames.append(alphize(tempFrame.convert("RGBA")))
		print("Frame", f, "completed.")
	# Save the file
	if str(input("Save to file? [Y/n]")) in ('', 'y', 'Y'):
		filename = str(input("Filename? (without extension) "))
		if (type(filename) is str and len(filename) > 0):
			frames[0].save(filename + ".gif", format = "GIF", append_images = frames[1:], save_all = True, duration = 100, loop = 0)
	return frames
