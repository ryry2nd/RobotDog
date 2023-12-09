from servos import Servos, longToShort, isWord
from speakAndSpell import VideoPlayer, Listen
from dotenv import load_dotenv
from brain import Brain
import os

load_dotenv()

INIT_PROMPT = os.getenv('INIT_PROMPT')
MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_PATH = os.getenv('MODEL_PATH')
VOICE_PATH = os.getenv('VOICE_PATH')
CACHE_PATH = os.getenv('CACHE_PATH')
WAKE_WORD = os.getenv("WAKE_WORD").lower()

vp = VideoPlayer(VOICE_PATH, CACHE_PATH)
l = Listen()
s = Servos(['g', 0], ['z', 0])
b = Brain(MODEL_NAME, MODEL_PATH, INIT_PROMPT)

def getWordIndex(messageList, word):
    for i in range(len(messageList)):
        if messageList[i] == word:
            return i
    
    return -1

def getAfter(messageList, word):
    return messageList[getWordIndex(messageList, word)+1:]

def main():
    try:
        with b.session():
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
                    elif isWord(query):
                        s.command(['k' + longToShort(query), .1])
                    else:
                        vp.say(b.think(queryList))
    except Exception as e:
        s.exit()
        raise e

if __name__ == "__main__":
    main()

s.exit()