#!/bin/bash

speechfile=$1
noisefile=$2

./init.py $speechfile $noisefile && sox -d -r 16000 -b 16 -c 1 -t raw - | ./VAD.py

./plot.py

rm *.npy
