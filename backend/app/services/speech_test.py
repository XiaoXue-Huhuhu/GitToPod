from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import os

# Load environment variables
load_dotenv()

class AzureSpeechService:
    def __init__(self):
        # Load Azure Speech API key and region
        self.speech_key = os.environ.get("SPEECH_KEY")
        self.speech_region = os.environ.get("SPEECH_REGION")

        if not self.speech_key or not self.speech_region:
            raise ValueError("SPEECH_KEY or SPEECH_REGION is missing in .env file!")

        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.speech_region)
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    def text_to_speech(self, text: str):
        # Create a speech synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

        # Perform speech synthesis (speak the text)
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Successfully synthesized the text to speech!")
        elif result.reason == speechsdk.ResultReason.Canceled:
            print("Speech synthesis failed: ", result.cancellation_details.reason)
            print("Details: ", result.cancellation_details.error_details)

if __name__ == "__main__":
    # Example text
    text_to_convert = "Hello, this is a test of Azure's text to speech service."
    
    # Create instance of the speech service
    azure_service = AzureSpeechService()

    # Convert text to speech
    azure_service.text_to_speech(text_to_convert)
