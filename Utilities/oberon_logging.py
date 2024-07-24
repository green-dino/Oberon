import os
import time
import logging

# Constants for logging levels
LOG_DEBUG = 0
LOG_INFO = 1
LOG_WARN = 2
LOG_ERR = 3
LOG_CRIT = 4
LOG_OVERWRITE = True  # Set to True if log should be overwritten

SCRIPT_LOG = "./script.log"  # Define your log file path

# Initialize the forensic log
if LOG_OVERWRITE:
    # Remove the old log file if it exists
    if os.path.exists(SCRIPT_LOG):
        os.remove(SCRIPT_LOG)

try:
    # Initialize the log with level and message format
    logging.basicConfig(filename=SCRIPT_LOG,
                        format='%(levelname)s\t: %(message)s',
                        level=logging.DEBUG)
except Exception as e:
    # Handle initialization failure
    print("Failed to initialize Logging:", e)

# Function to get current time
def GetTime(timeStyle="UTC"):
    if timeStyle == 'UTC':
        return 'UTC Time: ' + time.asctime(time.gmtime(time.time()))
    else:
        return 'LOC Time: ' + time.asctime(time.localtime(time.time()))

# Function to log events based on type
def LogEvent(eventType, eventMessage):
    try:
        timeStr = GetTime('UTC')  # Get current UTC time
        formattedMessage = f"{timeStr}: {eventMessage}"  # Format log message

        if eventType == LOG_DEBUG:
            logging.debug(formattedMessage)
        elif eventType == LOG_INFO:
            logging.info(formattedMessage)
        elif eventType == LOG_WARN:
            logging.warning(formattedMessage)
        elif eventType == LOG_ERR:
            logging.error(formattedMessage)
        elif eventType == LOG_CRIT:
            logging.critical(formattedMessage)
        else:
            logging.info(formattedMessage)  # Default to info level if type is unknown

    except Exception as e:
        print("Event Logging Failed:", e)

# Example usage of LogEvent function
if __name__ == "__main__":
    # Print basic script information
    SCRIPT_NAME = "Logging Check"
    SCRIPT_VERSION = "1.0"
    SCRIPT_AUTHOR = "Oberon"

    # Log basic script information
    LogEvent(LOG_INFO, SCRIPT_NAME)
    LogEvent(LOG_INFO, SCRIPT_VERSION)
    LogEvent(LOG_INFO, "Script Started")

    # Perform some work (simulate with sleep)
    print("Performing Work")
    time.sleep(5)

    # Log events during script execution
    LogEvent(LOG_DEBUG, 'Test Debug')
    LogEvent(LOG_WARN, 'Test Warning')
    LogEvent(LOG_CRIT, 'Test Critical')
    LogEvent(LOG_INFO, 'Script Ended')

    # Print script end time
    utcTime = GetTime('UTC')
    print("Script Ended:", utcTime)
