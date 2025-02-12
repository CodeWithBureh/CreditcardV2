from creditcard.components.data_ingestion import DataIngestion
from creditcard.components.data_validation import DataValidation
from creditcard.components.data_transformation import DataTransformation

from creditcard.exception.exception import CreditCardException
from creditcard.logging.logger import logging
from creditcard.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
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
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info("Data Transformation started")
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data Transformation completed")

    except Exception as e:
        logging.error(e,sys)

