from servos import Servos, longToShort, isWord
from speakAndSpell import VideoPlayer, Listen

vp = VideoPlayer()
l = Listen()
s = Servos(['g', 0], ['z', 0])

def main():
    try:
        while True:
            word, keyword = l.listen()

            if isWord(word):
                s.command(['k' + longToShort(word), .1])

    except KeyboardInterrupt:
        return
    except Exception as e:
        s.exit()
        raise e

if __name__ == "__main__":
    main()

s.exit()