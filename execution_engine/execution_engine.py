class ExecuteEngine:
    def __init__(self, config):
        self.config = config

        self.wifi_interfaces = []
        self.eth_interfaces = []
        self.namespaces = []
        self.clients = []

    def Execute(self):
        workflow = self.config.get(workflow)