#! /bin/env python
# -*- coding: utf-8 -*-

'''
A script to download all photos of specific user in Renren.
all photos will be downloaded in current working directory, documented with album names.
will not download `手机相册` and `头像相册` now, Maybe I'll add `手机相册` later maybe not.
NOTICE: all albums with the same name will be downloaded into the same directory.
'''

import os
import urllib
import urllib2
import cookielib
import time
import re
#import cPickle as p

__author__ = '''Reverland (lhtlyy@gmail.com)'''


def download_my_photos():
    username = '****'
    password = '****'
    uid = login(username, password)
    get_photos(uid)
    return 1


def download_friends_photos(uid):
    get_photos(uid, others=True)


def get_photos(uid, others=False):
    '''Get photos, if you want to get others' photos, change `others=True`'''
    if others is True:
        album_list_page = 'http://photo.renren.com/photo/' + str(uid) + '/album/relatives'
    else:
        album_list_page = 'http://photo.renren.com/photo/' + str(uid) + '/?__view=async-html'
    res = urllib2.urlopen(album_list_page)
    html = res.read()
    album_list = re.findall('<a\s+href="([^"]+)"\s+class="album-title">\n<div\sclass="infor">\n<span\s+class="album-name">\n+([^<]+)', html, re.S)
    for album_link, album_name in album_list:
        print 'Downloading album %s now' % album_name
        if not os.path.exists(album_name):
            os.mkdir(album_name)
        res = urllib2.urlopen(album_link)
        html = res.read()
        photo_links = re.findall(",large:'([^']+)", html)
        count = 1
        for photo in photo_links:
            print "Downloading %d photo(s) from album %s" % (count, album_name)
            urllib.urlretrieve(photo, album_name + '/' + str(time.time()) + '.jpg')
            print "Downloaded suscessfully"
            count += 1
        print 'Album %s downloaded' % album_name


def login(username, password):
    """log in and return uid"""
    logpage = "http://www.renren.com/ajaxLogin/login"
    data = {'email': username, 'password': password}
    login_data = urllib.urlencode(data)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    res = opener.open(logpage, login_data)
    print "Login now ..."
    html = res.read()
    #print html

    # Get uid
    print "Getting user id of you now"
    res = urllib2.urlopen("http://www.renren.com/home")
    html = res.read()
    # print html
    uid = re.search("'ruid':'(\d+)'", html).group(1)
    # print uid
    print "Login and got uid successfully"
    return uid
