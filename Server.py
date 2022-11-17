from App import App


class Server:

    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port

    def startAPI(self, apiPort):
        self.api = App()
        self.api.injectNode(self)
        self.api.start(apiPort)

