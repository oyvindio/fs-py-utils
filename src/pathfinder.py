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
    CACHE_KEY_FILES = "files"
    CACHE_KEY_DIRS = "dirs"
    
    def __init__(self, root, cache="paths.db"):
        """
        Arguments:
        - `root`: start finding paths from this directory
        - `cache`: a python shelf file for caching paths
        """
        self._root = root
        self._paths = None
        self._dirs = None
        self._files = None
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
            if self._paths is not None:
                cache[self.CACHE_KEY] = self._paths
            if self._dirs is not None:
                cache[self.CACHE_KEY_DIRS] = self._dirs
            if self._files is not None:
                cache[self.CACHE_KEY_FILES] = self._files
        
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

        
    def _initDirs(self):
        """
        Initializes `self._dirs`. This method is intended to be used
        as a mechanism for lazy initialization of `self._dirs`, and
        should thus be called in all public methods which is dependent
        on `self._dirs` being initialized, if `self._dirs is None.
        """
        from contextlib import closing
        with closing(shelve.open(self._cache)) as cache:
            if not cache.has_key(self.CACHE_KEY_DIRS):
                self._dirs = self.allPaths(filterFunc=os.path.isdir)
                self._shelvePaths()
            else:
                self._paths = cache[self.CACHE_KEY_DIRS]

    def _initFiles(self):
        """
        Initializes `self._files`. This method is intended to be used
        as a mechanism for lazy initialization of `self._files`, and
        should thus be called in all public methods which is dependent
        on `self._files` being initialized, if `self._files is None.
        """
        from contextlib import closing
        with closing(shelve.open(self._cache)) as cache:
            if not cache.has_key(self.CACHE_KEY_FILES):
                self._dirs = self.allPaths(filterFunc=os.path.isfile)
                self._shelvePaths()
            else:
                self._paths = cache[self.CACHE_KEY_FILES]

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
        return random.choice(self.allPaths())
        
    def allDirs(self):
        """
        Returns a list of all directories
        """
        if self._dirs is None:
            self._initDirs()
        return self._dirs

    def randomDir(self):
        """
        Returns a random directory
        """
        return random.choice(self.allDirs())


    def allFiles(self):
        """
        Returns a list of all files
        """        
        if self._files is None:
            self._initFiles()
        return self._files

    def randomFile(self):
        """
        Returns a random file
        """
        return random.choice(self.allFiles())
