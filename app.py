import sys 
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGODB_URL_KEY")

print(mongo_db_url)

import pymongo
from creditcard.exception.exception import CreditCardException
from creditcard.logging.logger import logging
from creditcard.pipeline.training_pipeline import TrainingPipeline
from creditcard.utils.ml_utils.model.estimator import CreditCardModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request

from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from creditcard.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from creditcard.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
from creditcard.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/" , tags=["authenication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        CreditCardException(e,sys)

@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocessor=load_object("final_models/preprocessor.pkl")
        final_model=load_object("final_models/model.pkl")
        creditcard_model=CreditCardModel(preprocessor=preprocessor, model=final_model)
        print(df.iloc[0])
        y_pred=creditcard_model.predict(df)
        print(y_pred)
        df["predicted_column"] = y_pred
        print(df["predicted_column"])
        df.to_csv("prediction_output/output.csv")
        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse("table.html", {"request": request, "table":table_html})
    
    except Exception as e:
        CreditCardException(e,sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
