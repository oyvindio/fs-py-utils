# -*- coding: utf-8 -*-

from __future__ import with_statement
import shelve
import os
import random

class PathFinder(object):
    """
    TODO description
    """
    CACHE_KEY = "paths"
    
    def __init__(self, root, cache="paths.db"):
        """
        Arguments:
        - `root`: start finding paths from this directory
        - `cache`: a python shelf file for caching paths
        """
        self._root = root
        self._paths = None
        self._cache = cache

    def _findAllPaths(self):
        """
        Returns a list of all paths under `self._root`
        """
        paths = []
        for root, dirs, files in os.walk(self._root):
            paths.append(root)
            for filename in files:
                paths.append(os.path.join(root, filename))
        return paths

    def _shelvePaths(self):
        """
        Write the list of paths to a shelve at `self._cache`
        """
        from contextlib import closing
        with closing(shelve.open(self._cache)) as cache:
            cache[self.CACHE_KEY] = self._paths
        
    def _initPaths(self):
        """
        Initializes `self._paths`. This method is intended to be used
        as a mechanism for lazy initialization of `self._paths`, and
        should thus be called in all public methods which is dependent
        on `self._paths` being initialized, if `self._paths is None.
        """
        from contextlib import closing
        with closing(shelve.open(self._cache)) as cache:
            if not cache.has_key(self.CACHE_KEY):
                self._paths = self._findAllPaths()
                self._shelvePaths()
            else:
                self._paths = cache[self.CACHE_KEY]

    def allPaths(self, filterFunc=None):
        """
        Returns a list of all paths, optionally filtered by passing `filterFunc`
        and the list of paths through `filter()`.
        """
        if self._paths is None:
            self._initPaths()
        return filter(filterFunc, self._paths)

    def randomPath(self, filterFunc=None):
        """
        Returns a random path, optionally filtering the list paths from which
        we do the random selection, by passing the list and `filterFunc`
        through `filter()`.
        """
        if self._paths is None:
            self._initPaths()
        paths = filter(filterFunc, self._paths)
        return random.choice(paths)
