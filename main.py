from creditcard.components.data_ingestion import DataIngestion
from creditcard.components.data_validation import DataValidation
from creditcard.exception.exception import CreditCardException
from creditcard.logging.logger import logging
from creditcard.entity.config_entity import DataIngestionConfig, DataValidationConfig
from creditcard.entity.config_entity import TrainingPipelineConfig


import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Intializing Data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(dataingestionartifact)
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Intiate the Data Validation")
        data_validation_artifact = data_validation.initaite_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)

    except Exception as e:
        logging.error(e,sys)

