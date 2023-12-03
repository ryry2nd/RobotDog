from servos import Servos, longToShort, isWord
from speakAndSpell import VideoPlayer, Listen

WAKE_WORD = "dog"

vp = VideoPlayer()
l = Listen()
s = Servos(['g', 0], ['z', 0])

def getWordIndex(messageList, word):
    for i in range(len(messageList)):
        if messageList[i] == word:
            return i
    
    return -1

def main():
    try:
        while True:
            word, keyword = l.listen()
            wordList = word.split()

            if keyword and l.isKeyword(WAKE_WORD):
                query = " ".join(wordList[getWordIndex(wordList, WAKE_WORD)+1:])
                if not query:
                    vp.say("woof woof")
                    query, keyword = l.listen()
                    if not query:
                        continue

                if isWord(query):
                    s.command(['k' + longToShort(query), .1])

    except KeyboardInterrupt:
        return
    except Exception as e:
        s.exit()
        raise e

if __name__ == "__main__":
    main()

s.exit()