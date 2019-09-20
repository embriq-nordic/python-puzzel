#!/usr/bin/env python

#
# Ola Ormset <oladotormsetatrejlersdotno> Rejlers Embriq AS 2019
#

import sys
from os.path import dirname
sys.path.append(dirname(__file__))
import puzzelpaths


from puzzel import puzzelapi
    
puzzel = puzzelapi()

puzzel.authenticate()

print "UserID: %s" % puzzel.userId
print "AccessToken: %s" % puzzel.accessToken

sys.exit(0)
