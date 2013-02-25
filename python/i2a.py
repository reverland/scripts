#! /bin/env python
# -*- coding: utf-8 -*-

"""
Turn images into acsii.
"""

__author__ = 'Reverland (lhtlyy@gmail.com)'

import Image
import ImageOps
import sys


filename = 'a.jpg'


def makeHTMLbox(body, fontsize, imagesize):
    """takes one long string of words and a width(px) then put them in an HTML box"""
    boxStr = """<div style=\"font-size: %spx;line-height: 100%s; width: %s;background-color: rgb(0, 0, 0);border: 1px grey solid;text-align: center; overflow: hidden;\">%s</div>
    """
    return boxStr % (fontsize, '%', imagesize[0], body)


def makeHTMLascii(body, color):
    """take words and , and create an HTML word """
    #num = str(random.randint(0,255))
    # return random color for every tags
    color = 'rgb(%s, %s, %s)' % color
    # get the html data
    wordStr = '<span style=\"color:%s;float:left;\">%s</span>'
    return wordStr % (color, body)


def i2m(im, fontsize):
    """turn an image into ascii like matrix"""
    im = im.convert('L')
    im = ImageOps.autocontrast(im)
    im.thumbnail((im.size[0] / fontsize, im.size[1] / fontsize))
    string = ''
    colors = [(0, i, 0) for i in range(0, 256, 17)]
    words = '据说只有到了十五字才会有经验的'
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            p = im.getpixel((x, y))
            i = 14
            while i >= 0:
                if p >= i * 17:
                    s = makeHTMLascii(words[3 * i:3 * (i + 1)], colors[i])
                    break
                i -= 1
            if x % im.size[0] == 0 and y > 0:
                s = s + '<br/>'
            string = string + s
    return string


def i2a(im, fontsize):
    """turn an image into ascii with colors"""
    im = im.convert('RGB')
    im = ImageOps.autocontrast(im)
    im.thumbnail((im.size[0] / fontsize, im.size[1] / fontsize))
    string = ''
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            c = im.getpixel((x, y))
            # print c
            s = makeHTMLascii('翻', c)
            if x % im.size[0] == 0 and y > 0:
                s = s + '<br/>'
            string = string + s
    return string


def getHTMLascii(filename, fontsize, style='matrix', outputfile='a.html', scale=1):
    """Got html ascii image"""
    im = Image.open(filename)
    size = (int(im.size[0] * scale), int(im.size[1] * scale))
    im.thumbnail(size, Image.ANTIALIAS)
    if style == 'matrix':
        ascii = makeHTMLbox(i2m(im, fontsize), fontsize, im.size)
    elif style == 'ascii':
        ascii = makeHTMLbox(i2a(im, fontsize), fontsize, im.size)
    else:
        print "Just support ascii and matrix now, fall back to matrix"
        ascii = makeHTMLbox(i2m(im, fontsize), fontsize, im.size)
    with open(outputfile, 'wb') as f:
        f.write(ascii)
    return 1


if __name__ == '__main__':
    if sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print """Usage:python i2a.py filename fontsize [optional-parameter]
        optional-parameter:
            scale -- between (0, 1)
            style -- matrix or ascii"""
    else:
        filename = sys.argv[1]
        try:
            fontsize = int(sys.argv[2])
        except:
            fontsize = int(raw_input('input fontsize please:'))
        try:
            scale = float(sys.argv[3])
        except:
            scale = 1
        try:
            style = sys.argv[4]
        except:
            style = 'matrix'
        getHTMLascii(filename, fontsize, scale=scale, style=style)
