import numpy as np
import matplotlib.pyplot as plt
import math
import itertools as it


class Data(object):
    x_data = np.array([])
    y_data = np.array([])
    rate_change = np.array([])
    jump_position = np.array([])

    def __init__(self):
        self.is_filtered = False
        self.is_warped = False

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

    def filter_data(self, mode):
        if mode == 'average':
            self.y_data = average_filter(self.y_data, 30)
            self.is_filtered = True
        elif mode == 'lowpass':
            self.y_data = low_pass_filter(self.y_data, 0.04)
            self.is_filtered = True
        else:
            print "Wrong mode. Data not filtered"

    def delete_jumps(self, warp_window_size, mode):
        data_around_jump = np.zeros(2*warp_window_size+1)
        number_of_jumps = len(self.jump_position)

        for k in range(0, number_of_jumps):

            for i, j in zip(range(0, 2*warp_window_size+1),
                            it.count(int(self.jump_position[k]-warp_window_size))):
                data_around_jump[i] = self.y_data[j]

            if mode == 'filter':
                data_around_jump = average_filter(data_around_jump, 35)
                self.is_warped = True
            elif mode == 'logistic':
                data_around_jump = logistic_function(data_around_jump[0], data_around_jump[-1],
                                                     len(data_around_jump), 2)
                self.is_warped = True
            else:
                print "Wrong mode. Jumps were not deleted"

            for i, j in zip(range(0, 2 * warp_window_size + 1),
                            it.count(int(self.jump_position[k] - warp_window_size))):
                self.y_data[j] = data_around_jump[i]


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


def low_pass_filter(data, alpha):
    data_filtered = np.array([])
    data_filtered = np.append(data_filtered, data[0])

    for i in range(1, len(data)):
        data_filtered = np.append(data_filtered, data_filtered[i-1]
                                  + alpha*(data[i]-data_filtered[i-1]))

    return data_filtered


def logistic_function(min_val, max_val, num_of_samples, curve_steepness):
    arguments = np.linspace(-3, 3, num=num_of_samples)
    result = np.array([])

    for i in range(0, num_of_samples):
        result = np.append(result, (max_val-min_val)/(1+math.exp(-curve_steepness*arguments[i]))+min_val)

    return result


def write_to_file(x_data, y_data, path):
    formatted_data = ["x   y\n"]
    for x, y in zip(x_data, y_data):
        formatted_data += [str(x) + " " + str(y) + "\n"]

    f = open(path, "w")
    f.writelines(formatted_data)
    f.close()


if __name__ == "__main__":

    sample_data = Data()
    sample_data.read_file('sample.txt')
    sample_data.detect_jumps(1)
    sample_data.filter_data('average')

    plt.figure(1)
    plt.plot(sample_data.x_data, sample_data.y_data)

    sample_data.delete_jumps(100, 'logistic')

    plt.figure(2)
    plt.plot(sample_data.x_data, sample_data.y_data)

    plt.show()
    sample_data.save_data()

