#! /bin/env python
# -*- coding: utf-8 -*-


'''
YAPMG -- Yet Another PhotoMosaic Generator written in Python
'''

import Image
import ImageOps
import os
import random
import ImageStat
import cPickle as p

__author__ = "Reverland (lhtlyy@gmail.com)"


def add_frame(image):
    '''Add frame for image.'''
    im = ImageOps.expand(image, border=int(0.01 * max(image.size)), fill=0xffffff)
    return im


def rotate_image(image, degree):
    '''Rotate images for specific degree. Expand to show all'''
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    im = image.rotate(degree, expand=1)
    return im


def drop_shadow(image, offset, border=0, shadow_color=0x444444):
    """Add shadows for image"""
    # Caclulate size
    fullWidth = image.size[0] + abs(offset[0]) + 2 * border
    fullHeight = image.size[1] + abs(offset[1]) + 2 * border
    # Create shadow, hardcode color
    shadow = Image.new('RGBA', (fullWidth, fullHeight), (0, 0, 0))
    # Place the shadow, with required offset
    shadowLeft = border + max(offset[0], 0)  # if <0, push the rest of the image right
    shadowTop = border + max(offset[1], 0)  # if <0, push the rest of the image down
    shadow.paste(shadow_color, [shadowLeft, shadowTop, shadowLeft + image.size[0], shadowTop + image.size[1]])
    shadow_mask = shadow.convert("L")
    # Paste the original image on top of the shadow
    imgLeft = border - min(offset[0], 0)  # if the shadow offset was <0, push right
    imgTop = border - min(offset[1], 0)  # if the shadow offset was <0, push down
    shadow.putalpha(shadow_mask)
    shadow.paste(image, (imgLeft, imgTop))
    return shadow


def process_image(filename, newname):
    '''convert image to png to support transparency'''
    if filename.split('.')[-1] != 'png':
        im = Image.open(filename)
        im.save(newname + '.png')
        print "processing image file %s" % filename
    return 1


def process_directory(path):
    os.chdir(path)
    count = 1
    for filename in os.listdir(path):
        ext = filename.split('.')[-1]
        if ext == 'jpeg' or ext == 'jpg':
            process_image(filename, str(count))
            os.remove(filename)
            count += 1
    return 1


def thumbnail(im, size):
    """thumnail the image"""
    im.thumbnail(size, Image.ANTIALIAS)
    return im


# Just for fun
def chao_image(path, size=(800, 800), thumbnail_size=(50, 50), shadow_offset=(10, 10), backgroud_color=0xffffff):
    image_all = Image.new('RGB', size, backgroud_color)
    for image in os.listdir(path):
        if image.split('.')[-1] == 'png':
            im = Image.open(image)
            degree = random.randint(-30, 30)
            im = thumbnail(rotate_image(drop_shadow(add_frame(im), shadow_offset), degree), thumbnail_size)
            image_all.paste(im, (random.randint(-thumbnail_size[0], size[0]), random.randint(-thumbnail_size[1], size[1])), im)
    return image_all


## May not useful
def rgb2xyz(im):
    """rgb to xyz"""
    rgb2xyz = (0.412453, 0.357580, 0.180423, 0, 0.212671, 0.715160, 0.072169, 0, 0.019334, 0.119193, 0.950227, 0)
    out = im.convert("RGB", rgb2xyz)
    return out


def average_image(im):
    """return average (r,g,b) for image"""
    color_vector = [int(x) for x in ImageStat.Stat(im).mean]
    return color_vector


def compare_vectors(v1, v2):
    """compare image1 and image2, return relations"""
    if len(v1) == len(v2):
        distance = 0
        for i in xrange(len(v1)):
            distance += (v1[i] - v2[i]) ** 2
        return distance
    else:
        print "vector not match in dimensions"


#for r, g, b in list(im.getdata())
def tile_dict(path):
    """Return list of average (R,G,B) for image in this path as dict."""
    dic = {}
    for image in os.listdir(path):
        if image.split('.')[-1] == 'png':
            try:
                im = Image.open(image)
            except:
                print "image file %s cannot open" % image
                continue
            if im.mode != 'RGB':
                im = im.convert('RGB')
            dic[image] = average_image(im)
    return dic


def thumbnail_background(im, scale):
    """thumbnail backgroud image"""
    newsize = im.size[0] / scale, im.size[1] / scale
    im.thumbnail(newsize)
    print 'thumbnail size and the number of tiles %d X %d' % im.size
    return im.size


def find_similar(lst, dic):
    """for lst([R, G, B], Calculate which key-value in dic has the most similarity.Return first 10)"""
    similar = {}
    for k, v in dic.items():
        similar[k] = compare_vectors(v, lst)
        # if len(v) != len(lst):
        #     print v, len(v), lst, len(lst)
    similar = [(v, k) for k, v in similar.items()]  # Not good, lost the same Score
    similar.sort()
    return similar[:10]


def get_image_list(im, dic):
    """receive a thumbnail image and a dict of image to be mosaic, return tiles(filename) in order(as a list)"""
    lst = list(im.getdata())
    tiles = []
    for i in range(len(lst)):
        #print find_similar(lst[i], dic)[random.randrange(10)][1]
        tiles.append(find_similar(lst[i], dic)[random.randrange(10)][1])
    return tiles


def paste_chaos(image, tiles, size, shadow_off_set=(30, 30)):
    """size is thumbnail of backgroud size that is how many tiles per line and row"""
    # image_all = Image.new('RGB', image.size, 0xffffff)
    image_all = image
    lst = range(len(tiles))
    random.shuffle(lst)
    fragment_size = (image.size[0] / size[0], image.size[1] / size[1])
    print 'tiles size %d X %d' % fragment_size
    print 'number of tiles one iteration: %d' % len(lst)
    for i in lst:
        im = Image.open(tiles[i])
        degree = random.randint(-20, 20)
        im = thumbnail(rotate_image(drop_shadow(add_frame(im), shadow_off_set), degree), (fragment_size[0] * 3 / 2, fragment_size[1] * 3 / 2))
        x = i % size[0] * fragment_size[0] + random.randrange(-fragment_size[0] / 2, fragment_size[0] / 2)
        y = i / size[0] * fragment_size[1] + random.randrange(-fragment_size[1] / 2, fragment_size[1] / 2)
        # print x, y
        image_all.paste(im, (x, y), im)
    return image_all


def main(filename, n, scale, iteration, path='./'):
    # 0. select an big image for mosaic
    print "open %s" % filename
    im = Image.open(filename)
    # 1. process image as png to support transparency
    print "process directory %s" % path
    process_directory(path)
    # 2. get a dict for path
    print "get tile dict for path `%s`" % path
    try:
        with open('dic.txt', 'r') as f:
            dic = p.load(f)
    except:
        dic = tile_dict(path)
        with open('dic.txt', 'wb') as f:
            p.dump(dic, f)
    # 3. thumbnail the big image for compare
    print "thumbnail background for compare"
    # n = 30  # 原始图片缩为多少分之一
    # scale = 3  # 原始图片放大倍数
    big_size = im.size[0] * scale, im.size[1] * scale
    im_chao = Image.new('RGB', big_size, 0xffffff)
    imb_t_size = thumbnail_background(im, n)
    print "how may tiles: %d X %d" % imb_t_size
    print 'number of iterations: %d' % iteration
    for i in range(iteration):
        print 'iteration: %d' % (i + 1)
        # 4. get a list of smail image for mosaic
        print "get pic list"
        im_tiles = get_image_list(im, dic)
        # 5. paste in chaos style
        print "generate final image"
        im_chao = paste_chaos(im_chao, im_tiles, imb_t_size)
    return im_chao


if __name__ == '__main__':
    im = main('../mm.jpg', 15, 5, 2)
    im.save('../final3.png')
    im.show()
