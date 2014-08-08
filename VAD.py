#!/usr/bin/python2.7

import numpy
import math
import scipy.io.wavfile
import sys
import array

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

def vad(freq, stream, xi, lambda_n, eta, status='noise', frame_index=0):
    frames = framesig(stream, 0.025 * freq, 0.01 * freq)
    z = numpy.array([numpy.fft.rfft(f, 512) for f in frames])
    speech_lines = []
    noise_lines = []
    for frame in frames:
        gamma = numpy.array(list(map(lambda x,y: numpy.abs(x) ** 2 / y, numpy.fft.rfft(frame, 512), lambda_n)))
        frame_value = (gamma * xi / (1 + xi) - numpy.log(1 + xi)).sum() / len(xi)
        if status == 'noise' and frame_value > eta:
            status = 'speech'
            print("speech started")
            speech_lines.append(0.01 * frame_index)
        elif status == 'speech' and frame_value <= eta:
            status = 'noise'
            noise_lines.append(0.01 * frame_index)
            print("speech stopped")
        frame_index += 1
    return [status, speech_lines, noise_lines, frame_index]

if __name__ == '__main__':
    lambda_n = numpy.load('lambda_n.npy')
    xi = numpy.load('xi.npy')
    eta = numpy.load('eta.npy')[0]
    chances = 0
    stream_full = numpy.array([])
    status = 'noise'
    frame_index = 0
    speech_lines = numpy.array([])
    noise_lines = numpy.array([])
    max_freq = 0
    while True:
        s = sys.stdin.read(2048)
        wave = array.array('h', s)
        stream_full = numpy.append(stream_full, wave)
        stream = numpy.array(wave)
        if len(stream) > 0:
            status, green, red, index = vad(16000, stream, xi, lambda_n, eta, status, frame_index)
            speech_lines = numpy.append(speech_lines, green)
            noise_lines = numpy.append(noise_lines, red)
            frame_index = index
            max_freq = max(max_freq, stream.max())
            try:
                numpy.save('data', numpy.array([stream_full, speech_lines, noise_lines, max_freq]))
            except KeyboardInterrupt:
                break
