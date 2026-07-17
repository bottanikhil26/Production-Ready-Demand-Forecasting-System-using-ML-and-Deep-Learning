import sys

from pathlib import Path



class AppException(Exception):
    """
    Base Exception for the entire project.

    Captures:
            - filename
            - function name
            - line number
            - original error message
            - type of error message
    """

    def __init__(self,
                 error_message : BaseException | str,
                 error_details : object | None = None,
                 ):
        super().__init__(str(error_message))

        if error_details is None:
            _,_, exc_tb = sys.exc_info()

        elif hasattr(error_details,"exc_info"):
            _ ,_ , exc_tb = error_details.exc_info()
        
        elif isinstance(error_details,BaseException):
            exc_tb = error_details.__traceback__
        
        else:
            _ ,_ , exc_tb = sys.exc_info()


        if exc_tb :

            while exc_tb.tb_next:
                exc_tb = exc_tb.tb_next
            
            self.file_name = Path(exc_tb.tb_frame.f_code.co_filename).name
            self.function_name = exc_tb.tb_frame.f_code.co_name
            self.line_number = exc_tb.tb_lineno
        

        else:
            self.file_name = "Unknown"
            self.function_name ="Unknown"
            self.line_number = -1
        
        self.error_message = str(error_message)

        self.exception_type = (
            type(error_message).__name__
            if isinstance(error_message,BaseException)
            else "UnknownException"
        )
    
    def __str__(self):

        return (
            f"Type : {self.exception_type}\n"
            f"Error Message : {self.error_message}\n"
            f"File :{self.file_name}\n"
            f"Function :{self.function_name}\n"
            f"Line :{self.line_number}"
            )
    
    def to_dict(self):
        return {
            "exception_type": self.exception_type,
            "file": self.file_name,
            "function": self.function_name,
            "line": self.line_number,
            "message": self.error_message,
        }

