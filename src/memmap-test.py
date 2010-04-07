#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import timeit
import os
import shelve
from time import strftime
import random
import pathfinder

ROOT_DIR="/home/oyvindio/tmp/memmaps"

def genSample(root=ROOT_DIR):
    """
    """
    p = pathfinder.PathFinder(root)
    files = p.allPaths(os.path.isfile)
    statement = "np.memmap(f, dtype=d)"
    while True:
        filename = random.choice(files)
        setup = "import os; import numpy as np; f = %r; d = %r" % (filename, dtypeFromExt(filename))
        t = timeit.Timer(statement, setup)
        try:
            runtime = t.timeit(1)
            yield (filename, runtime)
        except OSError:
            pass

def dtypeFromExt(filename):
    """
    returns the dtype to pass to numpy.memmap based on filename
    """
    (filename, ext) = os.path.splitext(filename)
    return ext[1:] # strip leading . from ext

def shelveResults(results):
    """
    write the results from the analysis to a shelf, for future
    reference

    Arguments:
    - `results`: a dict containing the results we want to shelve
    """
    s = shelve.open("memmap-%s.shelf" % strftime("%Y-%m-%d-%H%M%S"))
    for k, v in results.iteritems():
        s[k] = v
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

    filenames = [d[0] for d in samples]
    runtimes = [d[1] for d in samples]
    filesizes = [os.stat(p).st_size for p in filenames] # in bytes

    shelveResults({"filenames": filenames, "runtimes": runtimes,
                   "filesizes": filesizes})
