from datetime import datetime
import logging
from pathlib import Path


# Logging is tested via other tests
def create_logger(log_folder_path: Path | str) -> logging.Logger:
    logger = logging.getLogger(__name__)

    # Prepare file handler, first generate a name for the log file based on the time
    formatted_current_time = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
    filename = f"wtldr_log_{formatted_current_time}.log"

    # Create file handler
    file_handler = logging.FileHandler(Path(log_folder_path) / filename)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger.setLevel(logging.INFO)

    logger.addHandler(file_handler)

    return logger
