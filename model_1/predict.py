from model import *
from primer_input import *
from params import *

import openai

import os
import sys



def predict(query,pipe,chat,prompt_template):

    prediction = pipe.run(
        query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
    )

    #crear lista del contexto retornado por el retrieval utilizado
    list_of_contextual_ans_retrieval=[]

    for i in range (10):
        list_of_contextual_ans_retrieval.append(prediction['documents'][i].content)

    preparation_answer_user = prompt_template.format_messages(
                        query=query,
                        list_of_contextual_ans_retrieval=list_of_contextual_ans_retrieval)


    # Call the LLM to answer the question with the context cited
    answer_user_final = chat(preparation_answer_user)

    return answer_user_final
