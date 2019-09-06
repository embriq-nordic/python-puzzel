#!/usr/bin/env python

#
# Ola Ormset <oladotormsetatrejlersdotno> Rejlers Embriq AS 2019
#

import requests
import sys

import puzzelconfig

class puzzelapi:
    def __init__(self, **args):

        self.accessToken = False
        
        for k,w in args.items():
            setattr(self, k, w)

        self.__dict__.update(puzzelconfig.__dict__)
        
        self.args = args
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
    
