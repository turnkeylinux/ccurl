# Copyright (c) 2012 Alon Swartz <alon@turnkeylinux.org>
# 
# This file is part of CCurl
# 
# CCurl is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.

import os
import sys
import errno
import shutil
from urlparse import urlparse

def mkdir_parents(path, mode=0777):
    """mkdir 'path' recursively (I.e., equivalent to mkdir -p)"""
    dirs = path.split("/")
    for i in range(2, len(dirs) + 1):
        dir = "/".join(dirs[:i+1])
        if os.path.isdir(dir):
            continue
        os.mkdir(dir, mode)

class Cache:
    def __init__(self):
        _default =  os.path.join(os.environ.get('HOME'), '.ccurl/global')
        self.cache_path = os.environ.get('CCURL_CACHE', _default)

    @staticmethod
    def _warn(s):
        print >> sys.stderr, "warning: " + s

    def _get_cache_path(self, url):
        scheme, netloc, path = urlparse(url)[:3]
        return os.path.join(self.cache_path, scheme, netloc, path.lstrip("/"))

    def retrieve(self, url, path):
        """Retrieves <url> to <path> from cache if available"""
        cached_path = self._get_cache_path(url)

        if not os.path.exists(cached_path):
            return None

        try:
            os.link(cached_path, path)
        except OSError, e:
            if e[0] != errno.EXDEV:
                raise e
            self._warn("copying file from cache instead of hard-linking")
            shutil.copyfile(cached_path, path)

        return cached_path

    def store(self, url, path):
        """Store <path> in cache so it can be retrieved by <url>"""
        cached_path = self._get_cache_path(url)

        if os.path.exists(cached_path):
            self._warn("file already in cache, won't overwrite")
            return cached_path

        mkdir_parents(os.path.dirname(cached_path))
        try:
            os.link(path, cached_path)
        except OSError, e:
            if e[0] != errno.EXDEV:
                raise e
            self._warn("copying file into cache instead of hard-linking")
            shutil.copyfile(path, cached_path)

        return cached_path

    def delete(self, url):
        """Delete <url> from cache"""
        cached_path = self._get_cache_path(url)

        if not os.path.exists(cached_path):
            self._warn("file does not exist in cache")
            return False

        os.remove(cached_path)
        return True

