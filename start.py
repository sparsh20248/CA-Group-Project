class Port:
    inp = []
    output = []

    def __init__(self, name, port):
        self.name = name
        self.port = port

    def get_input(self):
        return self.inp
    def get_output(self):
        return self.output

class Router:

    def __init__(self, name):
        self.name = name
        self.Port = Port("port_north", direction)

