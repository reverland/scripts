#! /bin/env python
# -*- coding: utf-8 -*-

"""
A little script to download images from 'http://girl-atlas.com/'
Written for fun by Reverland(lhtlyy@gmail.com)
Free to use and with no warranty, BSD License.
"""

from gevent import monkey
monkey.patch_all()
import requests
#import urllib
import os
#import urllib2
import re
import argparse
parser = argparse.ArgumentParser()
#import gevent


# def http_proxy_handlers(proxy):
#     """dirty work, change opener"""
#     proxy_handler = urllib2.ProxyHandler({"http": proxy})
#     opener = urllib2.build_opener(proxy_handler)
#     urllib2.install_opener(opener)


def get_html(url, proxy=None):
    """get html"""
    #req = urllib2.Request(url)
    #res = urllib2.urlopen(req)
    # print "pull html file"
    #html = res.read()
    # print "end of pulling"
    r = requests.get(url, proxies=proxy)
    html = r.text
    return html


def parse_image_urls(html, pattern):
    """parse_image_urls and store them into a list"""
    result = pattern.findall(html)
    return result


def download(result, path):
    """dirty works, download all files in (name, url) list"""
    for name, url in result:
        print ">>> Begin download %s..." % name
        if os.path.exists(path + name + '.jpeg'):
            print "%s exists, skip..." % name
            continue
        try:
            r = requests.get(url)
            with open(path + name + '.jpeg', 'wb') as f:
                f.write(r.content)
            #urllib.urlretrieve(url, path + name + '.jpeg')
            print ">>> %s downloaded" % name
        except Exception, e:
            print "%s" % e
            continue


def download_by_url(url, path='./'):
    pattern = re.compile('<img title="([^"]+)" src=\'([^!]+)!mid\' />')
    result = parse_image_urls(get_html(url, proxy), pattern)
    download(result, path)


def download_by_tags(url):
    """download by tags"""
    html = get_html(url, proxy)
    next_page = re.compile("<a class=\"btn-form next\" href='([^']+)'>Next</a>").search(html)
    # print "next", next
    while next_page:
        url = 'http://girl-atlas.com' + next_page.group(1)
        # print url
        html_next = get_html(url, proxy)
        html = html + html_next
        next_page = re.compile("<a class=\"btn-form next\" href='([^']+)'>Next</a>").search(html_next)
    pattern = re.compile("<a href='([^']+)' class=\"caption\">(.+)</a>")
    result = parse_image_urls(html, pattern)
    # good enough with gevent, however I comment it.
    # jobs = [gevent.spawn(download_by_url, url, name + '/') for (url, name) in result]
    for album_url, album_name in result:
        album_name = album_name.replace('/', '')
        try:
            os.mkdir(album_name)
        except:
            pass
    # gevent.joinall(jobs)
        download_by_url(album_url, album_name + '/')

# download_by_tags('http://girl-atlas.com/t/40')
# download_by_tags('http://girl-atlas.com/t/722')
# download_by_tags('http://girl-atlas.com/t/937')
# download_by_tags('http://girl-atlas.com/t/6')

if __name__ == "__main__":
    parser.add_argument('-t', help="Download by tags,url format must be like this: 'http://girl-atlas.com/t/6'")
    parser.add_argument('-a', help="Download by albums,url format must be like this: 'http://girl-atlas.com/a/10130108074800002185'")
    parser.add_argument('-p', help="Enable proxy, like 'http://127.0.0.1:1998'")
    args = parser.parse_args()
    # print args
    if args.p:
        proxy = {'http': args.p}
    if args.a:
        print ">>>Downloading from %s now" % args.a
        download_by_url(args.a)
    elif args.t:
        print ">>>Downloading from %s now" % args.t
        download_by_tags(args.t)
