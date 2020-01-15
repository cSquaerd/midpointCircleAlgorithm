import mpca
from PIL import Image

def colorize(rcImage):
	if not rcImage.mode == "HSV":
		print("ColorSpace Error: Argument must be in HSV mode.")
		return None
	radius = rcImage.width // 2
	color = radius % 0x100
	for x in range(rcImage.size[0]):
		for y in range(rcImage.size[1]):
			if rcImage.getpixel((x, y)) == (0, 0, 0):
				rcImage.putpixel((x, y), (color, 0xFF, 0xFF))
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



