#!/usr/bin/python2.7

import numpy
import matplotlib.pyplot as plt
import json

if __name__ == '__main__':
    data = numpy.load('data.npy')
    n = len(data[0])
    plt.figure(1)
    plt.plot(numpy.linspace(0, float(n) / 16000, num=n), data[0])
    plt.vlines(data[1], -data[3], data[3], 'g')
    plt.vlines(data[2], -data[3], data[3], 'r')
    plt.show()
