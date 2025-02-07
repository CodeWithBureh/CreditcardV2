from creditcard.components.data_ingestion import DataIngestion
from creditcard.exception.exception import CreditCardException
from creditcard.logging.logger import logging
from creditcard.entity.config_entity import DataIngestionConfig
from creditcard.entity.config_entity import TrainingPipelineConfig


import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Intializing Data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)

    except Exception as e:
        logging.error(e,sys)

