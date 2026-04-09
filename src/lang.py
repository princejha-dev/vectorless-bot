from langdetect import detect
from googletrans import Translator

class LangFeature:
    def __int__(self):
        pass

    def detect_lang(self,text):
        try:
            return detect(text)
        except:
            return "en"
        
    def translate_to_english(self,text):
        return Translator.translate(text,dest="en").text
    
    def get_language_instructions(self,lang):
        if self.lang =="hi":
            return "Answer in Hindi (use simple Hinglish Or Pure Hindi)"
        elif self.lang == "mr":
           return "Answer in Marathi (use conversational marathi)"
        else:
            return "Answer in English"
