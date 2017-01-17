import numpy as np

x_data = np.array([])
y_data = np.array([])

file = open('sample.txt', 'r')

next(file)
for line in file:
    x = line.split()
    x_data = np.append(x_data, float(x[0]))
    y_data = np.append(y_data, float(x[1]))

print x_data
print y_data
print type(x_data)
file.close()
