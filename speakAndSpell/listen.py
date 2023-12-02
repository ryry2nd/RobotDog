from speech_recognition.exceptions import UnknownValueError
from rake_nltk import Rake
import speech_recognition as sr


class Listen:
    def __init__(self):
        self.rec = sr.Recognizer()
        self.keyword = Rake()

    def listen(self):
        with sr.Microphone() as source:
            self.rec.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)

        try:
            query = self.rec.recognize_google(audio, language="en-in")
        except UnknownValueError:
            return ""

        return query
    
    def isKeyword(self, str):
        for i in self.keyword.get_ranked_phrases():
            if str in i.split():
                return True
        
        return False