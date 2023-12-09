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

def getAfter(messageList, word):
    return messageList[getWordIndex(messageList, word)+1:]

def main():
    try:
        vp.say("activated")
        while True:
            word, keyword = l.listen()
            wordList = word.split()

            if keyword and l.isKeyword(WAKE_WORD):
                query = " ".join(getAfter(wordList, WAKE_WORD))
                if not query:
                    vp.say("woof woof")
                    query, keyword = l.listen()
                    if not query:
                        continue

                queryList = query.split()

                if l.isKeyword("play"):
                    if len(queryList) == 1:
                        vp.play()
                    else:
                        vp.setVid(''.join(getAfter(queryList, "say")))
                        vp.play()
                elif l.isKeyword("pause"):
                    vp.pause()
                elif l.isKeyword("say"):
                    vp.say(''.join(getAfter(queryList, "say")))
                
                elif isWord(query):
                    s.command(['k' + longToShort(query), .1])
    except Exception as e:
        s.exit()
        raise e

if __name__ == "__main__":
    main()

s.exit()