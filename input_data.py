__author__ = 'strike'

def read_data(filename = 'data.txt'):
    f = open(filename, 'r')
    data = []
    for line in f:
        newline = str(line)
        data.append([float(i) for i in newline.split()])
    return data

