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
  - A script to crack captchas of `正方教务系统`
        Test 95 items
        Right: 94
        Wrong: 1
        Success rate: 98.95
  - Dependencies: PIL
  - Usage: `python captcha.py file.gif`
