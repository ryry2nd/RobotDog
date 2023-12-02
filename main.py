from servos import keepCheckingPort, connectPort, send, closeAllSerial
from speakAndSpell import VideoPlayer, Listen
import threading, os

vp = VideoPlayer()
l = Listen()

def main():
    while True:
        print(l.listen())
    try:
        goodPorts = {}
        connectPort(goodPorts)
        t = threading.Thread(target=keepCheckingPort, args=(goodPorts,))
        t.start()

        send(goodPorts, ['g',0.1])
        send(goodPorts, ['z',0.1])
        
        while True:
            s = input(">")
            if (s == 'q'):
                break
            send(goodPorts, ["k"+s, 0])

        closeAllSerial(goodPorts)
    except Exception as e:
        print(e)
        closeAllSerial(goodPorts)
        os._exit(0)

if __name__ == "__main__":
    main()