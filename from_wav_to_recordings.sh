#!/bin/bash

#DATA=${DATA:-/home/atlab/Documents/ss}

for WAV in `ls *.wav`
do
  ch_wave -otype riff -F 16000 -o $WAV ../recordings/$WAV #from wav to recordings
done
#ch_wave -otype riff -F 16000 -o wav/arctic_a0001.wav recordings/arctic_a0001.wav

#sox recordings/arctic_a0001.wav -b16 -r 16k wav/arctic_a0001.wav
