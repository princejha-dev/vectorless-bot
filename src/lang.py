from langdetect import detect
from deep_translator import GoogleTranslator

class LanguageFeature:
    def __int__(self):
        pass

    def detect_lang(self,text:str)->str:
        """Takes User query and Detects the language"""
        try:
            return detect(text)
        except:
            return "en"
        
    def translate_to_english(self,text:str)->str:
        """Translates text to English using deep-translator"""
        try:
            translator = GoogleTranslator(source='auto', target='en')
            return translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails
    
    def get_language_instructions(self,lang):
        if lang =="hi":
            return "Answer in Hindi (use simple Hinglish Or Pure Hindi)"
        elif lang == "mr":
            return "Answer in Marathi (use conversational marathi)"
        elif lang == "ta":
            return "Answer in Tamil (use conversational Tamil)"
        elif lang == "gu":
            return "Answer in Gujarati (use conversational Gujarati)"
        else:
            return "Answer in English"
        
Langobj=LanguageFeature()
