#!/usr/bin/env python

#
# Ola Ormset <oladotormsetatrejlersdotno> Rejlers Embriq AS 2019
#

import sys
from os.path import dirname
sys.path.append(dirname(__file__))
from puzzelsetup import puzzel

result = puzzel.callout(sys.argv[1], sys.argv[2])

print result

sys.exit(0)
