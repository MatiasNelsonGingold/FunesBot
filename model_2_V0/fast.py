import pandas as pd
from fastapi import FastAPI
from predict import *
from model import *
from primer_input import *
from main import *


app = FastAPI()

##
@app.get("/predict")

def predict_ans(user_query: str):

    answer_query=predict_final(query=user_query,pipe=pipe,prompt_template=prompt_template,chat=chat)

    return dict(answer_query = answer_query)

@app.get("/")
def root():
    return {'greeting': 'Hello'}
