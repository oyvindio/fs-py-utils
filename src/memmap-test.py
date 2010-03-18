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
        mmapFile = random.choice(files)
        setup = "import os; import numpy as np; f = {0}, ext = {1}".format(
            mmapFile, dtypeFromExt(mmapFile))
        t = timeit.Timer(statement, setup)
        try:
            runtime = t.timeit(1)
            yield (mmapFile, runtime)
        except OSError:
            pass

def dtypeFromExt(mmapFile):
    """
    """
    (filename, ext) = os.path.splitext(mmapFile)
    
    return ext[1:] # strip leading . from ext

if __name__ == "__main__":
    g = genSample()
    for dummy in range(10):
        print g.next()
