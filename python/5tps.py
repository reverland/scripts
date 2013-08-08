#! /bin/env python
# -*- coding: utf-8 -*-

"""
a script to download 评书 from www.5tps.com

changelog:
    v0.1 initial， search api
    v0.2 warning updates pingshu
    v0.2 fix not right parser -郭德纲
"""

__version__ = '0.2'
__author__ = 'Liu Yuyang'
__license__ = 'BSD'

import sys
import os
import re
import cookielib
import urllib
import urllib2
from time import sleep

DEBUG = 0


def dprint(string):
    """debug for print"""
    if DEBUG:
        print string


class C5tps(object):
    """5tps网"""
    def __init__(self, name):
        super(C5tps, self).__init__()
        self.name = name.decode(sys.getfilesystemencoding())
        self.url = "http://www.5tps.com"
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)
        self.link, self.path = self.grep()

    def get_html(self, url):
        try:
            res = urllib.urlopen(url)
            html = res.read().decode('gbk')
        except:
            return None
        return html

    def search(self):
        data = urllib.urlencode({'keyword': self.name.encode('gbk')})
        try:
            res = urllib.urlopen(self.url + '/search.asp', data)
            html = res.read().decode('gbk')
        except:
            html = None
        return html

    def grep(self):
        print u"[+] 正在搜索相关评书..."
        html = self.search()
        if not html:
            print u"[!] 网络不佳，无法连接"
            html = self.search()
            if not html:
                print u"依旧无法连接，五秒后退出"
                sleep(5)
                exit(0)
        links = re.findall(u'<li><a href=.*' + self.name + u'.*', html)
        # print links
        if not links:
            print u"[X] 未发现有关 %s 的评书" % self.name
            exit(0)
        # print links
        if len(links) > 1:
            for i, l in zip(range(len(links)), links):
                l = re.search(u'html>(.*' + self.name + u'.*)</a>', l).group(1)
                # remove spans
                l = l.replace(u"<span>", "")
                l = l.replace(u"</span>", "")
                if re.search(u'font', l):
                    l += u'<---------！未完结'
                l = l.replace(u"<font color='red'>(", u"(更新到")
                l = l.replace(u"</font>", "")
                print u"[%d]: %s" % (i, l)
            try:
                n = int(raw_input(u">> 键入想要下载评书的序号：（默认为0，回车确认）".encode(sys.getfilesystemencoding())))
            except ValueError:
                n = 0
            link = links[n]
        else:
            link = links[0]
        name = re.search(u'html>(.*' + self.name + u'.*)</a>', link).group(1)
        try:
            m = re.search(u"<font color='red'>.*</font>", name).group(0)
        except:
            m = None
        if m:
            name = name.replace(m, "")
        name = name.replace(u"<span>", "")
        name = name.replace(u"</span>", "")
        dprint(name)
        link = re.search(u'href=([^>]+)', link).group(1)
        return (link, name)

    def download(self, path):
        print u"[+] 正在解析专辑地址,请稍候..."
        html = self.get_html(self.url + self.link)
        if not html:
            print u"[!] 网络不佳，无法解析专辑下载地址。正在重新尝试"
            try:
                html = self.get_html(self.url + self.link)
            except Exception, e:
                dprint(e)
                dprint(u"[!] 无法解析专辑地址，五秒后退出")
                sleep(5)
        links = re.findall(u"href='([^']+)'><IMG", html)
        print u"[+] 解析出专辑地址，准备下载..."
        sleep(3)
        print u"[+] 开始下载整个专辑：%s...\n-------------------" % self.path
        print u"[+] 整个专辑共有%d回" % len(links)
        for link in links:
            html = self.get_html(self.url + link)
            if not html:
                print u"[!] 网络错误，重试中..."
                html = self.get_html(self.url + link)
                if not html:
                    print u"[!] 无法下载，跳过"
                    continue
            try:
                mp3 = re.findall(u'href="(http://[^\:]*:8000[^"]+)"', html)[0]
                name = mp3.split('/')[-1].split('?')[0]
            except Exception, e:
                print u"[!] 解析文件地址失败"
                print u"[!] 无法下载，跳过"
                dprint(e)
                dprint(html)
                continue
            # print name
            if os.path.exists(path + os.path.sep + name):
                continue
            print u"[X] 开始下载%s" % name
            mp3 = unicode.encode(mp3, sys.getfilesystemencoding())
            urllib.urlretrieve(mp3, path + os.path.sep + name)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        name = raw_input(u"[!] 请输入想要所寻的书名: ".encode(sys.getfilesystemencoding()))
        while len(name) == 0:
            name = raw_input(u"[!] 请输入想要所寻的书名: ".encode(sys.getfilesystemencoding()))
    else:
        name = sys.argv[1]
    x = C5tps(name)
    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = x.path
    try:
        os.mkdir(path)
    except:
        print u"[!] 不能新建文件夹"
        if os.path.exists(path):
            print u"[!] 文件夹已存在！"
    x.download(path)
