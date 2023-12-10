import os, socket, pickle, torchaudio

BAD_CHARS = list("\\/*:?\"\'<>|\n\r\t\b\f")

class AiVoice:
    def __init__(self, s: socket.socket, cache_path:str):
        self.cache_path = cache_path
        self.s = s
    
    def convert_to_better_text(self, text):
        return ''.join(i for i in text.lower() if not i in BAD_CHARS)

    def generateVoice(self, text, quality="ultra_fast"):
        text = self.convert_to_better_text(text)
        path = os.path.join(self.cache_path, text + '.wav')

        if not os.path.exists(path):
            self.s.send(pickle.dumps([False, text, quality]))
            pcm_audio = pickle.loads(self.s.recv(pickle.loads(self.s.recv(256))))
            torchaudio.save(path, pcm_audio.squeeze(0).cpu(), 24000)
        
        return path