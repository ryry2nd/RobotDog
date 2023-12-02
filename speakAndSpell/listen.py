from speech_recognition.exceptions import UnknownValueError
from rake_nltk import Rake
import speech_recognition as sr

class Listen:
    def __init__(self):
        self.rec = sr.Recognizer()
        self.keyword = Rake()
        self.word = ""

    def listen(self):
        with sr.Microphone() as source:
            self.rec.adjust_for_ambient_noise(source)
            audio = self.rec.listen(source)

        try:
            query = self.rec.recognize_google(audio, language="en-in")
        except UnknownValueError:
            return "", ""
        
        self.keyword.extract_keywords_from_text(query)
        self.word = query.lower()
        return query, self.getKeywords()
    
    def isKeyword(self, str):
        for i in self.keyword.get_ranked_phrases():
            if str in i.split():
                return True
        
        return False
    
    def getKeywords(self):
        return self.keyword.get_ranked_phrases()
    
    def getWord(self):
        return self.word