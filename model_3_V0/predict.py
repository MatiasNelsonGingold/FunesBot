from model import *
from primer_input import *
from params import *
#from pages import *
from chapter_book_page import *
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.corpus import stopwords
import spacy
import numpy as np

model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')
nlp = spacy.load("en_core_web_sm")

def measure_complexity(query):
    doc = nlp(query)
    stopwords = nltk.corpus.stopwords.words('english')
    non_stopword_count = len([word for word in nltk.word_tokenize(query) if word not in stopwords])/(2/5)
    OPTIMAL_WORD_COUNT = 8  # Adjust this based on your observations
    word_count = len(query.split())
    length_penalty = max(0, min(1, int(OPTIMAL_WORD_COUNT - word_count)))
    named_entity_penalty = 0
    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            named_entity_penalty += 2
        elif entity.label_ == 'LOCATION':
            named_entity_penalty += 1

    complexity = named_entity_penalty + non_stopword_count + length_penalty
    complexity = min(max(complexity, 0), 10)
    return int(complexity)

def complexity_to_top_k(complexity):
    # Use a linear function to calculate top_k for the retriever
    top_k_retriever = (20*complexity)
    top_k_reader = complexity
    return top_k_retriever, top_k_reader

def predict_final(query,pipe,chat,prompt_template):
    prediction = []
    complexity = measure_complexity(query)
    top_k_retriever, top_k_reader = complexity_to_top_k(complexity)
    prediction = pipe.run(
        query=query, params={"Retriever": {"top_k": top_k_retriever}, "Reader": {"top_k": top_k_reader}})
    query_emb = model.encode(query)
    doc_emb = model.encode([doc.content for doc in prediction['documents']])
    scores = util.dot_score(query_emb, doc_emb)[0].cpu().tolist()
    doc_score_pairs = list(zip([doc.content for doc in prediction['documents']], scores))
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    # crear lista del contexto retornado por el retrieval utilizado
    list_of_contextual_ans_retrieval=[]

    count = 0
    MINIMUM_SCORE = 21.5  # Adjust this threshold based on your needs

    for content, score in doc_score_pairs:
        if count < 1 or score >= MINIMUM_SCORE:
            list_of_contextual_ans_retrieval.append(content)  # add document content
            count+= 1
            #list_of_contextual_ans_retrieval.append(score)  # add document score

    #for i in range (5):
    #    list_of_contextual_ans_retrieval.append(prediction['documents'][i].content)

    # #establecer el formato de llamar el openai chat
    preparation_answer_user = prompt_template.format_messages(
                        query=query,
                        list_of_contextual_ans_retrieval=list_of_contextual_ans_retrieval)
     # # Call the LLM to answer the question with the context cited
    answer_user_final = chat(preparation_answer_user)

    #answer_pages_final = funcion_todo(list_of_contextual_ans_retrieval,book)
    answer_pages_final = funcion_todo(list_of_contextual_ans_retrieval,book,meta_datos)

    #final_answer
    answer_final = answer_user_final.content + "\n\n" + answer_pages_final

    return answer_final
#valor_pregunta - valor_extracto -> valor indicativo de que tanta referencia a lap regunta hace el extracto
