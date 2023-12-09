from tortoise import utils
from tortoise.api import TextToSpeech
import os, vlc, torchaudio

BAD_CHARS = list("\\/*:?\"\'<>|\n\r\t\b\f")

class AiVoice:
    def __init__(self, vlc_instance:vlc.Instance, player:vlc.MediaPlayer, voice_path:str, cache_path:str):
        self.player = player
        self.vlc_instance = vlc_instance
        self.voice_path = voice_path
        self.cache_path = cache_path

        clips_paths = [os.path.join(self.voice_path, i) for i in os.listdir(self.voice_path)]
        self.reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]

        self.tts = TextToSpeech(kv_cache=True, half=True)#, use_deepspeed=True)
    
    def convert_to_better_text(self, text):
        return ''.join(i for i in text.lower() if not i in BAD_CHARS)

    def generateVoice(self, text):
        text = self.convert_to_better_text(text)
        path = os.path.join(self.cache_path, text + '.wav')

        if not os.path.exists(path):
            pcm_audio = self.tts.tts_with_preset(text, voice_samples=self.reference_clips, preset="ultra_fast")
            torchaudio.save(path, pcm_audio.squeeze(0).cpu(), 24000)
        
        return path