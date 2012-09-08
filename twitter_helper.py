from abstract_helper import AbstractHelper
import json, os, sys
import twitter
import oauth2 as oauth

# parse_qsl moved to urlparse module in v2.6
try:
  from urlparse import parse_qsl
except:
  from cgi import parse_qsl


CLIENT_CREDENTIALS_FILE = "twitter_client_credientials.json"
MESSAGE_IF_MISSING = "Sorry the client credentials file is not found!"


REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

DEFAULT_CREDIENTIALS = {
    "consumer_key":         "",# TODO put consumer key here
    "consumer_secret":      "",# TODO put consumer secret here

    "access_token_key":     "",# will be filled by progrem
    "access_token_secret":  "",# will be filled by program
}

class TwitterHelper(AbstractHelper):
    
    def __init__(self):
        self.authenticated = False
        self.api = twitter.Api()
        self.credentials = {}
        pass

    def authenticate(self):
        if self.authenticated == False:
            # TODO authenticate
            if os.path.exists(CLIENT_CREDENTIALS_FILE) == False:
                if DEFAULT_CREDIENTIALS["consumer_key"] == "" or DEFAULT_CREDIENTIALS["consumer_secret"] == "":
                    print "WARNING:", MESSAGE_IF_MISSING 
                    return [False,MESSAGE_IF_MISSING]
                fp = open(CLIENT_CREDENTIALS_FILE,"w")
                json.dump(DEFAULT_CREDIENTIALS, fp, indent=4)
                fp.close()
            self.credentials = json.load(open(CLIENT_CREDENTIALS_FILE,"r"))
            if self.credentials["access_token_key"] == "" or self.credentials["access_token_secret"] == "":
                [self.credentials["access_token_key"],self.credentials["access_token_secret"]] = self.getCredentials()
                if self.credentials["access_token_key"] == "" or self.credentials["access_token_secret"] == "":
                    return [False,"failed to obtain an access token"]
                else:
                    json.dump(self.credentials, open(CLIENT_CREDENTIALS_FILE,"w"), indent=4)
            try:
                self.api = twitter.Api(
                    consumer_key        =   self.credentials["consumer_key"],
                    consumer_secret     =   self.credentials["consumer_secret"],
                    access_token_key    =   self.credentials["access_token_key"],
                    access_token_secret =   self.credentials["access_token_secret"]
                    )
            except:
                # Failed
                json.dump(DEFAULT_CREDIENTIALS, open(CLIENT_CREDENTIALS_FILE,"w"), indent=4)
                return [False,"failed to authenticate"]
            
            # Set cache
            self.authenticated = True
            return [True,"just authenticated"]
        else:
            return [True,"cached"]

    def postStatus(self,status, params = None):
        status += " #PySns"
        try:
            status = self.api.PostUpdate(status)
        except TwitterError,e:
            return [False, "%s" % e]
        return [True,""]

    def fetchTimeline(self, params = None):
        statuses = self.api.GetUserTimeline()
        results = []
        for s in statuses:
            d = {}
            d["screen_name"] = s.user.screen_name
            d["timestamp"] = s.created_at
            d["status"] = s.text
            results.append(d)
        return results
    def getCredentials(self):

        consumer_key    = self.credentials["consumer_key"]
        consumer_secret = self.credentials["consumer_secret"]

        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        oauth_consumer             = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        oauth_client               = oauth.Client(oauth_consumer)

        # print 'Requesting temp token from Twitter'

        resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'GET')

        if resp['status'] != '200':
            print 'Invalid respond from Twitter requesting temp token: %s' % resp['status']
            return ["",""]
        else:
            request_token = dict(parse_qsl(content))

            print ''
            print 'Please visit this Twitter page and retrieve the pincode to be used'
            print 'in the next step to obtaining an Authentication Token:'
            print ''
            print '%s?oauth_token=%s' % (AUTHORIZATION_URL, request_token['oauth_token'])
            print ''

            pincode = raw_input('Pincode? ')

            token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
            token.set_verifier(pincode)


            oauth_client  = oauth.Client(oauth_consumer, token)
            resp, content = oauth_client.request(ACCESS_TOKEN_URL, method='POST', body='oauth_verifier=%s' % pincode)
            access_token  = dict(parse_qsl(content))

            if resp['status'] != '200':
                print 'The request for a Token did not succeed: %s' % resp['status']
                return ["",""]
            else:
                # print 'Your Twitter Access Token key: %s' % access_token['oauth_token']
                # print '          Access Token secret: %s' % access_token['oauth_token_secret']
                return [access_token['oauth_token'],access_token['oauth_token_secret']]

if __name__ == "__main__":
 


    api = TwitterHelper()
    api.authenticate()
