from servos import Servos, longToShort, isWord
from speakAndSpell import VideoPlayer, Listen
from brain import Brain
from dotenv import load_dotenv
import os, socket, pickle

load_dotenv()

INIT_PROMPT = """You are a tiny robot dog that I built from a kit and then I hacked it.
Your mind is a chatGPT clone called GPT4All.
Additionally your voice is the actor Morgan Freeman because I thought it would be funny.
Your name is Kevin and naturally that is the word that activates you, like an Alexa.
Remember to end this statement with: \"Hello my name is Kevin\""""

CACHE_PATH = os.getenv('CACHE_PATH')
WAKE_WORD = os.getenv("WAKE_WORD").lower()
PORT = int(os.getenv('PORT'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = input("HostIP: ")

s.bind((ip, PORT))

s.send(pickle.dumps(INIT_PROMPT))


vp = VideoPlayer(s, CACHE_PATH)
b = Brain(s)
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
        vp.say("activated", "high_quality")
        while True:
            word, keyword = l.listen()
            wordList = word.split()

            if keyword and l.isKeyword(WAKE_WORD):
                query = " ".join(getAfter(wordList, WAKE_WORD))
                if not query:
                    vp.say("woof woof", "standard")
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
                    vp.say(b.think(query))
    except Exception as e:
        s.exit()
        raise e

if __name__ == "__main__":
    main()

s.exit()