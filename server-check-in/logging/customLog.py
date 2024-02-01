import logging
import logging.config
import json
import logging.handlers
import pathlib
import colorlog 



def configure_logging(stdout_enabled=True, file_enabled=True, config='logging_config.json'):
    # Load the JSON configuration
    with open('logging_config.json', 'r') as config_file:
        logging_config = json.load(config_file)

    # Disable or enable stdout and file handlers based on the provided arguments
    handlers = []
    if stdout_enabled:
        handlers.append("stderr")
        handlers.append("stdout_info_debug")
    if file_enabled:
        handlers.append("file")

    # Update the handlers in the root logger
    logging_config["loggers"]["root"]["handlers"] = handlers

    # Configure logging using dictConfig
    logging.config.dictConfig(logging_config)

# Set up the custom SUCCESS log level
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

def success(self, message, *args, **kwargs):
    self.log(SUCCESS, message, *args, **kwargs)

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
        logger.critical(f"recieved the follow exception: {e.args[0]}")
        
        
        
        
        
if __name__ == "__main__":
    test_logger()