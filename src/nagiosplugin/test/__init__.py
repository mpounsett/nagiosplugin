# this is a package

import os.path
import sys

def path_setup():
    sys.path[0:0] = [os.path.abspath('%s/../..' % os.path.dirname(__file__))]
