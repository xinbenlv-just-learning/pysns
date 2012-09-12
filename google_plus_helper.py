import gflags
import httplib2
import logging
import os
import pprint
import sys

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = 'google_plus_client_secrets.json'

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0 for Google Plus

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

# Set up a Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/plus.me',
    message=MISSING_CLIENT_SECRETS_MESSAGE)





class GooglePlusHelper:

    def __init__(self):
        self.authenticated = False
        self.service = None
        self.http = None
        pass

    def authenticate(self):
        if self.authenticated == True:
            return [True,"cached"]
        try:
            # If the Credentials don't exist or are invalid run through the native client
            # flow. The Storage object will ensure that if successful the good
            # Credentials will get written back to a file.
            storage = Storage('plus.dat')
            credentials = storage.get()

            if credentials is None or credentials.invalid:
                credentials = run(FLOW, storage)
            
            # Create an httplib2.Http object to handle our HTTP requests and authorize it
            # with our good Credentials.
            http = httplib2.Http()
            http = credentials.authorize(http)

            service = build("plus", "v1", http=http)

            self.service = service
            self.http = http
            self.authenticated = True
            return [True,"just authenticated"]
        except Excepton,e :
            self.authenticated = False
            return [False,"%s" % e]
    def postStatus(self,status,params = None):
        # Reference http://code.google.com/p/google-plus-platform/issues/detail?id=41
        return [False, "Google Plus currently is Read-Only"]

    def fetchTimeline(self, params = None):
        service = self.service
        http = self.http
        try:
            results = []
            person = service.people().get(userId='me').execute(http=http)

            # print "Got your ID: %s" % person['displayName']
            # print
            # print "%-040s -> %s" % ("[Activitity ID]", "[Content]")

            # Don't execute the request until we reach the paging loop below
            request = service.activities().list(
                userId=person['id'], collection='public')

            # Loop over every activity and print the ID and a short snippet of content.
            while ( request != None ):
                activities_doc = request.execute()
                for item in activities_doc.get('items', []):
                    # print '%-040s -> %s' % (item['id'], item['object']['content'][:30])
                
                    r = {}
                    r['screen_name'] =item['actor']['displayName']
                    r['status'] = item['title']
                    r['timestamp'] = item['updated']
                    results.append(r)
                    
                request = service.activities().list_next(request, activities_doc)
            return results
        except AccessTokenRefreshError:
            print ("The credentials have been revoked or expired, please re-run"
                "the application to re-authorize")
            return []

if __name__ == '__main__':
    api = GooglePlusHelper()
    api.authenticate()    
    api.fetchTimeline()



