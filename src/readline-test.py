#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import random
import string

def generateTextFile(linecount, linelength, filename):
    """
    Generates a text file with `linecount` lines of length `linelength` with
    random text.
    
    Arguments:
    - `linecount`: no. lines
    - `linelength`: lenght of each line
    - `filename`: filename to write the file to
    """
    text = randomText(linecount, linelength)
    with open(filename, 'w') as f:
        f.write(text)
    
def randomText(linecount, linelength):
    """
    Generates  `linecount` lines of length `linelength` of random text.
    
    Arguments:
    - `linecount`: no. lines
    - `linelength`: lenght of each line
    """
    def randomLine(length):
        return "".join([random.choice(string.letters) for i in range(length)])
    return "\n".join([randomLine(linelength) for i in range(linecount)])


if __name__ == '__main__':
    generateTextFile(1000, 1000, "random.txt")
