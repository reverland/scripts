#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, print_function


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        # run doctests
        import doctest
        import __init__
        fails, count = doctest.testmod(__init__)
        sys.exit(0 if fails == 0 else 1)

    from __init__ import load_trainset, crack_file
    load_trainset()
    for filename in sys.argv[1:]:
        result = crack_file(filename)
        print(result)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
