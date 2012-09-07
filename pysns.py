import re
import twitter
from twitter import TwitterError
from colorstring import colorstring as c

AUTHOR = "Zainan Victor Zhou <zzn@zzn.im>"

class PySns:
    
    def __init__(self):
        # Twitter 
        self.twitter = twitter.Api(consumer_key='', # TODO put your consumer key for your application
            consumer_secret='', # TODO put your consumer secret for your application
            access_token_key='', # TODO put your access_token_key you obtain from get_access_token.py
            access_token_secret='', # TODO put your access_token_secret you obtain from get_access_token.py
            cache=None)
        # TODO Facebook
        # TODO Google Plus
    def Console(self):
        while(True):
            command = self.GetCommand() 
            if command in ["h","help"]:
                pass
            elif command in ["quit","exit","q","e"]:
                print c("Thank you for using PySNS by %s" % AUTHOR,"blue")
                print c("Bye!","blue")
                break
            elif command in ["s","status"]:
                # Post a message onto all SNS
                message = self.GetMessage()
                results =self.PostMessage(message)
                continue
            elif command in ["t","timeline"]:
                # TODO Fetch timeline from all SNS 
                self.ShowTimeline()
                continue
            else:
                print c("Wrong command.","blue")
            print c("Available commands:","blue")
            print c("    's' or 'status': post a new status to all SNS.","blue")
            print c("    't' or 'timeline' fetch timelines from all SNS.","blue")
            print c("    'q' or 'quit' or 'e' or 'exit': exit PySns.","blue")
 
    def GetCommand(self):
        return raw_input(c("Command:","blue"))
    def ShowTimeline(self):
        
        # Twitter
        print c("Twitter","clear","green") + " Timeline"
        statuses = self.twitter.GetUserTimeline()
        user = statuses[0].user
        statuses = self.twitter.GetFriendsTimeline()
        
        status_names = []
        status_times = []
        status_texts = []
        for s in statuses:
            status_names.append(s.user.screen_name)
            status_times.append("%s" % s.created_at)
            status_texts.append(s.text)
        for i in range(len(statuses)):
            s_color = ""
            s_color += "{:>30}".format(c(status_times[i], "clear", "blue"))
            s_color += " "
            s_color += "{:>30}".format(c(status_names[i], "clear", "yellow")) 
            s_color += ": "
            s_color += status_texts[i]
            print s_color
            
    def GetMessage(self):
        return raw_input(c("New Status:","green"))
       
    def PostMessage(self,message, tag = True): 
        results = {} #key, value = [status,color,additional message]
        try:
            if tag == True:
                message += " #PySns"
            status = self.twitter.PostUpdate(message)
            results["Twitter"] = ["Successful","green",""]
        except TwitterError,e:
            results["Twitter"] = ["Failed","green",str(e)]
        for ret in results:
            to_user = "Post to "+c(ret,"white","green") + " is " + c(results[ret][0],results[ret][1])
            if results[ret][2] != "":
                to_user += ", because: %s" %results[ret][2]
            print to_user
        return results

if __name__ == "__main__":
    pysns= PySns()
    pysns.Console()
