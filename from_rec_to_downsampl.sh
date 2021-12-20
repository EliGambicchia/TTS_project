#!/bin/bash

#DATA=${DATA:-/home/atlab/Documents/ss}

for WAV in `ls *.wav`
do
  sox recordings/arctic_$WAV -b16 -r 16k ../downsampling/$WAV
done
