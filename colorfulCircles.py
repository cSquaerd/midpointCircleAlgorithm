import mpca
from PIL import Image

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

def colorizeQuick(rcImage, pixels, offset):
	if not rcImage.mode == "HSV":
		return None
	radius = rcImage.width // 2
	color = (radius + offset) % 0x100
	for p in pixels:
		rcImage.putpixel((p.x + radius, p.y + radius), (color, 0xFF, 0xFF))
	return rcImage

def alphize(rcImage):
	if not rcImage.mode == "RGBA":
		print("ColorSpace Error: Argument must be in RGBA mode.")
		return None
	for x in range(rcImage.size[0]):
		for y in range(rcImage.size[1]):
			if rcImage.getpixel((x, y)) == (0xFF, 0xFF, 0xFF, 0xFF):
				rcImage.putpixel((x, y), (0x00, 0x00, 0x00, 0x00))
	return rcImage

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

def makeRainbowGif(maxRadius):
	# Generate the discs
	discs = []
	pixelArrays = []
	for r in range(1, maxRadius + 1):
		d = mpca.RasterCircle(r)
		discs.append(d.getImage())
		pixelArrays.append(d.pixels)

	# See how many frames we need	
	numFrames = min(maxRadius, 0x100)
	frames = []
	# Make the frames
	for f in range(numFrames):
		# Generate the discs for the current frame and compose them
		tempFrame = alphize(colorizeQuick(discs[0].convert("HSV"), pixelArrays[0], f).convert("RGBA"))
		i = 1
		for d in discs[1:]:
			nextFrame = alphize(colorizeQuick(d.convert("HSV"), pixelArrays[i], f).convert("RGBA"))
			nextFrame.alpha_composite( \
				tempFrame, \
				( \
					(nextFrame.width - tempFrame.width) // 2, \
					(nextFrame.height - tempFrame.height) // 2 \
				) \
			)
			tempFrame = nextFrame
			i += 1
		frames.append(tempFrame)
		print("Frame", f, "completed.")
	# Save the file
	filename = str(input("Filename? (without extension) "))
	if (type(filename) is str and len(filename) > 0):
		frames[0].save(filename + ".gif", format = "GIF", append_images = frames[1:], save_all = True, duration = 100, loop = 0)
	return frames
