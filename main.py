import numpy as np


class Data:
    x_data = np.array([])
    y_data = np.array([])

    def read_file(self, path):
        my_file = open(path, 'r')

        next(my_file)
        for line in my_file:
            line_list = line.split()
            self.x_data = np.append(self.x_data, float(line_list[0]))
            self.y_data = np.append(self.y_data, float(line_list[1]))

        my_file.close()

    def save_file(self, path):
        formatted_data = ["x   y\n"]
        for x, y in zip(self.x_data, self.y_data):
            formatted_data += [str(x) + " " + str(y) + "\n"]
        f = open(path, "w")
        f.writelines(formatted_data)
        f.close()

sample_data = Data()
sample_data.read_file('sample.txt')
print sample_data.x_data
print sample_data.y_data

sample_data.save_file('results.txt')


