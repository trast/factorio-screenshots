#!/usr/bin/python

from __future__ import division

import os
import sys
import cStringIO as StringIO
from PIL import Image

FULL_ZOOM = 11

def puterr(x):
    sys.stderr.write(x)
    sys.stderr.flush()

def save(im, z, x, y):
    # logical 0/0 is at (2**(z-1), 2**(z-1))
    ox = (x + 2**(z-1)) % (2**z)
    oy = (y + 2**(z-1)) % (2**z)
    assert 0 <= ox < 2**z, "ox=%d out of range" % ox
    assert 0 <= oy < 2**z, "oy=%d out of range" % oy
    try:
        os.makedirs('%d/%d' % (z, ox))
    except OSError:
        pass
    im.save('%d/%d/%d.jpg' % (z, ox, oy))

def do_slice(f):
    _, sx, sy = os.path.splitext(f)[0].split('_')
    # input is in chunk coordinates, which we slice into 2x2 tiles
    x = int(sx) * 2
    y = int(sy) * 2
    im = Image.open(f)
    for i in range(2):
        for j in range(2):
            save(im.crop((i*512, j*512, (i+1)*512, (j+1)*512)).resize((256,256)), FULL_ZOOM, x+i, y+j)

def main():
    infiles = sys.argv[1:]
    for f in infiles:
        do_slice(f)

if __name__ == '__main__':
    main()
