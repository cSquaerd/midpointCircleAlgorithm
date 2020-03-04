import mpca
import os

size = 1
mode = 0
modes = "nsi"
current = mpca.RasterCircle(size)
command = ""
prompt = "Raster Circle Browser\n" + \
	"Commands:\n\t" + \
	"w: Increase Size\n\t" + \
	"s: Decrease Size (Minimum: 1)\n\t" + \
	"e: Set Size (Minimum: 1)\n\t" + \
	"a/d: Cycle Drawing Modes\n\t" + \
	"q: Exit\n" + \
	"$ "

while command != 'Q':
	os.system("clear")
	current.printASCII()
	print("Current size:", str(size))
	command = str(input(prompt)).upper()

	if command == "Q":
		continue
	elif command not in "WASDE":
		print("Error: Unknown command.")
		input("(Press any key...)")
		continue
	
	if command == "W":
		size += 1
	elif command == "S" and size > 1:
		size -= 1
	elif command == "E":
		newsize = int(input("Enter a new size: "))
		if newsize > 0:
			size = newsize
		else:
			print("Error: Invalid size.")
			input("(Press any key...)")
	elif command == "D":
		mode += 1
		mode %= 3
	elif command == "A":
		mode -= 1
		mode %= 3

	if command in "WSE":
		current = mpca.RasterCircle(size)
	
	if modes[mode] == "n":
		current.setASCII()
	elif modes[mode] == "s":
		current.setASCIIMinimal()
	elif modes[mode] == "i":
		current.setASCIIInverted()

