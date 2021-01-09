import importlib
import os
import typing

import tornado.ioloop
import tornado.web

pluginRequests: typing.List[typing.Tuple[typing.Any]] = []
indexItems: typing.List[str] = []

class indexHandler(tornado.web.RequestHandler):
    def get(self):
        # This should probably be a full template, but don't bother for now
        fullIndex = "<br /><br />".join(indexItems)
        self.write(fullIndex)

def initialise():
    port = 12345

    settings = {
        "debug": False,
        "cookie_secret": "123",
        "autoreload": False,
    }

    # Flatten the list of lists of pageRequests
    pageList = [request for request in pluginRequests]
    pageList.append(("/", indexHandler))

    application = tornado.web.Application(pageList, **settings)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

def loadPlugin(moduleName):
    plugin = importlib.import_module("plugins.%s"%(moduleName))
    if hasattr(plugin, "requests"):
        pluginRequests.extend(plugin.requests)
    else:
        print("Warning: plugin %s had no requests to import"%(moduleName))
    if hasattr(plugin, "indexItems"):
        indexItems.extend(plugin.indexItems)

def loadPlugins():
    for pluginName in os.listdir("plugins"):
        if pluginName.startswith(".") or pluginName.startswith("_"):
            continue
        if os.path.isdir(os.path.join("plugins", pluginName)):
            loadPlugin(pluginName)
        elif pluginName.endswith(".py"):
            loadPlugin(pluginName[:-3])
        else:
            print("Warning: unknown file in plugin dir: %s"%(pluginName))

if __name__ == "__main__":
    loadPlugins()
    initialise()