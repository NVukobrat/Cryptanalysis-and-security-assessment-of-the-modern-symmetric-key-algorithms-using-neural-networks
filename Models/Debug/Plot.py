import matplotlib.pyplot as plt


def block_size_distribution(ciphers):
    block_sizes = dict()
    for cipher in ciphers:
        cipher_block_num = int(len(cipher) / 16)

        if cipher_block_num in block_sizes:
            block_sizes[cipher_block_num] += 1
        else:
            block_sizes[cipher_block_num] = 1

    plt.bar(block_sizes.keys(), block_sizes.values(), color='g')
    plt.show()
