#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import random
import pathfinder

ROOT_DIR="/tmp/memmaps"

def genSample(root=ROOT_DIR):
    """
    """
    p = pathfinder.PathFinder(root)
    files = filter(os.path.isfile, p.allPaths())
    statement = "np.memmap(f, dtype=ext)"
    while True:
        filename = random.choice(files)
        setup = "import os; import numpy as np; f = %s, ext = %s" % filename, dtypeFromExt(filename)
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

if __name__ == "__main__":
    g = genSample()
    for dummy in range(10):
        print g.next()
