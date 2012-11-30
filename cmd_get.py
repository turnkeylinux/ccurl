#!/usr/bin/python
# 
# Copyright (c) 2012 Alon Swartz <alon@turnkeylinux.org>
# 
# This file is part of CCurl
# 
# CCurl is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
"""
Get file from url and save to path

Arguments:

    url             URL of file to get
    path            Path to save file (default: .)

Environment:

    CCURL_CACHE     Path to ccurl's cache (default: $HOME/.ccurl/global)
"""

import sys
import getopt

import ccurl

def fatal(e):
    print >> sys.stderr, "error: " + str(e)
    sys.exit(1)

def usage(e=None):
    if e:
        print >> sys.stderr, "error: " + str(e)

    print >> sys.stderr, "Syntax: %s <url> [ <path> ]" % sys.argv[0]
    print >> sys.stderr, __doc__.strip()
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError, e:
        usage(e)

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

    if len(args) < 1:
        usage()

    url = args[0]
    try:
        dest = args[1]
    except IndexError:
        dest = "."

    try:
        ccurl.get(url, dest)
    except ccurl.Error, e:
        fatal(e)

if __name__=="__main__":
    main()

