from servos import Servos
from speakAndSpell import VideoPlayer, Listen
from TerminateThread import StoppableThread

vp = VideoPlayer()
l = Listen()
s = Servos(['g', .1], ['z', .1])


def main():
    try:
        while True:
            word = l.listen()
            

    except KeyboardInterrupt:
        return
    except Exception as e:
        s.exit()
        raise e

if __name__ == "__main__":
    main()

s.exit()