from model import *
from primer_input import *
from params import *
from pages import *
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.corpus import stopwords
import spacy
import numpy as np

model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')
nlp = spacy.load("en_core_web_sm")

def measure_complexity(query):
    unique_word_count = len(set(nltk.word_tokenize(query)))
    doc = nlp(query)
    named_entity_count = len(doc.ents)
    stopwords = nltk.corpus.stopwords.words('english')
    non_stopword_count = len([word for word in nltk.word_tokenize(query) if word not in stopwords])
    OPTIMAL_WORD_COUNT = 10  # Adjust this based on your observations
    word_count = len(query.split())
    length_penalty = (word_count - OPTIMAL_WORD_COUNT) ** 2
    complexity = 1 * unique_word_count + 2 * named_entity_count + 1.5 * non_stopword_count + length_penalty
    return complexity

def complexity_to_top_k(complexity):
    # Use a logarithmic function to calculate top_k for the retriever
    top_k_retriever = 30
    OPTIMAL_WORD_COUNT = 10
    top_k_reader = min(int(complexity / (OPTIMAL_WORD_COUNT / 10)), 10)
    return top_k_retriever, top_k_reader


def predict_final(query,pipe,chat,prompt_template):
    prediction = {}
    complexity = measure_complexity(query)
    top_k_retriever, top_k_reader = complexity_to_top_k(complexity)
    prediction = pipe.run(
        query=query, params={"Retriever": {"top_k": top_k_retriever}, "Reader": {"top_k": top_k_reader}})
    print("Retriever top_k: {}".format(top_k_retriever))
    print("Reader top_k: {}".format(top_k_reader))
    query_emb = model.encode(query)
    doc_emb = model.encode([doc.content for doc in prediction['documents']])
    scores = util.dot_score(query_emb, doc_emb)[0].cpu().tolist()
    doc_score_pairs = list(zip([doc.content for doc in prediction['documents']], scores))
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    # crear lista del contexto retornado por el retrieval utilizado
    list_of_contextual_ans_retrieval=[]

    MINIMUM_SCORE = 21.5  # Adjust this threshold based on your needs
    for content, score in doc_score_pairs:
        if score >= MINIMUM_SCORE:
            list_of_contextual_ans_retrieval.append(content)  # add document content
            #list_of_contextual_ans_retrieval.append(score)  # add document score
    print(len(list_of_contextual_ans_retrieval))
    #for i in range (10):
    #    list_of_contextual_ans_retrieval.append(prediction['documents'][i].content)

   # print('############')
    #print(list_of_contextual_ans_retrieval)
    #print('-----------------')
    #print(limpiar_texto(list_of_contextual_ans_retrieval))
    #print('############')

    # #establecer el formato de llamar el openai chat
    preparation_answer_user = prompt_template.format_messages(
                        query=query,
                        list_of_contextual_ans_retrieval=list_of_contextual_ans_retrieval)


    # # Call the LLM to answer the question with the context cited

    answer_pages_final = funcion_todo(list_of_contextual_ans_retrieval,book)

    answer_user_final = chat(preparation_answer_user)

    answer_user_final = answer_user_final.content + "\n\n" + answer_pages_final

    #answer_user_final = answer_user_final.text + "\n\n" + answer_pages_final

    return answer_user_final

    #return dict(Respuesta = answer_user_final, Contexto = answer_pages_final)

#valor_pregunta - valor_extracto -> valor indicativo de que tanta referencia a lap regunta hace el extracto
