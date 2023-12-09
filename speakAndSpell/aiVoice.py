from tortoise import utils
from tortoise.api import TextToSpeech
import os, vlc, torchaudio

VOICE_PATH = os.path.join("speakAndSpell", "voiceLines")
CACHE_PATH = os.path.join("speakAndSpell", "cache")

BAD_CHARS = list("\\/*:?\"\'<>|\n\r\t\b\f")

class AiVoice:
    def __init__(self, vlc_instance:vlc.Instance, player:vlc.MediaPlayer):
        self.player = player
        self.vlc_instance = vlc_instance

        clips_paths = [os.path.join(VOICE_PATH, i) for i in os.listdir(VOICE_PATH)]
        self.reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]

        self.tts = TextToSpeech(kv_cache=True, half=True)#, use_deepspeed=True)
    
    def convert_to_better_text(self, text):
        return ''.join(i for i in text.lower() if not i in BAD_CHARS)

    def generateVoice(self, text):
        text = self.convert_to_better_text(text)
        path = os.path.join(CACHE_PATH, text + '.wav')

        if not os.path.exists(path):
            pcm_audio = self.tts.tts_with_preset(text, voice_samples=self.reference_clips, preset="ultra_fast")
            torchaudio.save(path, pcm_audio.squeeze(0).cpu(), 24000)
        
        return path