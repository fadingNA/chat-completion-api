import speech_recognition as sr
import logging

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def check_microphone():
    try:
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            logger.info(
                f"Microphone with name '{name}' found for `Microphone(device_index={index})`")
    except Exception as e:
        logger.error(
            f"Error in check_microphone: {e} at line {sys.exc_info()[-1].tb_lineno}")
        raise e

if __name__ == '__main__':
    check_microphone()