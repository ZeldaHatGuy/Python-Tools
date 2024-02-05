import logging
import logging.config
import json
import logging.handlers
import colorlog 
import datetime as dt
import atexit
import inspect

'''
Orginal Concept from Mcoding with a few added features such as
Turning off/on file and stdout handlers
Adding the Success log level
Taking in custom config from the user
Mcoding video can be found here: https://www.youtube.com/watch?v=9L77QExPmI0
'''

logger = logging.getLogger(__name__)


def configure_logging(stdout_enabled=True, file_enabled=True, config='logging_config.json'):
    # Load the JSON configuration
    with open('logging_config.json', 'r') as config_file:
        logging_config = json.load(config_file)
        


    # Disable or enable stdout and file handlers based on the provided arguments
    handlers = []
    if stdout_enabled:
        # handlers.append("stderr")
        handlers.append("stdout_info_debug")
    if file_enabled:
        handlers.append("file")

    # Update the handlers in the root logger
    logging_config["loggers"]["root"]["handlers"] = handlers

    # Configure logging using dictConfig
    logging.config.dictConfig(logging_config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

# Set up the custom SUCCESS log level
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")


    
def success(self, message, *args, **kwargs):
    # Get the calling function's name
    calling_function = inspect.currentframe().f_back.f_globals.get('__name__')
    
    # Include the calling function's name in the log message
    message_with_function = f"{calling_function}: {message}"
    
    # Log the message
    self._log(SUCCESS, message_with_function, args, **kwargs)

# Add the success method to the Logger class
logging.Logger.success = success

    
    
def test_logger():

    configure_logging()

 
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    logger.success("Good to go!")
    
    try:
        1 / 0
    except ZeroDivisionError as e:
        logger.critical(f"Recieved the Following Exception: {e.args[0]}")
        
        
        
        
        
if __name__ == "__main__":
    test_logger()