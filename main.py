from think import Brain
from dotenv import load_dotenv
import os, socket, pickle, sys, threading

load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_PATH = os.getenv('MODEL_PATH')
GPT_DEVICE = os.getenv("GPT_DEVICE")
PORT = int(os.getenv("PORT"))

s = socket.socket()

def clientThread(c: socket.socket):
    try:
        b = Brain(MODEL_NAME, MODEL_PATH, pickle.loads(c.recv(4096)), device=GPT_DEVICE)

        with b.session():
            while True:
                data = pickle.loads(c.recv(1024))
                
                if data == 'exit':
                    c.close()
                    break
                c.send(pickle.dumps(b.think(data[1], data[2], data[3])))
    except Exception as e:
        c.send(e)
        c.close()

threads = []

def main():
    s.bind(('', PORT))
    s.listen(5)
    print("its working")

    while True:
        c, addr = s.accept()
        threads.append(threading.Thread(target=clientThread, args=(c, )))

if __name__ == "__main__":
    main()