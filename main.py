from aiVoice import AiVoice
from think import Brain
from dotenv import load_dotenv
import os, socket, pickle, sys, threading

load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_PATH = os.getenv('MODEL_PATH')
VOICE_PATH = os.getenv('VOICE_PATH')
GPT_DEVICE = os.getenv("GPT_DEVICE")
PORT = int(os.getenv("PORT"))

s = socket.socket()

def clientThread(c: socket.socket):
    try:
        b = Brain(MODEL_NAME, MODEL_PATH, pickle.loads(c.recv(4096)), device=GPT_DEVICE)
        voice = AiVoice(VOICE_PATH)

        with b.session():
            while True:
                data = pickle.loads(c.recv(1024))
                
                if data == 'exit':
                    c.close()
                    break
                if data[0]:
                    send = pickle.dumps(b.think(data[1], data[2], data[3]))
                else:
                    send = pickle.dumps(voice.generateVoice(data[1], data[2]))
                
                c.send(sys.getsizeof(send))
                c.send(send)
    except Exception as e:
        c.send(e)
        c.close()

threads = []

def main():
    s.bind(('', PORT))
    s.listen(5)

    while True:
        c, addr = s.accept()
        threads.append(threading.Thread(target=clientThread, args=(c, )))

if __name__ == "__main__":
    main()