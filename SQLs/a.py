import logging

# Step 1: Set up the logging format and configuration
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

# Step 2: Create a custom logger
logger = logging.getLogger("MyCustomLogger")

# Example usage of the logger
logger.info("This is an info message from MyCustomLogger.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
