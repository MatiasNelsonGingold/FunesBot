import pandas as pd
from fastapi import FastAPI
from predict import *
from model import *
from primer_input import *


app = FastAPI()

#llamar la pregunta del usuario
#Primer paso es crear el vínculo con la base de datos con el libro ya spliteado
document_store=primer_input_func()


#segundo paso es crear el pipe, crear el enlace con openai a través de la librería de langchain
#Por último, crear el template del prompt que se utilizará
pipe,chat,prompt_template =initialize_model(document_store)


##
@app.get("/predict")

def predict_ans(user_query: str):


    answer_query=predict_final(query=user_query,pipe=pipe,prompt_template=prompt_template,chat=chat)

    return dict(answer_query = answer_query)

@app.get("/")
def root():
    return {'greeting': 'Hello'}
