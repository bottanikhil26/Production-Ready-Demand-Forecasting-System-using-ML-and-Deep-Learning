import os
import logging
import structlog
from pathlib import Path
from datetime import datetime

class CustomLogger:
    _configured = False   
    """
    Logger for offline ML training pipelines.
    Creates a new log file for every training run.
    """
    def __init__(self,log_dir:str="ml_logs",log_type:str="Training",log_level :str = logging.INFO):
        self.log_dir = Path(log_dir)/log_type
        self.logs_dir = os.path.join(os.getcwd(),self.log_dir)
        os.makedirs(self.logs_dir,exist_ok=True)


        log_file =f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

        self.log_file_path = os.path.join(self.logs_dir,log_file)

        self.log_level = log_level

        self._configure()

    def _configure(self):
        if CustomLogger._configured:
            return
        

        formatter = logging.Formatter("%(message)s")
        file_handler = logging.FileHandler(self.log_file_path)
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
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.TimeStamper(fmt="%m_%d_%Y_%H_%M_%S"),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class = structlog.stdlib.BoundLogger,
            logger_factory = structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use =True,
        )

        CustomLogger._configured = True
    
    def get_logger(self,name:str):
        return structlog.get_logger(name)
                    


