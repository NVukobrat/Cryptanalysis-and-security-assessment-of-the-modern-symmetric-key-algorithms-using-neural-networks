from Crypto.Cipher import AES
from Crypto.Util.py3compat import *


class Crypt:
	BLOCK_SIZE = AES.block_size


def encrypt(key, iv=None, message=None, mode=AES.MODE_ECB):
	cipher_encrypt = None

	if mode == AES.MODE_ECB:
		cipher_encrypt = AES.new(key, AES.MODE_ECB)
	elif mode == AES.MODE_CBC:
		cipher_encrypt = AES.new(key, AES.MODE_CBC, iv)

	message = message.encode()
	message = __pad(message, Crypt.BLOCK_SIZE)
	cipher_message = cipher_encrypt.encrypt(message)

	return cipher_message


def decrypt(key, iv=None, cipher=None, mode=AES.MODE_ECB):
	cipher_decrypt = None

	if mode == AES.MODE_ECB:
		cipher_decrypt = AES.new(key, AES.MODE_ECB)
	elif mode == AES.MODE_CBC:
		cipher_decrypt = AES.new(key, AES.MODE_CBC, iv)

	decrypt_message = cipher_decrypt.decrypt(cipher)
	decrypt_message = __un_pad(decrypt_message, Crypt.BLOCK_SIZE)
	decrypt_message.decode()

	return decrypt_message


def __pad(data_to_pad, block_size, style='pkcs7'):
	padding_len = block_size - len(data_to_pad) % block_size
	if style == 'pkcs7':
		padding = bchr(padding_len) * padding_len
	elif style == 'x923':
		padding = bchr(0) * (padding_len - 1) + bchr(padding_len)
	elif style == 'iso7816':
		padding = bchr(128) + bchr(0) * (padding_len - 1)
	else:
		raise ValueError("Unknown padding style")
	return data_to_pad + padding


def __un_pad(padded_data, block_size, style='pkcs7'):
	data_len = len(padded_data)
	if data_len % block_size:
		raise ValueError("Input data is not padded")
	if style in ('pkcs7', 'x923'):
		padding_len = bord(padded_data[-1])
		if padding_len < 1 or padding_len > min(block_size, data_len):
			raise ValueError("Padding is incorrect.")
		if style == 'pkcs7':
			if padded_data[-padding_len:] != bchr(padding_len) * padding_len:
				raise ValueError("PKCS#7 padding is incorrect.")
		else:
			if padded_data[-padding_len:-1] != bchr(0) * (padding_len - 1):
				raise ValueError("ANSI X.923 padding is incorrect.")
	elif style == 'iso7816':
		padding_len = data_len - padded_data.rfind(bchr(128))
		if padding_len < 1 or padding_len > min(block_size, data_len):
			raise ValueError("Padding is incorrect.")
		if padding_len > 1 and padded_data[1 - padding_len:] != bchr(0) * (padding_len - 1):
			raise ValueError("ISO 7816-4 padding is incorrect.")
	else:
		raise ValueError("Unknown padding style")
	return padded_data[:-padding_len]
