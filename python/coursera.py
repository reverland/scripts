import requests
import re
import string
import os

'''
This script is to download videos for course 'High Performance Scientific Computing' in Coursera.
For some reason, These downloads are not allowed according to the download policy.
It's not agree with the spirit for coursera, and many people have a hard time study online.
So I write a script to download videos for myself.

PLEASE DO NOT REDISTRIBUTE THE VIDEOS IF YOU DOWNLOAD THEM.
AND WITH NO WARRANTY.

edit your email and password to login and authenticate.
No matter you are behind some walls or not, change the proxy to work for your self.

GPLv2 license if there must be one.

'''

auth_url = 'https://class.coursera.org/scicomp-001/auth/auth_redirector?type=login&subtype=normal&visiting=https%3A%2F%2Fclass.coursera.org%2Fscicomp-001%2Flecture%2Findex'
video_url = 'https://class.coursera.org/scicomp-001/lecture/index'
proxy = {'https': 'http://127.0.0.1:1998'}
email = 'reverland@reverland.org'
password = 'xxxxxx'


def login(email, password, proxy=None):
    login_page = 'https://www.coursera.org/maestro/api/user/login'
    payload = {'email_address': email, 'password': password}
    headers = {'Referer': 'https://www.coursera.org/account/signin',
               'Cookie': 'csrftoken=VE3o3jqpPUbv16YcMTtBFOvl',
               'X-CSRFToken': 'VE3o3jqpPUbv16YcMTtBFOvl',
               'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'en-us,en;q=0.5',
               'Cache-Control': 'no-cache',
               'Connection': 'keep-alive',
               'Content-Length': '54',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20130303 Firefox/19.0',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    r = s.post(login_page, data=payload, proxies=proxy, headers=headers, verify=False)
    return r.text


def auth(auth_url, proxy):
    r = s.get(auth_url, proxies=proxy)
    return r


def parse_links(video_url, proxy):
    # get video html file
    r = s.get(video_url, proxies=proxy)
    # parse videos urls
    links = re.findall(r'data-modal-iframe="([^"]+)"', r.text)
    return links


def download_with_links(links, proxy):
    for link in links:
        r = s.get(link, proxies=proxy)
        src = re.search('<source type="video/mp4" src="([^"]+)"', r.text).group(1)
        name = string.strip(re.search('course-lecture-title-block">([^<]+)\s+', r.text, re.S).group(1)).replace('/', ' or ')
        print ">> Download %s now..." % name
        if os.path.exists(name):
            print ">> Warning: %s exists. skip" % name
            continue
        with open(name, 'wb') as f:
            r = requests.get(src, proxies=proxy)
            f.write(r.content)


if __name__ == '__main__':
    # initial a session
    s = requests.Session()
    print "Log in with your coursera account now...\n"
    login(email, password, proxy)
    # auth with course
    print "Authenticate your account for the course"
    auth(auth_url, proxy)
    print "success..."
    # parse links
    links = parse_links(video_url, proxy)
    # download files
    print "Begin downloading..."
    download_with_links(links, proxy)
