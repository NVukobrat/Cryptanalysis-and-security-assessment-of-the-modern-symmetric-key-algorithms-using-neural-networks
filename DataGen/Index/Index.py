def index_ord(data):
	index = dict()
	for i in range(len(data)):
		index[i] = data[i]

	return index


def index_reverse(data):
	index = dict()
	for i in range(len(data)):
		index[data[i]] = i

	return index
