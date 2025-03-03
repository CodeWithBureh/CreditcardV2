import os
import sys

from creditcard.exception.exception import CreditCardException
from creditcard.logging.logger import logging

from creditcard.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from creditcard.entity.config_entity import ModelTrainerConfig

from creditcard.utils.main_utils.utils import save_object, load_object , load_numpy_array_data, evaluate_models
from creditcard.utils.ml_utils.model.estimator import CreditCardModel
from creditcard.utils.ml_utils.metric.classification import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier)
import mlflow
import dagshub


dagshub.init(repo_owner='CodeWithBureh', repo_name='CreditCard', mlflow=True, token=os.getenv("DAGSHUB_TOKEN") )


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CreditCardException
        
        def track_mlflow(self, best_model, classification_metric):
            with mlflow.start_run():
                f1_score = classification_metric.f1_score
                precision_score = classification_metric.precision_score
                recall_score = classification_metric.recall_score

                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision_score", precision_score)
                mlflow.log_metric("recall_score", recall_score)
                mlflow.sklearn.log_model(best_model, "model")


    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "Random Forest" : RandomForestClassifier(verbose=1), 
            "Decision Tree" : DecisionTreeClassifier(),
            "Gradient Boosting" : GradientBoostingClassifier(verbose=1), 
            "Logistic Regression" : LogisticRegression(verbose=1), 
            "AdaBoost" : AdaBoostClassifier(),
        }
        params = {
            "Decision Tress":{
                "criterion" : ["gini", "entropy", "log_loss"],
                # splitter : ["best", "random"],
                # "max_features" : ["sqrt", "log2"],
            },
            "Random Forest":{
                #"criterion" : ["gini", "entropy", "log_loss"],
                #"max_features":["sqrt", "log2", None],
                "n_estimators" : [8,16,32,64,128,256]
            },
            "Gradient Boosting":{
                # "loss":["log_loss", "exponential"],
                "learning_rate":[.1, .01, .05, .001],
                "subsample": [.6, .7 , .75, .8 , .85, .9 ],
                #"criterion" : ["gini", "entropy", "log_loss"],
                #"max_features":["sqrt", "log2", None],
                "n_estimators" : [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                "learning_rate": [.1, .01, .05 ,.001],
                "n_estimators": [8,16,32,64,128,256]
            }
        }
        model_report : dict = evaluate_models(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test
                                              ,models=models , param=params)
        
        ## To get best model score from dict
        best_model_score = max(sorted(model_report.values()))

        ## To get best model name from dict

        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]
        y_train_pred = best_model.predict(x_train)

        classification_train_metric = get_classification_score(y_true=y_train , y_pred=y_train_pred) # Will be logged in MLFLOW

        ## Track the experiments with MLFLOW
        self.track_mlflow(best_model, classification_train_metric)


        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_true=y_test , y_pred= y_test_pred)
        
        self.track_mlflow(best_model, classification_test_metric)


        preprocessor = load_object(file_path= self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        Credit_Card_Model = CreditCardModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=Credit_Card_Model)
        
        #Model Pusher
        save_object("final_models/model.pkl", best_model)

        ## Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric)
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact




    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try: 
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model = self.train_model(x_train,y_train,x_test , y_test)

        except Exception as e:
            raise CreditCardException(e,sys)