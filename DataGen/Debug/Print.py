from DataGen.Debug import hex_dump


def debug_print(value, name=""):
	print("#" * 9 + " " + name + " " + "#" * 9)
	print("Value:")
	print(value)
	print()
	hex_dump(value, name=name)
	print("#" * 9 + " " + name + " " + "#" * 9)
	print("")
