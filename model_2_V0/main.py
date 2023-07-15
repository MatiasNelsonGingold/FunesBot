import numpy as np
import pandas as pd

from model import *
from primer_input import *
from predict import *


#llamar la pregunta del usuario
#Primer paso es crear el vínculo con la base de datos con el libro ya spliteado en pinecone
document_store=primer_input_func()


#segundo paso es crear el pipe, crear el enlace con openai a través de la librería de langchain
#Por último, crear el template del prompt que se utilizará
pipe,chat,prompt_template =initialize_model(document_store)


#llamar la pregunta del usuario
respuesta_u=predict_final(query='who is pierre?',pipe=pipe,chat=chat,prompt_template=prompt_template)

print(respuesta_u)
