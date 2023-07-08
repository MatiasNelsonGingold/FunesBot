import numpy as np
import pandas as pd

from model import *
from primer_input import *
from predict import *

#Primer paso es el preprocesamiento del libro
document_store_f=primer_input_func()

#segundo paso es crear el pipe, crear el enlace con openai a través de la librería de langchain
#Por último, crear el template del prompt que se utilizará
pipe,chat,prompt_template =initialize_model(document_store_f)

model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')

#llamar la pregunta del usuario
respuesta_u=predict(query='Who is Pierre?',pipe=pipe,chat=chat,prompt_template=prompt_template)

print(respuesta_u)
