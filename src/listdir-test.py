
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import timeit
import os
import shelve
import matplotlib as mpl
mpl.use("svg") # plot graphs as scalable vector graphics
import matplotlib.pyplot as plt
from time import strftime
import pathfinder

ROOT_DIR = "/"

def genSample(root=ROOT_DIR):
    """
    a generator that yields a tuple of
    (random_path, runtime for os.listdir(random_path))
    """
    p = pathfinder.PathFinder(root)
    statement = "os.listdir(d)"
    while True:
        directory = p.randomPath()
        setup = "import os; d = %r" % directory
        t = timeit.Timer(statement, setup)
        try:
            runtime = t.timeit(1)
            yield (directory, runtime)
        except OSError:
            # This means we can't open directory for whatever reason; typically
            # a permissions issue, or the directory merely does not exist.
            # When this happens, we merely skip the directory, and try another
            # one automagically
            pass

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

    plt.savefig("%s.svg" % filename)

def shelveResults(paths, runtimes, filename):
    """
    write the results from the analysis to a shelf, for future
    reference

    Arguments:
    - `paths`:
    - `runtimes`:
    - `filename`: filename excluding extension (.shelf)
    """
    s = shelve.open("%s.shelf" % filename)
    s["paths"] = paths
    s["runtimes"] = runtimes
    s.close()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-r", "--root-directory", dest="root",
                      help="root directory for path list")
    parser.add_option("-s", "--samples", dest="samples",
                      help="number of samples to use when measuring")
    options, args = parser.parse_args()
    root = options.root if options.root else ROOT_DIR
    numSamples = int(options.samples) if options.samples else 10000

    g = genSample(root)
    samples = [g.next() for i in range(numSamples)]

    paths = [d[0] for d in samples]
    runtimes = [d[1] for d in samples]
    dirsizes = [len(os.listdir(p)) for p in paths]

    resultTime = strftime("%Y-%m-%d-%H%M%S")
    scatterPlot(dirsizes, runtimes, resultTime)
    shelveResults(paths, runtimes, resultTime)


