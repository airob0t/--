#coding:utf-8

import glob, os, sys
from PIL import Image

EXTS = ['jpg', 'png']

def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = sum(im.getdata()) / 64
    seq = map(lambda i: 0 if i < avg else 1, im.getdata())
    return reduce(lambda x, (y, z): x | (z << y), enumerate(seq), 0)

def hamming(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h

if __name__ == '__main__':
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        print "Usage: %s image.jpg [dir]" % sys.argv[0]
    else:
        im, wd = sys.argv[1], '.' if len(sys.argv) < 3 else sys.argv[2]
        h = avhash(im)

        os.chdir(wd)
        images = []
        for ext in EXTS:
            images.extend(glob.glob('*.%s' % ext))

        seq = []
        for f in images:
            seq.append((f, hamming(avhash(f), h)))

        for f, ham in sorted(seq, key=lambda i: i[1]):
            print "%d\t%s" % (ham, f)
