import logging
import json
import sys
import os
from pathlib import Path

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        if hasattr(record, 'extra'):
            log_obj.update(record.extra)
            
        return json.dumps(log_obj)


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("pdf_chat_api")
    logger.setLevel(logging.DEBUG)
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    console_handler.setLevel(logging.INFO)
    
    # File handler with JSON formatting
    log_file = log_dir / "app.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(JSONFormatter())
    file_handler.setLevel(logging.DEBUG)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()