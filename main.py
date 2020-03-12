import argparse
import os

import numpy as np

from utils import split_segments, get_number_of_digits
from wavfile import read_wav_info, read_segment, write_24b, write

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input', dest='input', action='store', type=str, required=True,
                    help='Path to the WAV file')
parser.add_argument('--length', dest='length', action='store', type=int, required=True,
                    help='Length of each chunk in seconds')
parser.add_argument('--overlap', dest='overlap', action='store', type=int, required=True,
                    help='Overlap of each chunk in seconds')

args = parser.parse_args()

input_file = args.input
chunk_length = args.length
overlap = args.overlap

assert os.path.isfile(input_file), 'File {} does not exist.'.format(input_file)
assert input_file.lower().endswith('.wav'), '{} is not a WAV file'.format(input_file)

size, comp, num_channels, fs, sbytes, block_align, bitrate, bytes, dtype = read_wav_info(input_file)
raw_pcm = read_segment(input_file, 0, None, normalised=False, retype=False)

byte_length = raw_pcm.size
nframes_per_channel = byte_length // block_align
byte_per_frame = bitrate // 8
length_sec = nframes_per_channel // fs

assert chunk_length > overlap >= 0, "Overlap must be non negative and smaller than length"

nsegs, segs = split_segments(length_sec, chunk_length, overlap, incltail=True)

file, ext = os.path.splitext(input_file)
num_digits = get_number_of_digits(nsegs)
chunk_name_format = '{}__{:0' + str(num_digits) + 'd}{}'

for i, (start, end) in zip(list(range(nsegs)), segs):
    chunk_name = chunk_name_format.format(file, i + 1, ext)
    sample_start = start * fs * num_channels * byte_per_frame
    sample_end = end * fs * num_channels * byte_per_frame
    chunk_size = sample_end - sample_start
    chunk_size_per_channel = chunk_size // num_channels // byte_per_frame

    print(('Chunk #{}/{} named {} is from {} sec to {} sec'.format(i + 1, nsegs, chunk_name, start, end)))
    chunk_data = raw_pcm[sample_start:sample_end]
    uint8_data = chunk_data.reshape((chunk_size_per_channel, num_channels, byte_per_frame)).astype(np.uint8)

    if bitrate == 24:
        write_24b(chunk_name, fs, uint8_data)
    else:
        write(chunk_name, fs, uint8_data, bitrate=bitrate)
