# from servos import Servos, longToShort, isWord
from speakAndSpell import VideoPlayer, Listen
from dotenv import load_dotenv
from brain import Brain
import os

load_dotenv()

INIT_PROMPT = """You are a tiny robot dog named Kevin that your creator built from a kit and then he hacked it by slapping a raspberry pi on the board that normally controls you and used the api for the kit to use your limbs.
Your mind is a chatGPT clone called GPT4All.
You are entirely coded in python because it has all of the libraries you need.
Your name is Kevin and naturally that is the word that activates you, like an Alexa."""

MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_PATH = os.getenv('MODEL_PATH')
WAKE_WORD = os.getenv("WAKE_WORD").lower()
GPT_DEVICE = os.getenv("GPT_DEVICE")

vp = VideoPlayer()
l = Listen()
# s = Servos(['g', 0], ['z', 0])
b = Brain(MODEL_NAME, MODEL_PATH, INIT_PROMPT, device=GPT_DEVICE)

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
            vp.say("activated", True)
            while True:
                query, keyword = l.listen()

                if keyword and l.isKeyword(WAKE_WORD):
                    if query == WAKE_WORD:
                        vp.say("woof woof")
                        query, keyword = l.listen()
                        if not query:
                            continue

                    queryList = query.split()
                    if l.isKeyword("stop", "pause"):
                        vp.stop()
                    elif l.isKeyword("play"):
                        if len(queryList) == 1:
                            vp.play()
                        else:
                            vp.setVid(''.join(getAfter(queryList, "say")))
                            vp.play()
                    # elif isWord(query):
                    #     s.command(['k' + longToShort(query), .1])
                    else:
                        gen = b.think(query, streaming=True)
                        text = ""
                        for i in gen:
                            print(i, end='')
                            text += i
                        print()
                        vp.say(text)
    except Exception as e:
        # s.exit()
        raise e

if __name__ == "__main__":
    main()

# s.exit()