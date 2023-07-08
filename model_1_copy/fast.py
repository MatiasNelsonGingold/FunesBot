import pandas as pd
from fastapi import FastAPI
from predict import *

from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline

app = FastAPI()

document_store = InMemoryDocumentStore(use_bm25=True)

    #file path local
file_path_local = 'WAR_and_PEACE_TEXT_FORMAT.txt'

#Función primer input

indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run(file_path=file_path_local)

retriever = BM25Retriever(document_store=document_store)

reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

pipe = ExtractiveQAPipeline(reader, retriever)

##
@app.get("/predict")

def predict_ans(user_query: str):

    """
    single prediction with one input
    """
    #user_query= (dict(
    #    query=[user_query],
    #))


    answer_query=predict_final(user_query,pipe)

    return dict(answer_query = answer_query)

@app.get("/")
def root():
    return {'greeting': 'Hello'}
