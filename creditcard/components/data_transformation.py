import sys,os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from creditcard.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from creditcard.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact

from creditcard.entity.config_entity import DataTransformationConfig
from creditcard.exception.exception import CreditCardException
from creditcard.logging.logger import logging

from creditcard.utils.main_utils.utils import  save_numpy_array, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CreditCardException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame: 
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CreditCardException(e,sys) 
    
    def get_data_transformer_object(cls)->Pipeline:
        logging.info("Entered the get_data_transformer method of DataTransformation class")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processer:Pipeline = Pipeline([
                ("imputer",imputer)
            ])
            return processer
        except Exception as e:
            raise CreditCardException(e,sys)


    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered the initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting the data transformation process")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_train_df = train_df[TARGET_COLUMN]

            # testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_test_df = test_df[TARGET_COLUMN]

            preprocessor = self.get_data_transformer_object()

            preprocesser_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocesser_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocesser_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_test_df)]

            # save numpy array data
            save_numpy_array(self.data_transformation_config.train_file_path,train_arr)
            save_numpy_array(self.data_transformation_config.test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocesser_object)

            save_object("final_models/preprocessor.pkl", preprocesser_object,)

            # preparing artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.train_file_path,
                transformed_test_file_path=self.data_transformation_config.test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path)

            return data_transformation_artifact

        except Exception as e:
            raise CreditCardException(e,sys)

