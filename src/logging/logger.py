import os
import logging
import structlog
from pathlib import Path
from datetime import datetime

class CustomLogger:
      
    """
    Logger for offline ML training pipelines.
    Creates a new log file for every training run.
    """
    _configured = False 
    def __init__(self,log_dir:str="ml_logs",log_type:str="training",log_level :int = logging.INFO):
        self.log_dir = Path.cwd()/log_dir/log_type
        self.log_dir.mkdir(parents=True,exist_ok=True)


        self.log_file_path =self.log_dir/f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

        self.log_level = log_level

        self._configure()

    def _configure(self):
        if CustomLogger._configured:
            return
        

        formatter = logging.Formatter("%(message)s")
        file_handler = logging.FileHandler(self.log_file_path,encoding="utf-8")
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        
        logging.basicConfig(
            level=self.log_level,
            format ="%(message)s",
            handlers=[console_handler,file_handler]
        )


        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="%m_%d_%Y_%H_%M_%S"),
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class = structlog.stdlib.BoundLogger,
            logger_factory = structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use =True,
        )

        CustomLogger._configured = True
    
    def get_logger(self,name:str):
        return structlog.get_logger(name)
                    


