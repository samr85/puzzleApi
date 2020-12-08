import tornado.web
import json
import re

wordList = [
    ("hello", 1),
    ("hello2", 2),
    ("other", 4)
]

class RegexWordList(tornado.web.RequestHandler):
    def get(self, regexUrlComponent):
        """ This is what gets called when the user request the page specified below in the requests list """
        # Any URL encoding in the component will have been undone before getting here
        print(regexUrlComponent)
        try:
            # Attempt to compile the regex for later use
            # If the user has given a bad regex, then this can except
            compRegex = re.compile(regexUrlComponent)
        except re.error as e:
            # Send an error message saying what was wrong with the regex to the user
            message = "Invalid regex: %s. Input was: '%s'"%(e.msg, regexUrlComponent)
            raise tornado.web.HTTPError(status_code=400, reason=message, log_message=message)
        self.write_error

        matchEntries = []
        # Do the actual job here - find the entries that match the word list
        for entry in wordList:
            if compRegex.search(entry[0]):
                matchEntries.append(entry)

        # Convert from a list of tuples into a list of dicts
        matchInfo = []
        for entry in matchEntries:
            matchInfo.append({
                "word": entry[0],
                "weight": entry[1],
            })

        # JSON return calls must be a dict, cannot be a list
        retInfo = {
            "matches": matchInfo,
        }

        # Send the data to the client.
        # This would normally be a string, but if you put a dict in, then it will be sent as JSON
        self.write(retInfo)

requests = [
    # Match against anything specified after regexWordList, treating the entire rest of the string as the regex
    (r"/regexWordList/(.+)", RegexWordList),
]
