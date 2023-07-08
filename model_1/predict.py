from model import *
from primer_input import *
from params import *
<<<<<<< HEAD
from sentence_transformers import SentenceTransformer, util
=======
>>>>>>> main

import openai

import os
import sys
<<<<<<< HEAD
import pprint


from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')

def predict(query,pipe,chat,prompt_template):
    
    prediction = pipe.run(
        query=query, params={"Retriever": {"top_k": 30}, "Reader": {"top_k": 10}}
    )

    # Compute dot score between query and all document embeddings
    query_emb = model.encode(query)
    doc_emb = model.encode([doc.content for doc in prediction['documents']])
    scores = util.dot_score(query_emb, doc_emb)[0].cpu().tolist()

    # Combine docs & scores
    doc_score_pairs = list(zip([doc.content for doc in prediction['documents']], scores))

    # Sort by decreasing score
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    # Create a list of the context returned by the retrieval used
    list_of_contextual_ans_retrieval=[]


    MINIMUM_SCORE = 21.5  # Adjust this threshold based on your needs

    for content, score in doc_score_pairs:
        if score >= MINIMUM_SCORE:
            list_of_contextual_ans_retrieval.append(content)  # add document content
            list_of_contextual_ans_retrieval.append(score)  # add document score

    # Establish the format to call the OpenAI chat
=======



def predict(query,pipe,chat,prompt_template):

    prediction = pipe.run(
        query=query, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 5}}
    )

    # crear lista del contexto retornado por el retrieval utilizado
    list_of_contextual_ans_retrieval=[]

    for i in range (5):
        list_of_contextual_ans_retrieval.append(prediction['documents'][i].content)

    print(list_of_contextual_ans_retrieval)

    # #establecer el formato de llamar el openai chat
>>>>>>> main
    preparation_answer_user = prompt_template.format_messages(
                        query=query,
                        list_of_contextual_ans_retrieval=list_of_contextual_ans_retrieval)

<<<<<<< HEAD
    # Call the LLM to answer the question with the context cited
    answer_user_final = chat(preparation_answer_user)

    print(list_of_contextual_ans_retrieval)
    return answer_user_final

=======

    # # Call the LLM to answer the question with the context cited
    answer_user_final = chat(preparation_answer_user)


    return answer_user_final
>>>>>>> main
