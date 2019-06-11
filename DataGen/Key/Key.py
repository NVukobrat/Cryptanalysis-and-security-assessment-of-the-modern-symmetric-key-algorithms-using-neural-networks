from Crypto import Random

from DataGen.Debug import Bits


class Key:
	LOW = 16
	MEDIUM = 24
	HIGH = 32


def generate(length=Key.LOW, static=False):
	"""
	Allowed lengths:
	16 - 128 bit
	24 - 192 bit
	32 - 256 bit
	"""
	if length != Key.LOW and length != Key.MEDIUM and length != Key.HIGH:
		raise Exception("Wrong key length (16, 24 and 32 allowed)")

	if static:
		if length == Key.LOW:
			return b'\x9e\xdd>"\xa5<\x8e`y\xf4\xca=TL\xc6\xf3'
		elif length == Key.MEDIUM:
			return b'\x0b\x80\x8aG\x9aSA\xed\xc3\xe2\x90\x9c\xfa\xb6\r\xc9T\xdddS\x04\x0c\xb7q'
		elif length == Key.HIGH:
			return b'\x11\x05\x00\xbe\xb2,l\xd7\xe8\x9cv\t\x85jw\xear \x9a\tQ\x84\x01?\x02\xbe\xa8wv\xd8\xf1\xa4'

	rnd = Random.new()
	key = rnd.read(length)

	return key


def generate_batch(batch_size, length=Key.LOW, static=False):
	batch = list()

	for i in range(batch_size):
		key = generate(length, static)
		batch.append(key)

	return batch


def generate_zero_one_groups(reference_bit_index, wanted_key_group_size):
	key_batch_size = int(wanted_key_group_size * 3)
	keys = generate_batch(key_batch_size)

	keys_group_zero = list()
	keys_group_one = list()

	for key in keys:
		bits = Bits.hex_to_bits(key)

		if bits[reference_bit_index] == 0 and len(keys_group_zero) != wanted_key_group_size:
			keys_group_zero.append(key)
		elif bits[reference_bit_index] == 1 and len(keys_group_one) != wanted_key_group_size:
			keys_group_one.append(key)

		if len(keys_group_one) == wanted_key_group_size and len(keys_group_zero) == wanted_key_group_size:
			break

	if len(keys_group_one) != wanted_key_group_size or len(keys_group_zero) != wanted_key_group_size:
		raise Exception("Key groups don't satisfy requested criteria for length. Increase key batch size.")

	return keys_group_zero, keys_group_one
