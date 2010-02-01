#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import timeit
import random
import numpy as np

ROOT_DIR = "/tmp"
DIRS_TO_TEST = 10

class RandomListdir(object):
    """
    """
    
    def __init__(self, root="/"):
        """
        """
        self.root = root
        self.directories = self._findAllDirs(root)

    def _findAllDirs(self, directory):
        """
        Returns a list of all subdirectories under directory

        Arguments:
        - `directory`: the directory from which we start the os.walk call
        """
        # this effectively calls os.listdir on each directory under directory,
        # which may affect measurements... (caching etc.)
        return [root for root, dirs, files in os.walk(directory)]

    def testDir(self, directory):
        """
        Arguments:
        - `directory`: the directory we want to test
        """
        return os.listdir(directory)

    def randomDir(self):
        """
        returns a random directory
        """
        return random.choice(self.directories)


if __name__ == "__main__":
    statement = """\
r.testDir(d)
    """
    setup="""\
import os
import random
from __main__ import RandomListdir
r = RandomListdir('/tmp')
d = r.randomDir()
    """
    t = timeit.Timer(statement, setup)
    runtimes = t.repeat(10)
    print runtimes
