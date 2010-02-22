#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import timeit
import random
import shelve
import numpy as np
import matplotlib as mpl
#mpl.use("svg") # plot graphs as scalable vector graphics
import matplotlib.pyplot as plt


ROOT_DIR = "/"
SHELVE_FILE = "dirs.db"

def findAllDirs(directory):
    """
    Returns a list of all subdirectories under directory

    Arguments:
    - `directory`: the directory from which we start the os.walk call
    """
    # ignore these dirs under /
    ignorelist = ["proc", "sys", "dev", "tmp"]
    directories = list()
    # this effectively calls os.listdir on each subdirectory under directory,
    # which may affect measurements... (caching etc.)
    for root, dirs, files in os.walk(directory):
        if root == "/":
            for d in ignorelist:
                if d in dirs:
                    dirs.remove(d)
        directories.append(root)
    return directories
    ## return [root for root, dirs, files in os.walk(directory)]

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

def genSample():
    """
    a generator that yields a tuple of
    (random_path, runtime for os.listdir(random_path))
    """
    directories = readShelvedDirs()
    statement = "os.listdir(d)"
    while True:
        directory = random.choice(directories)
        setup = "import os; d = %r" % directory
        t = timeit.Timer(statement, setup)
        runtime = t.timeit(1)
        #runtime  = timeit.timeit(statement, setup, number=1)
        yield (directory, runtime)

def plot(dirsizes, runtimes):
    """
    create a scatter plot
    Arguments:
    - `dirsizes`:
    - `runtimes`:
    """
    plt.subplot(111)
    plt.axes([0, max(dirsizes), 0, max(runtimes)])
    plt.grid(True)
    plt.scatter(dirsizes, runtimes)
    plt.savefig("/tmp/test.svg")


if __name__ == "__main__":
    g = genSample()
    samples = [g.next() for i in range(100)]

    runtimes = [d[1] for d in samples]
    dirsizes = [len(os.listdir(d[0])) for d in samples]
    plot(dirsizes, runtimes)
