import yaml
from creditcard.exception.exception import CreditCardException
from creditcard.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, "rb") as yaml_file:
            data = yaml.safe_load(yaml_file)
        return data
    except Exception as e:
        raise CreditCardException(e,sys)

def write_yaml_file(file_path:str,content:object , replace:bool = False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CreditCardException(e,sys)
    
def save_numpy_array(file_path:str, array:np.ndarray):
    """
    Save numpy array to file
    file_path: str: location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array) 
    except Exception as e:
        raise CreditCardException(e,sys)

def save_object(file_path:str , obj: object) -> None:
    try:
        logging.info(f"Entered the save_object method of Main Utils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file) 
        logging.info("Exited the save_object method of Main Utils class")
    except Exception as e:
        raise CreditCardException(e,sys)

