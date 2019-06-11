from os import listdir
from os.path import isdir, isfile


def read_pan(path):
    data = list()

    for directory in listdir(path):
        path_to_directory = path + "/" + directory
        if not isdir(path_to_directory):
            continue

        for file in listdir(path_to_directory):
            path_to_file = path_to_directory + "/" + file
            if not isfile(path_to_file):
                continue

            with open(path_to_file, "r") as open_file:
                content = open_file.read()

                data.append(content)

    return data
