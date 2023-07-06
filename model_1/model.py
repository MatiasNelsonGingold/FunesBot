import numpy as np
import pandas as pd

from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from params import *



def initialize_model():


    document_store = InMemoryDocumentStore(use_bm25=True)

    retriever = BM25Retriever(document_store=document_store)

    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

    pipe = ExtractiveQAPipeline(reader, retriever)

    # To control the randomness and creativity of the generated
    # text by an LLM, use temperature = 0.0
    chat = ChatOpenAI(temperature=0.5,openai_api_key=ian_api)


    #PROMPT TEMPLATE
    template_string = """Answer the question {query} \
    With the context found in the text within the list {list_of_contextual_ans_retrieval}
    """


    prompt_template = ChatPromptTemplate.from_template(template_string)

    return pipe,chat,prompt_template
