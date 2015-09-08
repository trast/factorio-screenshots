#!/usr/bin/python

from __future__ import division

import os
import sys
import cStringIO as StringIO
from PIL import Image

FULL_ZOOM = 9

def puterr(x):
    sys.stderr.write(x)
    sys.stderr.flush()

def save(im, z, x, y):
    ox = x % (2**z)
    if ox < 0:
        ox += 2**z
    oy = y + 2**(z-1)
    assert 0 <= ox < 2**z, "ox=%d out of range" % ox
    assert 0 <= oy < 2**z, "oy=%d out of range" % oy
    try:
        os.makedirs('%d/%d' % (z, ox))
    except OSError:
        pass
    puterr('%d/%d/%d.jpg\n' % (z, ox, oy))
    im.save('%d/%d/%d.jpg' % (z, ox, oy))

def do_slice(f):
    _, sx, sy = os.path.splitext(f)[0].split('_')
    # center of image is the x/y coordinate in filename
    # 32x32 in every image -> 8x8 in every tile
    x = (int(sx) - 16) // 8
    y = (int(sy) - 16) // 8
    im = Image.open(f)
    for i in range(4):
        for j in range(4):
            save(im.crop((i*256, j*256, (i+1)*256, (j+1)*256)), FULL_ZOOM, x+i, y+j)

def main():
    infiles = os.listdir('.')
    screenshot_coords = set()
    for f in infiles:
        if not f.startswith('s_'):
            continue
        do_slice(f)

if __name__ == '__main__':
    main()
