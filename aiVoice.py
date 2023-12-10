from tortoise import utils
from tortoise.api import TextToSpeech
import os

class AiVoice:
    def __init__(self, voice_path:str):
        self.voice_path = voice_path
        clips_paths = [os.path.join(self.voice_path, i) for i in os.listdir(self.voice_path)]
        self.reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]
        self.tts = TextToSpeech(kv_cache=True, half=True)#, use_deepspeed=True)

    def generateVoice(self, text, quality="ultra_fast"):
        return self.tts.tts_with_preset(text, voice_samples=self.reference_clips, preset=quality)