#! /bin/env python
# -*- coding: gbk -*-

"""Download xiqu"""

import urllib
import urllib2
import gevent
from gevent import monkey
import re
from urlparse import urlparse
from posixpath import basename


monkey.patch_all()


def worker(reg, url):
    """docstring for worker"""
    res = urllib.urlopen(url)
    reg3 = re.compile('<embed src="([^"]+)"')
    text = res.read()
    groups = re.finditer(reg, text)
    m_arr = []
    for g in groups:
        name = g.group(2).strip().replace('\\', '') + ".mp3"
        name = unicode(name, 'gb2312')
        print name
        path = 'http://www.00394.net' + g.group(1)
        #print path
        res = urllib.urlopen(path)
        html = res.read()
        path = re.findall(reg3, html)[0]
        #parse_object = urlparse(path)
        #filename = basename(parse_object.path)
        #filename = unicode(filename, 'gbk')
        #print filename
        #filename = filename.encode('utf-8')
        #filename = urllib.quote(filename)
        #path = "http://storage-huabei-1.sdcloud.cn/00394/uploads/media/4/" + filename
        #print path
        path = unicode(path, 'gbk').encode('utf-8')
        path = urllib.quote(path, safe=':/')
        print path
        with open('a.txt', 'a+') as f:
            f.write(path + '\n')
        m_arr.append((name, path))
    return m_arr


def grun(path, name):
    """docstring for grun"""
    urllib.urlretrieve(path, name)

if __name__ == '__main__':
    reg = re.compile('<a href="([^"]+)"\s+class="title">([^<]+)</a>')
    #reg2 = re.compile('<li><span class="pageinfo">[^<]+<strong>([d+])</strong>')
    #res = urllib.urlopen("http://www.00394.net/yuju/yujump3/list_17_1.html")
    #html = res.read()
    #print html
    #page_num = re.findall(reg2, html)
    page_num = 9
    for i in range(page_num):
        url = "http://www.00394.net/yuju/yujump3/list_17_" + str(i + 1) + ".html"
        musicArray = worker(reg, url)
        print musicArray
        jobs = []
        for (name, path) in musicArray:
            jobs.append(gevent.spawn(grun, path, name))
        gevent.joinall(jobs)
