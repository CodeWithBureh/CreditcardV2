import sys
from creditcard.logging import logger

class CreditCardException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _,_,tb = error_details.exc_info()

        self.line_number = tb.tb_lineno
        self.file_name = tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in python script name [{self.file_name}] line number [{self.line_number}]  error message [{self.error_message}]" #.format(self.file_name, self.line_number, str(self.error_message))
    
