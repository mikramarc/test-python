import numpy as np
import matplotlib.pyplot as plt


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

    def save_data(self):
        write_to_file(self.x_data, self.y_data, 'results.txt')
        write_to_file(self.x_data, self.rate_change, 'change.txt')

    def detect_jumps(self, threshold):
        for i in range(len(self.y_data)-1):
            self.rate_change = np.append(self.rate_change, abs(self.y_data[i+1]-self.y_data[i]))

            if self.rate_change[i] > threshold:
                self.jump_position = np.append(self.jump_position, i)


def average_filter(data, n):
    num_of_samples = len(data)
    data_filtered = np.zeros(num_of_samples)

    for i in range(n):
        for j in range(-i, i+1):
            data_filtered[i] += data[i+j]
        data_filtered[i] /= 2*i+1

    for i in range(n, num_of_samples-n):
        for j in range(-n, n+1):
            data_filtered[i] += data[i+j]
        data_filtered[i] /= 2*n+1

    for i in range(num_of_samples-n, num_of_samples):
        for j in range(-(num_of_samples-(i+1)), (num_of_samples-(i+1))+1):
            data_filtered[i] += data[i+j]
        data_filtered[i] /= 2*(num_of_samples-(i+1))+1

    return data_filtered


def write_to_file(x_data, y_data, path):
    formatted_data = ["x   y\n"]
    for x, y in zip(x_data, y_data):
        formatted_data += [str(x) + " " + str(y) + "\n"]

    f = open(path, "w")
    f.writelines(formatted_data)
    f.close()


def plot(x_data, y_data):
    plt.plot(x_data, y_data)
    plt.show()


sample_data = Data()
sample_data.read_file('sample.txt')
sample_data.detect_jumps(1)

sample_data.save_data()

sample_data.y_data = average_filter(sample_data.y_data, 30)

plot(sample_data.x_data, sample_data.y_data)
