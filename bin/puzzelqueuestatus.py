#!/usr/bin/env python

import sys
from os.path import dirname
sys.path.append(dirname(__file__))
import puzzelpaths


from puzzel import puzzelapi
    
puzzel = puzzelapi()

puzzel.authenticate()

if len(sys.argv) > 1:
    search = sys.argv[1]
else:
    search = ""
    
status = puzzel.queuedetail(search)

for key, data in status.items():
    id, desc = key
    print "Users in queue", desc
    for user in data:
        if user["contactCentreStatus"] != "LoggedOn":
            continue
        print user["contactCentreStatus"], user["firstName"], user["lastName"]
    print

sys.exit(0)
