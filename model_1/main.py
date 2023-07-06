import numpy as np
import pandas as pd

from model import *
from primer_input import *
from predict import *

#primer paso es crear el pipe, crear el enlace con openai a través de la librería de langchain
#Por último, crear el template del prompt que se utilizará
document_store,pipe,chat,prompt_template =initialize_model()

#preprocesamiento del libro
indexing_pipeline=primer_input(document_store)

#llamar la pregunta del usuario
respuesta_u=predict(query='what are the main traits of Pierre Bezukhov?',pipe=pipe,chat=chat,prompt_template=prompt_template)

print(respuesta_u)
