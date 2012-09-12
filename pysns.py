from colorstring import colorstring as c

#####Test here


REFERENCE = "https://github.com/xinbenlv/pysns"

class PySns:
    
    def __init__(self, additional_helpers = None):
        # TODO include all helpers here
        self.helpers = {}
        
        # Add googleplus helper
        from google_plus_helper import GooglePlusHelper
        self.helpers["google_plus"] = GooglePlusHelper()

        # Add twitter helper
        
        from twitter_helper import TwitterHelper
        self.helpers["twitter"] = TwitterHelper()

        # Add facebook helper
        # from facebook_helper import FacebookHelper
        # self.helpers.append("twitter", FacebookHelper)

        # Additional Helper for Extension
        if additional_helpers != None:
            for h in additional_helpers:
                self.helpers[h] = additional_helpers[h]

    def console(self):
        while(True):
            command = self.getCommand() 
            if command in ["h","help"]:
                pass
            elif command in ["quit","exit","q","e"]:
                print c("Thank you for using PySNS (visit:%s)" % REFERENCE,"blue")
                print c("Bye!","blue")
                break
            elif command in ["l","login"]:
                results = self.login()
                self.showResults("Login",results)
                continue
            elif command in ["s","status"]:
                # Post a status onto all SNS
                status = self.getStatus()
                results = self.postStatus(status)
                self.showResults("Update Status",results)
                continue
            elif command in ["t","timeline"]:
                self.showTimeline()
                continue
            else:
                print c("Wrong command.","blue")
            print c("Available commands:","blue")
            print c("    's' or 'status': post a new status to all SNS.","blue")
            print c("    't' or 'timeline' fetch my personal status timeline from all SNS.","blue")
            print c("    'l' or 'login' login into all SNS.","blue")
            print c("    'q' or 'quit' or 'e' or 'exit': exit PySns.","blue")
    def login(self):
        results = {}
        for sns in self.helpers:
            api = self.helpers[sns]
            results[sns] = api.authenticate()
        return results
    def getCommand(self):
        return raw_input(c("Command:","blue"))

    def showTimeline(self):

        for sns in self.helpers:
            api = self.helpers[sns]
            if not api.authenticated:
                continue
            print ""
            print c(sns,"clear","green") + " Timeline"
            timeline = api.fetchTimeline()
            for status in timeline:
                s_color = ""
                s_color += "{:>30}".format(c(status["timestamp"], "clear", "blue"))
                s_color += " "
                s_color += "{:>30}".format(c(status["screen_name"], "clear", "yellow")) 
                s_color += ": "
                s_color += status["status"]
                print s_color
            print ""
    def showResults(self,action,results):
        for sns in results:
            if results[sns][0] == True:
                color = "green"
            else:
                color = "red"
            to_user = action + " " + c(sns,"white","green") + " is " + c("%s" % results[sns][0],color)
            if results[sns][1] != "":
                to_user += ", reason: %s" %results[sns][1]
            print to_user

    def getStatus(self):
        return raw_input(c("New Status:","green"))
       
    def postStatus(self,status, tag = True): 
        results = {}
        for sns in self.helpers:
            api = self.helpers[sns]
            if not api.authenticated:
                results[sns] = [False,"not authenticated"]
                continue
            results[sns] = api.postStatus(status)
        return results

if __name__ == "__main__":
    pysns= PySns()
    pysns.console()
