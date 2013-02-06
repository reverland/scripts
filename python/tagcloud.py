#import string
import random
import sys
#from pytagcloud import create_tag_image, make_tags
#from pytagcloud.lang.counter import get_tag_counts

filename = sys.argv[1]

# check your own parameter
# 400 0 9 1 4 for Gresburg.txt
# default for command line
boxsize = 600
basescale = 10
fontScale = 0.5
omitnumber = 5
omitlen = 0


def cmd2string(filename):
    '''accept the filename and return the string of cmd'''
    chist = []

    # Open the file and store the history in chist
    with open(filename, 'r') as f:
        chist = f.readlines()
        # print chist

    for i in range(len(chist)):
        chist[i] = chist[i].split()
        chist[i] = chist[i][1]
    ss = ''
    for w in chist:
        if w != 'sudo' and w != 'pacman':
            ss = ss + ' ' + w

    return ss


def string2dict(string, dic):
    """split a string into a dict record its frequent"""
    wl = string.split()
    for w in wl:
        if w == '\n':
            continue
        # if len(w) <= 3:
        #     continue
        if w not in dic:
            dic[w] = 1
        else:
            dic[w] += 1
    return dic


def makeHTMLbox(body, width):
    """takes one long string of words and a width(px) then put them in an HTML box"""
    boxStr = """<div style=\"width: %spx;background-color: rgb(0, 0, 0);border: 1px grey solid;text-align: center; overflow: hidden;\">%s</div>
    """
    return boxStr % (str(width), body)


def makeHTMLword(body, fontsize):
    """take words and fontsize, and create an HTML word in that fontsize."""
    #num = str(random.randint(0,255))
    # return random color for every tags
    color = 'rgb(%s, %s, %s)' % (str(random.randint(0, 255)), str(random.randint(0, 255)), str(random.randint(0, 255)))
    # get the html data
    wordStr = '<span style=\"font-size:%spx;color:%s;float:left;\">%s</span>'
    return wordStr % (str(fontsize), color, body)


#def generatetagcloud(string, filename):
    """accept a string and generate a tag cloud using pytagcloud"""
    tags = make_tags(get_tag_counts(string), minsize=10, maxsize=120)
    create_tag_image(tags, filename.split('.')[0] + '.' + 'png', background=(0, 0, 0), size=(800, 600), fontname='Droid Sans', rectangular=False)


def main():
    # get the html data first
    wd = {}
    s = cmd2string(filename)
    wd = string2dict(s, wd)
    vkl = [(k, v) for k, v in wd.items() if v >= omitnumber and len(k) > omitlen]  # kick off less used cmd
    words = ""
    for w, c in vkl:
        words += makeHTMLword(w, int(c * fontScale + basescale))  # These parameter looks good
    html = makeHTMLbox(words, boxsize)
    # dump it to a file
    with open(filename.split('.')[0] + '.' + 'html', 'wb') as f:
        f.write(html)
    return html


    #generatetagcloud(file2string(filename), filename)
    #print "suscessfully created"
if __name__ == "__main__":
    main()
