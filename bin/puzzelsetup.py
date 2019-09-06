#!/usr/bin/env python

#
# Ola Ormset <oladotormsetatrejlersdotno> Rejlers Embriq AS 2019
#

import sys
import os

for path in ["etc", "lib"]:
    sys.path.append(os.path.join(os.path.dirname(__file__),"..",path))

    

from puzzel import puzzelapi
    
puzzel = puzzelapi()

puzzel.authenticate()

