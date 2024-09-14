from utils import *
from imports import *
from config import *


def listen(llm):
    try:
        r = sr.Recognizer()

        def callback(indata, frames, time, status):
            pass
        with sr.Microphone() as source:
            logger.info("Listening...")
            r.adjust_for_ambient_noise(source, duration=5)

            logger.info("Okay, I'm listening now.")

            while 1:
                text = ""
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=30)
                    logger.info("Got it! Now to recognize it...")

                    text = r.recognize_whisper(
                        audio,
                        model="medium.en",
                        show_dict=True
                    )["text"] # This is the text that was recognized

                    logger.info(f"Recognized: {text}")
                except Exception as e:
                    logger.error(f"Error in listen: {e} at line {sys.exc_info()[-1].tb_lineno}")
                    raise e
                
                response_text = llm.predict(human_input=text)
                logger.info(f"Response: {response_text}")
                engine.say(response_text)
                engine.runAndWait()

    except Exception as e:
        logger.error(f"Error in listen: {e} at line {sys.exc_info()[-1].tb_lineno}")
        raise e
        
