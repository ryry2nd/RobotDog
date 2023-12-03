from servos.ardSerial import keepCheckingPort, connectPort, send, closeAllSerial
from servos.TerminateThread import StoppableThread

class Servos:
    def __init__(self, *send):
        self.goodPorts = {}
        connectPort(self.goodPorts)
        self.t = StoppableThread(target=keepCheckingPort, args=(self.goodPorts,))
        self.t.start()

        self.command(*send)
    
    def command(self, *command, timeout: int = 0):
        ret = []
        for i in command:
            ret.append(send(self.goodPorts, i, timeout))
        
        return ret
    
    def exit(self):
        closeAllSerial(self.goodPorts)
        self.t.stop()
        del self