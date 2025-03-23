import logging
import os

def setup_logging(log_file='application.log', level=logging.INFO):
    """Configure logging settings for the application."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        filename=log_file,
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging is set up.")