from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(subscription=ai_key, region=ai_region)
        translation_config.speech_recognition_language = "en-US"
        translation_config.add_target_language('fr')
        translation_config.add_target_language('de')
        translation_config.add_target_language('pt')
        print(f"Ready to translate from {translation_config.speech_recognition_language}")


        # Configure speech
        speech_config = speech_sdk.SpeechConfig(subscription=ai_key, region=ai_region)

        # Get user input
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n fr = French\n de = German\n pt = Portuguese\n Enter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'
                

    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''

    # Translate speech
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translation_recognizer = speech_sdk.translation.TranslationRecognizer(translation_config=translation_config, audio_config=audio_config)
    print("Speak now...")
    translation_result: speech_sdk.translation.TranslationRecognitionResult = translation_recognizer.recognize_once_async().get()
    print(f"Translating {translation_result.text} into {targetLanguage}...")
    if translation_result.reason == speech_sdk.ResultReason.TranslatedSpeech:
        translation = translation_result.translations[targetLanguage]
        print(translation)
    else:
        print(translation_result.reason)
        if translation_result.reason == speech_sdk.ResultReason.Canceled:
            cancellation = translation_result.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)
    

    # Synthesize translation
    voices = {
        "fr": "fr-FR-HenriNeural",
        "de": "de-DE-MajaNeural",
        "pt": "pt-PT-RaquelNeural"
    }
    speech_config.speech_synthesis_voice_name = voices[targetLanguage]
    speech_synthetizer = speech_sdk.speech.SpeechSynthesizer(speech_config=speech_config)
    speak: speech_sdk.SpeechSynthesisResult = speech_synthetizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
        

if __name__ == "__main__":
    main()