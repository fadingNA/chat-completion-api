import speech_recognition as sr
import logging

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_speech_recognition():
    try:
        r = sr.Recognizer()

        # If you have multiple microphones, specify the device_index
        # For example, to use the microphone with index 1:
        # with sr.Microphone(device_index=1) as source:
        with sr.Microphone() as source:
            logger.info("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            logger.info("Please say something...")

            audio = r.listen(source)
            logger.info("Recording complete. Recognizing speech...")

            # Whisper from openAI can understand multiple languages
            text = r.recognize_whisper(
                audio,
                model="medium",
                language="th",
                show_dict=True
            )["text"]
            logger.info(f"Transcribed Text: {text}")

    except sr.UnknownValueError:
        logger.error("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        logger.error(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        logger.error(f"Error in test_speech_recognition: {e}")

if __name__ == '__main__':
    test_speech_recognition()