def hex_dump(src, length=16, sep='.', name=''):
	result = []

	# Python3 support
	try:
		xrange(0, 1)
	except NameError:
		xrange = range

	for i in xrange(0, len(src), length):
		sub_src = src[i:i + length]
		hex_val = ''
		isMiddle = False
		for h in xrange(0, len(sub_src)):
			if h == length / 2:
				hex_val += ' '
			h = sub_src[h]
			if not isinstance(h, int):
				h = ord(h)
			h = hex(h).replace('0x', '')
			if len(h) == 1:
				h = '0' + h
			hex_val += h + ' '
		hex_val = hex_val.strip(' ')
		text = ''
		for c in sub_src:
			if not isinstance(c, int):
				c = ord(c)
			if 0x20 <= c < 0x7F:
				text += chr(c)
			else:
				text += sep
		result.append(('%08X:  %-' + str(length * (2 + 1) + 1) + 's  |%s|') % (i, hex_val, text))

	print("Hex Dump (" + name + "):")
	print('\n'.join(result))


def from_hex_to_bytes(hex_value):
	return bytes.fromhex(hex_value)


def from_bytes_to_hex(byte_value):
	return byte_value.hex()
