#
# Copyright 2014 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
## -*- coding: utf-8 -*-

import os
import cherrypy
import requests
import json
from json2html import *
from sqldbservice import SqlDBService
from mako.template import Template
from mako.lookup import TemplateLookup


class PersonalityInsightsService:
    """Wrapper on the Personality Insights service"""

    def __init__(self, vcapServices):
        """
        Construct an instance. Fetches service parameters from VCAP_SERVICES
        runtime variable for Bluemix, or it defaults to local URLs.
        """

        # Local variables
        self.url = "https://gateway.watsonplatform.net/personality-insights/api"
        self.username = "046ecae3-1c92-4061-8f5a-d5dd6538bace"
        self.password = "vD4uq7t5YmnV"

        if vcapServices is not None:
            print("Parsing VCAP_SERVICES")
            services = json.loads(vcapServices)
            svcName = "personality_insights"
            if svcName in services:
                print("Personality Insights service found!")
                svc = services[svcName][0]["credentials"]
                self.url = svc["url"]
                self.username = svc["username"]
                self.password = svc["password"]
            else:
                print("ERROR: The Personality Insights service was not found")

    def getProfile(self, text):
        """Returns the profile by doing a POST to /v2/profile with text"""

        if self.url is None:
            raise Exception("No Personality Insights service is bound to this app")
        response = requests.post(self.url + "/v2/profile",
                          auth=(self.username, self.password),
                          headers = {"content-type": "text/plain"},
                          data=text
                          )
        try:
            return json.loads(response.text)
        except:
            raise Exception("Error processing the request, HTTP: %d" % response.status_code)


class DemoService(object):

    def __init__(self, service, sqldb):
        self.service = service
        self.sqldb = sqldb
        self.defaultContent = None
        try:
            contentFile = open("public/text/en.txt", "r")
            self.defaultContent = contentFile.read()
        except Exception as e:
            print "ERROR: couldn't read mobidick.txt: %s" % e
        finally:
            contentFile.close()


    @cherrypy.expose
    def index(self):
        self.insights = ""
        listInsights = sqldb.listInsights()
        if listInsights:
            self.insights = json2html.convert( json = json.dumps(listInsights) ) + "<br/>" 
        return lookup.get_template("index.html").render(content=self.defaultContent,insights=self.insights)


    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def build(self, text=None):
        try:
            profileJson = self.service.getProfile(text)
            self.dump = json.dumps(profileJson)
            return self.dump
        except Exception as e:
            print "ERROR: %s" % e
            return str(e)


    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def save(self, text=None):
        snippet = text[:100]
        json = self.dump
        sqldb.saveInsight(snippet, json)
        print("Insight salvo!")




if __name__ == '__main__':
    lookup = TemplateLookup(directories=["templates"])

    # Get host/port from the Bluemix environment, or default to local
    HOST_NAME = os.getenv("VCAP_APP_HOST", "127.0.0.1")
    PORT_NUMBER = int(os.getenv("VCAP_APP_PORT", "3000"))
    cherrypy.config.update({
        "server.socket_host": HOST_NAME,
        "server.socket_port": PORT_NUMBER,
    })

    # Configure 2 paths: "public" for all JS/CSS content, and everything
    # else in "/" handled by the DemoService
    conf = {
        "/": {
            "tools.response_headers.on": True,
            "tools.staticdir.root": os.path.abspath(os.getcwd())
        },
        "/public": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "./public"
        }
    }

    print("Connecting SqlDB... ")
    sqldb = SqlDBService(os.getenv("VCAP_SERVICES"))
    personalityInsights = PersonalityInsightsService(os.getenv("VCAP_SERVICES"))

    # Start the server
    print("Listening on %s:%d" % (HOST_NAME, PORT_NUMBER))
    cherrypy.quickstart(DemoService(personalityInsights,sqldb), "/", config=conf)
