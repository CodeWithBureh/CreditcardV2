import os
import sys
import numpy as np
import pandas as pd

"""
Defining common constant variables for the training pipeline
"""
TARGET_COLUMN:str = "Class"
PIPELINE_NAME:str = "CreditCard"
ARTIFACTS_DIR:str = "Artifacts"
FILE_NAME:str = "credit_card.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"


"""
Data Ingestion related constants start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME:str = "creditcard_data"
DATA_INGESTION_DATABASE_NAME:str = "akinolaanderson"
DATA_INGESTION_DIR_NAME:str = "Credit_Card_Data"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float = 0.2


# DATA_INGESTION_FILE_PATH:str = "Credit_Card_Data/credit_card.csv"

