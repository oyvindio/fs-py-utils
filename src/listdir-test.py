#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import timeit
import random
import shelve
import matplotlib as mpl
mpl.use("svg") # plot graphs as scalable vector graphics
import matplotlib.pyplot as plt
from time import strftime
import pathfinder


ROOT_DIR = "/usr/lib"
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
    p = pathfinder.PathFinder(ROOT_DIR)
    statement = "os.listdir(d)"
    while True:
        directory = p.randomPath()
        setup = "import os; d = %r" % directory
        t = timeit.Timer(statement, setup)
        runtime = t.timeit(1)
        yield (directory, runtime)

def scatterPlot(dirsizes, runtimes, filename):
    """
    create a scatter plot
    Arguments:
    - `dirsizes`:
    - `runtimes`:
    - `filename`: filename excluding extension (.svg)
    """
    ax = plt.figure().add_subplot(111)
    ax.scatter(dirsizes, runtimes)
    ax.axis([0, max(dirsizes), 0, max(runtimes)])
    plt.title("os.listdir run times")
    plt.xlabel("Directory size (file count)")
    plt.ylabel("Run time (seconds)")
    plt.grid(True)

    plt.savefig("{0}.svg".format(filename))

def shelveResults(paths, runtimes, filename):
    """
    write the results from the analysis to a shelve, for future
    reference

    Arguments:
    - `paths`:
    - `runtimes`:
    - `filename`: filename excluding extension (.shelve)
    """
    s = shelve.open("{0}.shelve".format(filename))
    s["paths"] = paths
    s["runtimes"] = runtimes
    s.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        numSamples = int(sys.argv[1])
    else:
        numSamples = 10000

    g = genSample()
    samples = [g.next() for i in range(numSamples)]

    paths = [d[0] for d in samples]
    runtimes = [d[1] for d in samples]
    dirsizes = [len(os.listdir(p)) for p in paths]

    resultTime = strftime("%Y-%m-%d-%H%M%S")
    scatterPlot(dirsizes, runtimes, resultTime)
    shelveResults(paths, runtimes, resultTime)


