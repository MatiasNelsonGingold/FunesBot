from model import *
from primer_input import *
from params import *
from pages import *
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')


def predict_final(query,pipe,chat,prompt_template):

    prediction = pipe.run(
        query=query, params={"Retriever": {"top_k": 30}, "Reader": {"top_k": 10}}
    )

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
            list_of_contextual_ans_retrieval.append(score)  # add document score

    for i in range (5):
        list_of_contextual_ans_retrieval.append(prediction['documents'][i].content)

    print(list_of_contextual_ans_retrieval)


    # #establecer el formato de llamar el openai chat
    preparation_answer_user = prompt_template.format_messages(
                        query=query,
                        list_of_contextual_ans_retrieval=list_of_contextual_ans_retrieval)


    # # Call the LLM to answer the question with the context cited
    answer_user_final = chat(preparation_answer_user)

    answer_pages_final = funcion_todo(list_of_contextual_ans_retrieval,book)

    return dict(Respuesta = answer_user_final, Contexto = answer_pages_final)

#valor_pregunta - valor_extracto -> valor indicativo de que tanta referencia a lap regunta hace el extracto
