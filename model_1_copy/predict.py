from model import *
from primer_input import *
from params import *


from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from params import *



from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.document_stores import InMemoryDocumentStore


import openai
import os
import sys


def predict_final(query,pipe):
    # To control the randomness and creativity of the generated
    # text by an LLM, use temperature = 0.0
    chat = ChatOpenAI(temperature=0.5,openai_api_key=ian_api)


    #PROMPT TEMPLATE
    template_string = """Answer the question {query} \
    With the context found in the text within the list {list_of_contextual_ans_retrieval}
    """

    prompt_template = ChatPromptTemplate.from_template(template_string)

    prediction = pipe.run(
        query=query, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 5}}
    )

    # crear lista del contexto retornado por el retrieval utilizado
    list_of_contextual_ans_retrieval=[]

    for i in range (5):
        list_of_contextual_ans_retrieval.append(prediction['documents'][i].content)

    print(list_of_contextual_ans_retrieval)

    # #establecer el formato de llamar el openai chat
    preparation_answer_user = prompt_template.format_messages(
                        query=query,
                        list_of_contextual_ans_retrieval=list_of_contextual_ans_retrieval)


    # # Call the LLM to answer the question with the context cited
    answer_user_final = chat(preparation_answer_user)


    return dict(Respuesta = answer_user_final)
