
class AbstractHelper:

    def __init__(self):
        self.authenticated = False
        pass

    def authenticate(self):
        '''Check if is authenticated, try to authenticate if necessary
        
        return:
            True if authenticated
            False if failed to authenticate
        '''

        pass

    def postStatus(self,status,params = None):
        '''Post status to the social network

        input:
            status: plaintext unicode for
            params: an object for future extension
        
        return: 
            a dictionary
            
                "success"
                    True if successfully posted
                    False if failed to post
                "reason"
                    a string for the reason for failure
        '''

        pass

    def fetchTimeline(self, params = None):
        '''Fetch Timeline from the social network

        input:
            params: an object for future extension
        return:
            an list of dictionaries, current keys: screen_name, timestamp, status
        '''
        
        pass
