import threading

import asyncio
import tornado.ioloop
import tornado.web

# Import the plugins
import regexWordList

pluginRequests = [
    regexWordList.requests,
    ]

def initialise():
    port = 12345

    settings = {
        "debug": False,
        "cookie_secret": "123",
        "autoreload": False,
    }

    # Flatten the list of lists of pageRequests
    pageList = [request for pluginRequest in pluginRequests for request in pluginRequest]

    application = tornado.web.Application(pageList, **settings)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    initialise()