def to_bits(s):
	"""
	Supports only string on input:
	'Hi :D'
	"""
	result = []
	for c in s:
		bits = bin(ord(c))[2:]
		bits = '00000000'[len(bits):] + bits
		result.extend([int(b) for b in bits])
	return result


def from_bits(bits):
	"""
	Supports only bits on input:
	[1, 0, 1, 1, 0, 0, 1, 0]
	"""
	chars = []
	for b in range(int(len(bits) / 8)):
		byte = bits[b * 8:(b + 1) * 8]
		chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
	return ''.join(chars)


def access_hex_bit(data, num):
	"""
	Supports only hex format as input:
	b'\xff'
	"""
	base = int(num / 8)
	shift = num % 8
	return (data[base] & (1 << shift)) >> shift


def hex_to_bits(data):
	"""
	Supports only hex format as input:
	b'\xff'
	"""
	return [access_hex_bit(data, i) for i in range(len(data) * 8)]
