import random
from os import listdir

from DataGen.Debug.Log import iteration_progress


def read_cipher_key_group(path,
                          max_size=-1,
                          additional_message='',
                          log=True,
                          log_interval=100,
                          bit_length=-1,
                          random_bit=False,
                          ):
    print("Reading cipher key group (" + additional_message + "): ")

    ciphers = list()
    key_groups = list()

    sum_cipher_file_num = 0
    counter = 0
    for bit_index in listdir(path):
        bit_index_full_path = path + "/" + bit_index
        for exact_bit in listdir(bit_index_full_path):
            exact_bit_full_path = bit_index_full_path + "/" + exact_bit
            for cipher_file in listdir(exact_bit_full_path):
                if sum_cipher_file_num == 0:
                    sum_cipher_file_num = \
                        len(listdir(exact_bit_full_path)) * \
                        len(listdir(bit_index_full_path)) * \
                        len(listdir(path))

                cipher_full_path = exact_bit_full_path + "/" + cipher_file

                with open(cipher_full_path, "r") as open_file:
                    content = open_file.read()

                    if random_bit:
                        content = ''.join(random.sample(content, bit_length))

                    if bit_length != -1 and bit_length > 0:
                        ciphers.append(content[0:bit_length])
                    else:
                        ciphers.append(content)

                key_groups.append(bit_index)

                counter = iteration_progress(log, counter, log_interval, sum_cipher_file_num)

                if max_size != -1 and max_size <= len(key_groups):
                    print("Finished " + str(counter) + "/" + str(sum_cipher_file_num))
                    return ciphers, key_groups

    return ciphers, key_groups
