from creditcard.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_TRAINER_TRAINED_MODEL_NAME

import os, sys

from creditcard.exception.exception import CreditCardException
from creditcard.logging.logger import logging

class CreditCardModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise CreditCardException(e,sys)

    def predict(self, x):
        try:
            x_transform = self.preprocessor.tranform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise CreditCardException(e,sys)

