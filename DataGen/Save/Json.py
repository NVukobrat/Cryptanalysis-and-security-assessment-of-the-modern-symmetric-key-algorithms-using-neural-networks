import json

from DataGen.Crypt import CombineCrypt
from DataGen.Save import Save


def index_to_json(index, full_path, type):
	preprocess = dict()

	for cipher in index:
		preprocess[cipher.hex()] = dict()
		preprocess[cipher.hex()][CombineCrypt.CombineCrypt.KEY] = index[cipher][
			CombineCrypt.CombineCrypt.KEY].hex()

		if type == Save.Encrypt:
			preprocess[cipher.hex()][CombineCrypt.CombineCrypt.MSG] = index[cipher][CombineCrypt.CombineCrypt.MSG]
		elif type == Save.Decrypt:
			preprocess[cipher.hex()][CombineCrypt.CombineCrypt.MSG] = index[cipher][
				CombineCrypt.CombineCrypt.MSG].decode('utf-8')

	to_json(preprocess, full_path)


def encrypted_messages_to_json(encrypted_messages, full_path):
	preprocess = list()

	for cipher in encrypted_messages:
		preprocess.append(cipher.hex())

	to_json(preprocess, full_path)


def decrypted_messages_to_json(decrypted_messages, full_path):
	preprocess = list()

	for message in decrypted_messages:
		preprocess.append(message.decode('utf-8'))

	to_json(preprocess, full_path)


def to_json(data, full_path):
	with open(full_path, 'w') as outfile:
		json.dump(data, outfile, indent=4, sort_keys=True)
