import numpy as np


class Data:
    x_data = np.array([])
    y_data = np.array([])
    rate_change = np.array([])
    jump_position = np.array([])

    def read_file(self, path):
        my_file = open(path, 'r')

        next(my_file)
        for line in my_file:
            line_list = line.split()
            self.x_data = np.append(self.x_data, float(line_list[0]))
            self.y_data = np.append(self.y_data, float(line_list[1]))

        my_file.close()

    def save_data(self, path):
        write_to_file(self.x_data, self.y_data, path)

    def detect_jumps(self, threshold):
        for i in range(len(self.y_data)-1):
            self.rate_change = np.append(self.rate_change, abs(self.y_data[i+1]-self.y_data[i]))

            if self.rate_change[i] > threshold:
                self.jump_position = np.append(self.jump_position, i)


def write_to_file(x_data, y_data, path):
    formatted_data = ["x   y\n"]
    for x, y in zip(x_data, y_data):
        formatted_data += [str(x) + " " + str(y) + "\n"]

    f = open(path, "w")
    f.writelines(formatted_data)
    f.close()


sample_data = Data()
sample_data.read_file('sample.txt')
sample_data.detect_jumps(1)

print sample_data.jump_position

sample_data.save_data('results.txt')


