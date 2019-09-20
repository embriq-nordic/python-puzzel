#!/usr/bin/env python

#
# Ola Ormset <oladotormsetatrejlersdotno> Rejlers Embriq AS 2019
#

import requests
import sys
import datetime
import os
import re
import ast

import puzzelconfig

class puzzelapi:
    def __init__(self, **args):

        self.accessToken = False
        
        for k,w in args.items():
            setattr(self, k, w)

        self.__dict__.update(puzzelconfig.__dict__)
        
        self.args = args

        self.cfgdir = os.path.join(os.environ["HOME"], ".python-puzzel")
        self.tokenfile = os.path.join(self.cfgdir, "accesstoken")
        if not os.path.isdir(self.cfgdir):
            os.mkdir(self.cfgdir)


        return

    def _getToken(self):
        if not os.path.isfile(self.tokenfile):
            return None, None

        try:
            data = open(self.tokenfile).readlines()
            token = data[0]
            info = data[1]
        except:
            return None, None
                
        return token.strip(), info.strip()

    def _tokenTime(self, timestamp):
        return int(re.match(".*\((.*)-\d*\).*", timestamp).groups()[0][:-3])
    
    def _setToken(self):
        open(self.tokenfile, "w").write("%s\n%s" % (self.accessToken, self.accessinfo))
        return
    
    def post(self, api, params={}):
        if self.accessToken:
            params["accessToken"] = self.accessToken
        resp = requests.post(self.baseurl + api, params=params)
        return resp

    def get(self, api, params={}):
        if self.accessToken:
            params["accessToken"] = self.accessToken
        resp = requests.get(self.baseurl + api, params=params)
        return resp

    def authenticate(self):

        token, info = self._getToken()
        info = ast.literal_eval(info)
                
        if token:
            utcnow = int(datetime.datetime.utcnow().strftime("%s"))
            tokentime = self._tokenTime(info["result"]["accessTokenExpiry"])

            if tokentime > utcnow:
                self.accessToken = token
                self.accessinfo = info
                self.userId = info["result"]["userId"]
                return token, info
        
        params = {
            "userName": "%s\%s" % (self.customerKey, self.username),
            "password": self.password
        }
        auth = self.post("/auth/credentials", params)

        returncode = auth.json()["code"]
        if returncode != 0:
            print "unable to log in"
            sys.exit(1)
        
        self.accessToken = auth.json()["result"]

        # Get info on Accesstoken

        res = self.get("/accesstokeninformation")
        self.accessinfo = res.json()
        self.userId = self.accessinfo["result"]["userId"]

        self._setToken()
        
        return self.accessToken, self.accessinfo

    def getvisualqueues(self):
        params = {
            "userId": self.userId
        }

        states = self.get("/%s/visualqueues/stateinformation/All" % self.customerKey, params)

        return states.json()["result"]

    def usersavailable(self):

        params = {
            "customerKey": self.customerKey,
            "userId": self.userId
            }

        res = self.get("/%s/users/%s/usersavailable" % (self.customerKey, self.userId), params)

        return res.json()["result"]

    def users(self):
        res = self.get("/%s/users" % self.customerKey)
        return res.json()["result"]

    def userdetail(self):
        res = self.get("/%s/users/%s" % (self.customerKey, self.userId))
        return res.json()["result"]

    def queuedetail(self, query = ""):
        results = {}
        queues = self.getvisualqueues()

        matches = []
        for q in queues:
            if  query.lower() in q["description"].lower():
                matches.append((q["id"], q["description"]))
        

        for id, desc in matches:
            details = self.get("/%s/visualqueues/%s/info/UserDetailsOnly" %
                               (self.customerKey, id))
            results[(id, desc)] = details.json()["result"]["usersDetails"]

        return results
    
    def callout(self, number, description = "foo"):
        params = {
            "maxAttempts": 1,
            "destination": number,
            "listName": description,
            "requestDescription": description,
            "requestCategory": description
            }
        res = self.post("/%s/users/%s/callout" % (self.customerKey, self.userId), params)
        return res.json()
    
    def usersearch(self, search):
        params = {
            "searchString": search,
            }
        res = self.post("/%s/users/%s/catalog/contacts/search" % (self.customerKey, self.userId), params)
        return res.json()

