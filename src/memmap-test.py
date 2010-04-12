#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abstracttest
import pathfinder
import timeit
import os
import random


class MemmapTest(abstracttest.AbstractTest):

    ROOT_DIR = "/home/oyvindio/tmp/memmaps"
    PRGNAME = "memmap"

    def genSample(self, root=ROOT_DIR):
        """
        a generator that yields a tuple of
        (random_file, runtime for np.memmap(random_file))
        """
        p = pathfinder.PathFinder(root)
        statement = "np.memmap(f, dtype=d)"
        while True:
            filename = p.randomFile()
            setup = "import os; import numpy as np; f = %r; d = %r" \
                    % (filename, self.dtypeFromExt(filename))
            t = timeit.Timer(statement, setup)
            try:
                runtime = t.timeit(1)
                yield (filename, runtime)
            except OSError:
                pass

    def dtypeFromExt(self, filename):
        """
        returns the dtype to pass to numpy.memmap based on filename
        """
        (filename, ext) = os.path.splitext(filename)
        return ext[1:] # strip leading . from ext

    def getSamples(self):
        return super(MemmapTest, self).getSamples()

    def shelveResults(self, results):
        return super(MemmapTest, self).shelveResults(results)

if __name__ == "__main__":
    m = MemmapTest()
    samples = m.getSamples()

    filenames = [d[0] for d in samples]
    runtimes = [d[1] for d in samples]
    filesizes = [os.stat(p).st_size for p in filenames] # in bytes

    m.shelveResults({"filenames": filenames, "runtimes": runtimes,
                   "filesizes": filesizes})
