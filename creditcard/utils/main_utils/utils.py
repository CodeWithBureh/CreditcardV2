import yaml
from creditcard.exception.exception import CreditCardException
from creditcard.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle
from sklearn.model_selection import GridSearchCV


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

def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise CreditCardException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CreditCardException(e,sys) from e


def evaluate_models(x_train, y_train, x_test, y_test , models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred = model.predict(x_train)

            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

            return report
        
    except Exception as e:
        raise CreditCardException(e,sys)


