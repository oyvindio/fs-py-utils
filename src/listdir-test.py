#!/usr/bin/env python
# -*- coding: utf-8 -*-

import timeit
import os
#import matplotlib as mpl
#mpl.use("svg") # plot graphs as scalable vector graphics
#import matplotlib.pyplot as plt
from time import strftime
import abstracttest
import pathfinder

class ListdirTest(abstracttest.AbstractTest):
    
    ROOT_DIR = "/"
    PRGNAME = "listdir"

    def genSample(self, root=ROOT_DIR):
        """
        a generator that yields a tuple of
        (random_path, runtime for os.listdir(random_path))
        """
        p = pathfinder.PathFinder(root)
        statement = "os.listdir(d)"
        while True:
            #directory = p.randomPath(os.path.isdir)
            directory = p.randomDir()
            setup = "import os; d = %r" % directory
            t = timeit.Timer(statement, setup)
            try:
                runtime = t.timeit(1)
                yield (directory, runtime)
            except OSError:
                # This means we can't open directory for whatever
                # reason; typically a permissions issue, or the
                # directory merely does not exist.  When this happens,
                # we merely skip the directory, and try another one
                # automagically
                pass

    def pathLength(self, path, length=0):
        if len(path) <= 1:
            return length
        length += 1
        head, tail = os.path.split(path)
        return self.pathLength(head, length)

    ## def scatterPlot(self, dirsizes, runtimes):
    ##     """
    ##     create a scatter plot
    ##     Arguments:
    ##     - `dirsizes`:
    ##     - `runtimes`:
    ##     """
    ##     ax = plt.figure().add_subplot(111)
    ##     ax.scatter(dirsizes, runtimes)
    ##     ax.axis([0, max(dirsizes), 0, max(runtimes)])
    ##     plt.title("os.listdir run times")
    ##     plt.xlabel("Directory size (file count)")
    ##     plt.ylabel("Run time (seconds)")
    ##     plt.grid(True)
    ##     plt.savefig("listdir-%s.svg" % strftime("%Y-%m-%d-%H%M"))

    def getSamples(self):
        return super(ListdirTest, self).getSamples()

    def shelveResults(self, results):
        return super(ListdirTest, self).shelveResults(results)

if __name__ == "__main__":
    l = ListdirTest()
    samples = l.getSamples()

    paths = [d[0] for d in samples]
    runtimes = [d[1] for d in samples]
    dirsizes = [len(os.listdir(p)) for p in paths]
    pathdepths = map(l.pathLength, paths)

    ## l.scatterPlot(dirsizes, runtimes)
    l.shelveResults({"paths": paths, "runtimes": runtimes,
                     "dirsizes": dirsizes, "pathdepths": pathdepths})
