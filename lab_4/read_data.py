
def read_data():
    f = open(filename, 'r')
    data = []
    for line in f:
        newline = str(line)
        data.append([float(i) for i in newline.split()])
    f.close()
    return data