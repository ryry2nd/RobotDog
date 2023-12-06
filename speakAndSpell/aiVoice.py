from tortoise import utils
from tortoise.api import TextToSpeech
import os, vlc

class AiVoice:
    def __init__(self, player:vlc.player, voicePath):
        self.player = player

        clips_paths = [os.path.join(voicePath, i) for i in os.listdir(voicePath)]

        self.reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]

        self.tts = TextToSpeech(kv_cache=True, half=True, )
    
    def say(self, text):
        pcm_audio = self.tts.tts_stream(text, voice_samples=self.reference_clips, preset="fast")

        self.player.set_media(vlc_instance.media_new(pcm_audio))
        self.player.play()