from __future__ import with_statement
from optparse import OptionParser
import shelve
from time import strftime

class AbstractTest(object):
    """
    """
    ROOT_DIR = "/"
    SAMPLES=10000
    PRGNAME = "Abstract"

    def __init__(self):
        """
        """
        self.parser  = OptionParser()
        self.parser.add_option("-r", "--root-directory", dest="root",
                          help="root directory for path list")
        self.parser.add_option("-s", "--samples", dest="samples",
                          help="number of samples to use when measuring")

        options, args = self.parser.parse_args()        
        self.root = options.root if options.root else self.ROOT_DIR
        self.numSamples = int(options.samples) if options.samples else self.SAMPLES

    def getSamples(self):
        """
        return a list of samples
        """
        g = self.genSample(self.root)
        samples = [g.next() for i in range(self.numSamples)]
        return samples

    def shelveResults(self, results):
        """
        write the results from the analysis to a shelf, for future
        reference

        Arguments:
        - `results`: a dict containing the results we want to shelve
        """
        from contextlib import closing
        with closing(shelve.open(
            "%s-%s.shelf" % (self.PRGNAME,strftime("%Y-%m-%d-%H%M")))) as s:
            for k, v in results.iteritems():
                s[k] = v
