#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import timeit
import random
import shelve
import numpy as np
import matplotlib as mpl
mpl.use("svg") # plot graphs as scalable vector graphics
import matplotlib.pyplot as plt


ROOT_DIR = "/"
SHELVE_FILE = "dirs.db"

def findAllDirs(directory):
    """
    Returns a list of all subdirectories under directory

    Arguments:
    - `directory`: the directory from which we start the os.walk call
    """
    # this effectively calls os.listdir on each directory under directory,
    # which may affect measurements... (caching etc.)
    return [root for root, dirs, files in os.walk(directory)]

def shelveDirs(directories, filename=SHELVE_FILE):
    """
    Writes a list of all paths on the system to a shelve at `filename`.
    """
    s = shelve.open(filename)
    s["dirs"] = directories
    s.close()

def readShelvedDirs(filename=SHELVE_FILE):
    """
    Tries to read a list of paths from the shelve at `filename`. If no
    list is found, scans the file system, creates a new shelve and
    returns a new list of directories.
    """
    s = shelve.open(filename)
    if not s.has_key("dirs"):
        directories = findAllDirs(ROOT_DIR)
        shelveDirs(directories)
        return directories
    else:
        directories = s["dirs"]
        s.close()
        return directories

if __name__ == "__main__":
    directories = readShelvedDirs()
    statement = """\
os.listdir(d)
"""
    setup="""\
import os
import random
d = random.choice({0})
print d
""".format(directories)
    runtime  = timeit.timeit(statement, setup, number=1)
    print runtime

