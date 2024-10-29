"""
This file contains the code for the voice controller.
"""

import logging
import pyttsx3
import speech_recognition as sr

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)


def check_microphone():
    """
    Check and return the list of available microphones.
    """
    return sr.Microphone().list_microphone_names()


def listen(llm):
    """
    Listen for audio input from the microphone and use Whisper model to recognize speech.

    Args:
    llm: The language model to process the input.

    Returns:
    str: The recognized text from the speech input.
    """
    try:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            logger.info("Listening...")
            r.adjust_for_ambient_noise(source, duration=5)
            logger.info("Okay, I'm listening now.")

            while True:
                audio = r.listen(source, timeout=5, phrase_time_limit=30)
                logger.info("Got it! Now to recognize it...")

                # Recognize speech using Whisper
                try:
                    result = r.recognize_whisper(
                        audio, model="medium.en", show_dict=True
                    )
                    text = result["text"]  # Extract recognized text
                    logger.info(f"Recognized: {text}")
                    return text
                except sr.UnknownValueError:
                    logger.warning("Whisper could not understand the audio.")
                    return "Sorry, I did not catch that."
                except sr.RequestError as e:
                    logger.error(f"Could not request results from Whisper; {e}")
                    return "Error in recognizing speech."

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        engine.say("An error occurred. Please try again.")
        engine.runAndWait()


# Example usage:
# llm_instance = some_llm_function()
# listen(llm_instance)
