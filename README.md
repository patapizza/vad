vad
===

Simple Voice Activity Detector

## Running

`./run.sh speech.wav noise.wav`

speech.wav is a sample of speech only recorded in the testing environment

noise.wav is a sample of noise only recorded in the testing environment

## Creating WAV files

`sox -d -r 16000 -b 16 -c 1 sample.wav`

## Author

J. Odent

J. Lyons for `framesig` function: see https://github.com/jameslyons/python_speech_features

## License

    GNU GPL v2 - see LICENSE
