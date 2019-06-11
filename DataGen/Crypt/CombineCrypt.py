from DataGen.Crypt import AESCrypt, SimpleCrypt
from DataGen.Debug import Log


class CombineCrypt:
	KEY = "key"
	MSG = "msg"
	CIPHER = "cipher"


def crypt_key_message_group(key_group, message_group, log=True, log_interval=20, additional_message=''):
	print("Combine key-message group crypt " + "(" + additional_message + "):")

	encrypted_index = dict()
	encrypted_messages = list()
	counter = 0

	for key in key_group:
		for message in message_group:
			# Encryption
			# cipher_message = AESCrypt.encrypt(
			cipher_message = SimpleCrypt.encrypt(
				key=key,
				message=message
			)
			# debug_print(cipher_message, "Cipher message")

			# Messages
			encrypted_messages.append(cipher_message)

			# Index
			encrypted_index[cipher_message] = dict()
			encrypted_index[cipher_message][CombineCrypt.KEY] = key
			encrypted_index[cipher_message][CombineCrypt.MSG] = message

		counter = Log.iteration_progress(log, counter, log_interval, key_group)

	return encrypted_messages, encrypted_index


def decrypt_key_message_group(cipher_group, cipher_index, log=True, log_interval=15000, additional_message=''):
	print("Combine key-message group decrypt " + "(" + additional_message + "):")

	decrypted_index = dict()
	decrypted_messages = list()
	counter = 0

	for cipher_message in cipher_group:
		# Decryption
		# decrypt_message = AESCrypt.decrypt(
		decrypt_message = SimpleCrypt.decrypt(
			key=cipher_index[cipher_message][CombineCrypt.KEY],
			cipher=cipher_message
		)
		# debug_print(decrypt_message, "Decrypt message")

		# Messages
		decrypted_messages.append(decrypt_message)

		# Index
		decrypted_index[cipher_message] = dict()
		decrypted_index[cipher_message][CombineCrypt.KEY] = cipher_index[cipher_message][CombineCrypt.KEY]
		decrypted_index[cipher_message][CombineCrypt.MSG] = decrypt_message

		counter = Log.iteration_progress(log, counter, log_interval, cipher_group)

	return decrypted_messages, decrypted_index


def crypt_decrypt_success_check(encrypted_index, decrypted_index, additional_message=''):
	print("Crypt-Decrypt stressfulness check (" + additional_message + "): ")

	success = True
	for k1, k2 in zip(encrypted_index, decrypted_index):
		if k1 != k2:
			success = False

		if encrypted_index[k1][CombineCrypt.KEY] != decrypted_index[k2][CombineCrypt.KEY]:
			success = False

	if success:
		print("Successful")
	else:
		print("Unsuccessful")
	print()
