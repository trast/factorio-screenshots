#!/usr/bin/python

from __future__ import division

import multiprocessing
import os
import cStringIO as StringIO
import sys

from PIL import Image

FULL_ZOOM = 11

def puterr(x):
    sys.stderr.write(x)
    sys.stderr.flush()

def save(im, z, x, y):
    ox = x % (2**z)
    oy = y % (2**z)
    try:
        os.makedirs('%d/%d' % (z, ox))
    except OSError:
        pass
    im.save('%d/%d/%d.jpg' % (z, ox, oy))

def do_one_shrink((z, x, y)):
    im = Image.new('RGB', (512, 512))
    for i in range(2):
        for j in range(2):
            try:
                im.paste(Image.open('%d/%d/%d.jpg' % (z+1, 2*x+i, 2*y+j)), (i*256, j*256))
            except IOError:
                pass  # meh, remains black
    save(im.resize((256, 256), Image.BICUBIC), z, x, y)

def do_shrink(z, pool=None):
    xs = [int(x) for x in os.listdir(str(z+1))]
    done = set()
    shrinks_to_do = []
    for x in xs:
        x1 = x - x%2
        ys = [int(os.path.splitext(y)[0]) for y in os.listdir('%d/%d' % (z+1, x))]
        for y in ys:
            y1 = y - y%2
            if (x1, y1) in done:
                continue
            done.add((x1, y1))
            shrinks_to_do.append((z, x1//2, y1//2))
    if pool:
        pool.map(do_one_shrink, shrinks_to_do)
    else:
        map(do_one_shrink, shrinks_to_do)

def main():
    pool = multiprocessing.Pool(12)
    for z in range(FULL_ZOOM-1, 0, -1):
        puterr("%d\n" % z)
        do_shrink(z, pool)

if __name__ == '__main__':
    main()
