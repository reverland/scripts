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

## Bash

* byr.sh
  - Telnet to bbs.byr.cn with preservation from being kicked off.
  - Dependency: expect
  - Usage: edit your username/password and run `sh byr.sh`
