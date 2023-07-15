import numpy as np
import pandas as pd

from haystack.nodes.retriever.dense import EmbeddingRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from params import *



def initialize_model(document_store):

    retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="multi-qa-MiniLM-L6-cos-v1",
    model_format="sentence_transformers"
    )

    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

    pipe = ExtractiveQAPipeline(reader, retriever)

    # To control the randomness and creativity of the generated
    # text by an LLM, use temperature = 0.0
    chat = ChatOpenAI(temperature=0.1,openai_api_key=ian_openai_api)


    #PROMPT TEMPLATE
    template_string = """Answer the question {query} \
    With the context found in the text within the list {list_of_contextual_ans_retrieval}
    """

    prompt_template = ChatPromptTemplate.from_template(template_string)

    return pipe,chat,prompt_template
