# Collection of scripts of me

---
## Python

* renren.py
  - A script to visualize renren friendship
  - Dependencies: networkx matplotlib
  - Usage: edit `renren.py` for username and password
  - [Demo](http://reverland.org/python/2013/02/05/visualize-the-friendship-of-renren/)
* tagcloud.py 
  - Visualize command history as cloud tags, also available for other texts.
  - Optional-dependencies: pytagcloud
  - Usage: `history >> hist.txt |python tagcloud hist.txt`
  - [Demo](http://reverland.org/python/2013/01/28/visualize-your-shell-history/)
* captcha.py
  - Thanks to [xenon](http://github.com/xen0n) who modularize it.
  - A script to crack captchas of `正方教务系统`, trainset-included.

        Test 95 items
        Right: 95
        Wrong: 0
        Success rate: 100

  - Dependencies: PIL
  - Usage: `python captcha.py file.gif`
* getphotos.py
  - Download photos in Renren for specific user.
  - Usage: Provide several functions to download photos. More refer to the doc.
* yapmg.py 
  - Yet Another PhotoMosaic Generator written in python.*SPECIAL* for [chaos](http://www.fmedda.com/en/mosaic/chaos) style and classic now.
  - Dependency: PIL
  - Usage: Provide several functions to manipulate photos, and generate photomosaic photo. More refer to the source.
  - Warning: *ALL* non-png images will be converted to png and removed. Just support jpeg/jpg/png now.
  - [Demo](http://reverland.org/python/2013/02/19/yet-another-photomosaic-generator/)
* i2a.py
  - Image to ascii, matrix and ascii style supported.
  - Dependency: PIL
  - Usage: `python i2a.py filename fontsize scale style`
  - [Demo](http://reverland.org/python/2013/02/25/generate-ascii-images-like-the-matrix/)
* missile.py
  - Provide a class to facilitate missile flight simulation.(JUST FOR FUN!)
  - [Demo](http://reverland.org/python/2013/03/02/python/)
* image2css.py
  - Generate the css code to draw specific image.
  - Dependency: PIL
  - Usage: `python image2css.py file [ratio]`
  - [Demo](http://reverland.org/python/2013/03/07/image-to-css/)
* girl-atlas.py
  - Download images from http://girl-atlas.com
  - Usage: `python girl-atlas.py -h` ,Just support download by tag or album now.
* coursera.py
  - Download videos for courses which are not download-allowed.
  - Usage: Edit your email/password/proxy/video\_url/auth\_url in the source file
* agwg.a[X]
  - Wait, I have a new idea...
  - Ghost writing generator for payloads: poorly written to fool reverse enginneer and anti-virus softwares... It will generate a new file.
  - Usage: `python agwg.py file.asm`
* metagoofil.py
  - I just wanna reinvent the wheels...
* 5tps.py
  - 我听评书网交互下载脚本

## Bash

* byr.sh
  - Telnet to bbs.byr.cn with preservation from being kicked off.
  - Dependency: expect
  - Usage: edit your username/password and run `sh byr.sh`
* convert.sh[X]
  - Convert all swf file into mp3 in current directory.(recursively) **Warning: For It will remove all swf files, may damage your data, backup before you use!**
  - Dependency: ffmpeg
  - Usage: sh convert.sh
