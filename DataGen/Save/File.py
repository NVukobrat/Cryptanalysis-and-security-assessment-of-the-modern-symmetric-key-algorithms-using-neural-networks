import os
import time

from DataGen.Crypt import CombineCrypt
from DataGen.Debug import Log
from DataGen.Debug import Bits
from DataGen.Debug.Bits import hex_to_bits
from DataGen.Save.Save import Save


def index_to_file(index, root_path, reference_bit, write_type, log=True, log_interval=100, additional_message=''):
	print("Saving index as files (" + additional_message + "): ")

	counter = 0
	for cipher in index:
		cipher_key_group = Bits.access_hex_bit(index[cipher][CombineCrypt.CombineCrypt.KEY], reference_bit)

		full_dir_path, full_file_name = __index_cipher_paths(root_path, cipher_key_group, reference_bit)

		if write_type == Save.Hex:
			cipher = cipher.hex()
		elif write_type == Save.Byte:
			cipher = cipher
		elif write_type == Save.Bit:
			cipher = hex_to_bits(cipher)
			cipher = ''.join(str(e) for e in cipher)
		else:
			raise Exception("Invalid write type (Hex and Byte allowed)")

		to_file(
			cipher,
			full_dir_path,
			full_file_name,
			write_type
		)

		counter = Log.iteration_progress(log, counter, log_interval, index)


def __index_cipher_paths(root_path, cipher_key_group, reference_bit):
	full_dir_path = __cipher_dir_path(
		root_path,
		cipher_key_group,
		reference_bit
	)

	full_file_name = __cipher_file_name(
		cipher_key_group,
		reference_bit
	)

	return full_dir_path, full_file_name


def __cipher_dir_path(root_path, cipher_key_group, reference_bit):
	full_dir_path = root_path + "/" + str(cipher_key_group) + "/" + str(reference_bit) + "/"

	return full_dir_path


def __cipher_file_name(cipher_key_group, reference_bit):
	timestamp = time.time()
	timestamp = str(timestamp).replace(".", "_")

	full_file_name = "cipher_" + str(cipher_key_group) + "_" + str(reference_bit) + "_" + timestamp

	return full_file_name


def to_file(data, full_dir_path, file_name, input_data_type):
	if not os.path.exists(full_dir_path):
		os.makedirs(full_dir_path)

	write_type = ""
	if input_data_type == Save.Hex:
		write_type = 'w'
		file_name += ".txt"
	elif input_data_type == Save.Byte:
		write_type = 'wb'
	elif input_data_type == Save.Bit:
		write_type = 'w'
		file_name += ".txt"

	with open(full_dir_path + "/" + file_name, write_type) as outfile:
		outfile.write(data)
