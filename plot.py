#!/usr/bin/python2.7

import numpy
import matplotlib.pyplot as plt
import json

if __name__ == '__main__':
    '''data = None
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
    if data:
        n = len(data['stream'])
        plt.figure(1)
        plt.plot(numpy.linspace(0, float(n) / 16000, num=n), data['stream'])
        plt.vlines(data['speech'], data['min_freq'], data['max_freq'], 'g')
        plt.vlines(data['noise'], data['min_freq'], data['max_freq'], 'r')
        plt.show(block=False)'''
    data = numpy.load('data.npy')
    n = len(data[0])
    plt.figure(1)
    plt.plot(numpy.linspace(0, float(n) / 16000, num=n), data[0])
    plt.vlines(data[1], -data[3], data[3], 'g')
    plt.vlines(data[2], -data[3], data[3], 'r')
    plt.show()
