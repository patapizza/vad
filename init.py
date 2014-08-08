#!/usr/bin/python2.7

import numpy
import math
import scipy.io.wavfile
import sys
import json

def framesig(sig,frame_len,frame_step,winfunc=lambda x:numpy.ones((1,x))):
    """Frame a signal into overlapping frames.

    :param sig: the audio signal to frame.
    :param frame_len: length of each frame measured in samples.
    :param frame_step: number of samples after the start of the previous frame that the next frame should begin.
    :param winfunc: the analysis window to apply to each frame. By default no window is applied.    
    :returns: an array of frames. Size is NUMFRAMES by frame_len.
    """
    slen = len(sig)
    frame_len = round(frame_len)
    frame_step = round(frame_step)
    if slen <= frame_len: 
        numframes = 1
    else:
        numframes = 1 + math.ceil((1.0*slen - frame_len)/frame_step)
        
    padlen = (numframes-1)*frame_step + frame_len
    
    zeros = numpy.zeros((padlen - slen,))
    padsignal = numpy.concatenate((sig,zeros))
    
    indices = numpy.tile(numpy.arange(0,frame_len),(numframes,1)) + numpy.tile(numpy.arange(0,numframes*frame_step,frame_step),(frame_len,1)).T
    indices = numpy.array(indices,dtype=numpy.int32)
    frames = padsignal[indices]
    win = numpy.tile(winfunc(frame_len),(numframes,1))
    return frames*win

def get_eta(lambda_n, lambda_s, frames, eta_apriori):
    eta = float(eta_apriori)
    while 1:
        z = numpy.array([numpy.fft.rfft(f, 512) for f in frames])
        xi = numpy.array(list(map(lambda x,y: x / y, lambda_s, lambda_n)))
        fp = 0
        for frame in frames:
            gamma = numpy.array(list(map(lambda x,y: numpy.abs(x) ** 2 / y, numpy.fft.rfft(frame, 512), lambda_n)))
            frame_value = (gamma * xi / (1 + xi) - numpy.log(1 + xi)).sum() / len(xi)
            if frame_value > eta:
                fp += 1
        fp_rate = float(fp) / len(frames)
        if fp_rate < 0.05:
            break
        eta *= 2
    return eta


def get_estimate(file):
    freq, stream = scipy.io.wavfile.read(file)
    frames = framesig(stream, 0.025 * freq, 0.01 * freq)
    z = numpy.array([numpy.fft.rfft(f, 512) for f in frames])
    return (numpy.array([sum([numpy.abs(zz[i]) ** 2 for zz in z]) / len(z[0]) for i in range(len(z[0]))]), frames)

if __name__ == '__main__':
    lambda_s, _ = get_estimate(sys.argv[1])
    lambda_n, noisy_frames = get_estimate(sys.argv[2])
    xi = numpy.array(list(map(lambda x,y: x / y, lambda_s, lambda_n)))
    eta = get_eta(lambda_n, lambda_s, noisy_frames, 2)
    numpy.save('lambda_n', lambda_n)
    numpy.save('xi', xi)
    numpy.save('eta', numpy.array([eta]))
