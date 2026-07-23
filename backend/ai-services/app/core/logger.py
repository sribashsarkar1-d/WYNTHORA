import logging
import json
import os
from datetime import datetime

LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../logs"))
os.makedirs(LOGS_DIR, exist_ok=True)

class JSONFormatter(logging.Formatter):
    """
    Structured JSON Formatter for Enterprise Observability.
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    Creates a structured JSON logger writing to a specific file in the logs/ directory.
    Example: setup_logger("IngestionManager", "ingestion.log")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers if setup_logger is called multiple times for the same name
    if not logger.handlers:
        filepath = os.path.join(LOGS_DIR, log_file)
        
        # File handler for JSON logs
        file_handler = logging.FileHandler(filepath, encoding='utf-8')
        file_handler.setFormatter(JSONFormatter())
        
        # Console handler for development visibility (standard format)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger
