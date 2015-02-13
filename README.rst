Ccurl - Caching curl
====================

ccurl.py module
---------------

FUNCTIONS::

    add(src, url)
        Add file from <src> to the cache using <url> for future retrieval
    
    delete(url)
        Delete <url> from cache
    
    get(url, dest)
        Get file from <url> and save it to <dest>.
        
        Tries to retrieve <url> from cache, otherwise stores it in
        cache following retrieval.

Command line interface
----------------------

add::

    Syntax: ./cmd_add.py <path> <url>
    Add file from path to cache using url for future retrieval

    Arguments:

        path            Path to source file
        url             URL of the file's origin

    Environment:

        CCURL_CACHE     Path to ccurl's cache (default: $HOME/.ccurl/global)

del::

    Syntax: ./cmd_del.py <url>
    Remove file from cache using url

    Arguments:

        url             URL of the file's origin

    Environment:

        CCURL_CACHE     Path to ccurl's cache (default: $HOME/.ccurl/global)

    Note:

        To delete all files that aren't being used (ie. no hardlinks):
        cd $HOME/.ccurl/global
        find -type f -name "*.deb" -links 1 -delete

get::
    Syntax: ./cmd_get.py <url> [ <path> ]
    Get file from url and save to path

    Arguments:

        url             URL of file to get
        path            Path to save file (default: .)

    Environment:

        CCURL_CACHE     Path to ccurl's cache (default: $HOME/.ccurl/global)
