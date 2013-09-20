########################################################################
#  Copyright (C) 2013 Sol Birnbaum
# 
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
########################################################################

import httplib, urllib

class as_connect(object):
    """ActiveSync connector object"""
    USER_AGENT = "Python"
    POST_URL_TEMPLATE = "/Microsoft-Server-ActiveSync?Cmd=%s&User=%s&DeviceId=123456&DeviceType=Python"

    def __init__(self, server, port=443, ssl=True):
        
        self.server =server
        self.port = port
        self.ssl = ssl
        self.policykey = 0
        self.headers = {
                        "Content-Type": "application/vnd.ms-sync.wbxml",
                        "User-Agent" : self.USER_AGENT,
                        "MS-ASProtocolVersion" : "14.1",
                        "Accept-Language" : "en_us"
                        }
        return

    def set_credential(self, username, password):
        import base64
        self.username = username
        self.credential = base64.b64encode(username+":"+password)
        self.headers.update({"Authorization" : "Basic " + self.credential})

    def post(self, cmd, body):
        url = self.POST_URL_TEMPLATE % (cmd, self.username)
        conn = httplib.HTTPSConnection(self.server, self.port)
        conn.request("POST",url, body, self.headers)
        res = conn.getresponse()
        #print res.status, res.reason, res.getheaders()
        return res.read()
    
    def options(self):
        conn = httplib.HTTPSConnection(self.server, self.port)
        conn.request("OPTIONS","/Microsoft-Server-ActiveSync", None, self.headers)
        res = conn.getresponse()
        if res.status is 200:
            self._server_protocol_versions = res.getheader("ms-asprotocolversions")
            self._server_protocol_commands = res.getheader("ms-asprotocolcommands")
            self._server_version = res.getheader("ms-server-activesync")
        else:
            print "Connection Error!:"
            print res.status, res.reason
            for header in res.getheaders():
                print header[0]+":",header[1]

    def get_policykey(self):
        return self.policykey

    def set_policykey(self, policykey):
        self.policykey = policykey
        self.headers.update({ "X-MS-PolicyKey" : self.policykey })