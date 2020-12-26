################################################################################################################
# CROWDSTRIKE FALCON                                                                                           #
# OAuth2 API - Customer SDK                                                                                    #
#                                                                                                              #
# event_streams - Falcon X Horizon Event Stream API Interface Class                                            #
################################################################################################################
# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <https://unlicense.org>

import requests
import json
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

class Event_Streams:
    """ The only requirement to instantiate an instance of this class
        is a valid token provided by the Falcon API SDK OAuth2 class.
    """

    def __init__(self, access_token, base_url="https://api.crowdstrike.com"):
        """ Instantiates the base class, ingests the authorization token, 
            and initializes the headers and base_url global variables. 
        """
        self.headers = { 'Authorization': 'Bearer {}'.format(access_token) }
        self.base_url = base_url

    class Result:
        """ Subclass to handle parsing of result client output. """
        def __init__(self):
            """ Instantiates the subclass and initializes the result object. """
            self.result_obj = {}
            
        def __call__(self, status_code, headers, body):
            """ Formats values into a properly formatted result object. """
            self.result_obj['status_code'] = status_code
            self.result_obj['headers'] = dict(headers)
            self.result_obj['body'] = body
            
            return self.result_obj

    def refreshActiveStreamSession(self, parameters, partition=0):
        """ Refresh an active event stream. Use the URL shown in a GET /sensors/entities/datafeed/v2 response. """
        # [POST] https://assets.falcon.crowdstrike.com/support/api/swagger.html#/event-streams/refreshActiveStreamSession
        FULL_URL = self.base_url+'/sensors/entities/datafeed-actions/v1/{}'.format(str(partition))
        HEADERS = self.headers
        PARAMS = parameters
        try:
            response = requests.request("POST", FULL_URL, json={}, params=PARAMS, headers=HEADERS, verify=False)
            returned = self.Result()(response.status_code, response.headers, response.json())
            
        except Exception as e:
            returned = self.Result()(500, {}, str(e))
        
        return returned

    def listAvailableStreamsOAuth2(self, parameters):
        """ Discover all event streams in your environment. """
        # [GET] https://assets.falcon.crowdstrike.com/support/api/swagger.html#/event-streams/listAvailableStreamsOAuth2
        FULL_URL = self.base_url+'/sensors/entities/datafeed/v2'
        HEADERS = self.headers
        PARAMS = parameters
        try:
            response = requests.request("GET", FULL_URL, params=PARAMS, headers=HEADERS, verify=False)
            returned = self.Result()(response.status_code, response.headers, response.json())
            
        except Exception as e:
            returned = self.Result()(500, {}, str(e))
        
        return returned