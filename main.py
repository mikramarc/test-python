import numpy as np


def read_file():
    my_file = open('sample.txt', 'r')
    x = np.array([])
    y = np.array([])

    next(my_file)
    for line in my_file:
        line_list = line.split()
        x = np.append(x, float(line_list[0]))
        y = np.append(y, float(line_list[1]))

    my_file.close()
    return x, y

x_data, y_data = read_file()
print x_data
print y_data
print type(x_data)


