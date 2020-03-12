import numpy as np


def split_segments(siglen, window, noverlap, incltail=False):
    """
    Calculate how many segments can be extracted from a signal given
    the window size and overlap size
     INPUT:
      - SIGLEN : length of the signal
      - WINDOW : window size (number of samples)
      - NOVERLAP: overlap size (number of samples)
      - INCLTAIL: true to always include the last owner (might be < window)
                    false to exclude it if it's < window
     OUTPUT:
      - NSEGS   : number of segments that can be extracted
      - SEGS    : a two dimensional arrays. Each column is a pair of segments
                   indices
     Example:
      [nsegs, segs] = nsegment(53, 10, 5)
       nsegs = 9
       segs =
         1    10
         6    15
        11    20
        16    25
        21    30
        26    35
        31    40
        36    45
        41    50
      tail:
        51    53
    """
    idx1 = np.arange(0, siglen, window - noverlap)
    idx2 = idx1 + window

    last = np.where(idx2 > siglen)[0][0] + 1
    if idx2[last - 2] == siglen:
        incltail = False
    if incltail:
        nsegs = last
        idx2[nsegs - 1] = siglen
    else:
        nsegs = last - 1

    segs = np.empty((nsegs, 2), dtype=np.uint32)

    segs[:, 0] = idx1[:nsegs]
    segs[:, 1] = idx2[:nsegs]

    return nsegs, segs.tolist()


def get_number_of_digits(number):
    num_digits = 0
    while number > 0:
        number //= 10
        num_digits += 1

    return num_digits
