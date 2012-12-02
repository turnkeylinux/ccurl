# Copyright (c) 2012 Alon Swartz <alon@turnkeylinux.org>
# 
# This file is part of CCurl
# 
# CCurl is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.

import os
import urllib

from executil import system, mkarg

from cache import Cache

class Error(Exception):
    pass

def get(url, dest):
    """Get file from <url> and save it to <dest>.

    Tries to retrieve <url> from cache, otherwise stores it in
    cache following retrieval.
    """
    url = urllib.unquote(url)
    if url.endswith("/"):
        raise Error("illegal url - can't get a directory")

    if os.path.isdir(dest):
        dest = os.path.join(dest, os.path.basename(url))
    else:
        if dest.endswith("/"):
            raise Error("no such directory: " + dest)

    if os.path.lexists(dest):
        raise Error("won't overwrite already existing file: " + dest)

    cache = Cache()
    cached_path = cache.retrieve(url, dest)
    if cached_path:
        print "* get: retrieved file from cache"
    else:
        print "* get: retrieving file from network..."
        system("curl -L -f %s -o %s" % (mkarg(url), mkarg(dest)))
        cached_path = cache.store(url, dest)

    return cached_path

def add(src, url):
    """Add file from <src> to the cache using <url> for future retrieval"""
    url = urllib.unquote(url)
    if url.endswith("/"):
        raise Error("illegal url - can't get a directory")

    if not os.path.exists(src):
        raise Error("no such file: " + src)

    print "* add: storing file in cache..."
    cache = Cache()
    cached_path = cache.store(url, src)
    return cached_path

