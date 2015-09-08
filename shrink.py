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
    oy = y
    try:
        os.makedirs('%d/%d' % (z, ox))
    except OSError:
        pass
    puterr('%d/%d/%d.jpg\n' % (z, ox, oy))
    im.save('%d/%d/%d.jpg' % (z, ox, oy))

def do_one_shrink(z, x, y):
    im = Image.new('RGB', (512, 512))
    for i in range(2):
        for j in range(2):
            try:
                im.paste(Image.open('%d/%d/%d.jpg' % (z+1, 2*x+i, 2*y+j)), (i*256, j*256))
            except IOError:
                pass  # meh
    save(im.resize((256, 256), Image.BICUBIC), z, x, y)

def do_shrink(z):
    xs = [int(x) for x in os.listdir(str(z+1))]
    for x in xs:
        if x % 2:
            continue
        ys = [int(os.path.splitext(y)[0]) for y in os.listdir('%d/%d' % (z+1, x))]
        for y in ys:
            if y % 2:
                continue
            do_one_shrink(z, x//2, y//2)

def main():
    for z in range(FULL_ZOOM-1, 0, -1):
        do_shrink(z)

if __name__ == '__main__':
    main()
