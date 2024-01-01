import socket, pickle

class Brain:
    def __init__(self, s: socket.socket):
        self.s = s
    def think(self, prompt:str, *args, **kwargs):
        self.s.send(pickle.dumps([prompt, args, kwargs]))
        return pickle.loads(self.s.recv(1024))