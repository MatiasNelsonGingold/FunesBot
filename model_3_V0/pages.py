#from primer_input import book
retrieval_ = ['What I say is widen the scope of our society, let the\nmot d’ordre be not virtue alone but independence and action as well!”\n\nNicholas, who had left his nephew, irritably pushed up an armchair, sat\ndown in it, and listened to Pierre, coughing discontentedly and frowning\nmore and more.\n\n“But action with what aim?” he cried. “And what position will you adopt\ntoward the government?”\n\n“Why, the position of assistants. The society need not be secret if the\ngovernment allows it. ', 'Princess Mary will take her there and\nshow her over, and they’ll talk nineteen to the dozen. That’s\ntheir woman’s way! I am glad to have her. Sit down and talk. About\nMikhelson’s army I understand—Tolstóy’s too... a simultaneous\nexpedition.... But what’s the southern army to do? Prussia is\nneutral... I know that. What about Austria?” said he, rising from his\nchair and pacing up and down the room followed by Tíkhon, who ran after\nhim, handing him different articles of clothing. “What of Sweden? ', '“He seeks only for peace, and only\nthese people sans foi ni loi * can give it him—people who recklessly\nhack at and strangle everything—Magnítski, Arakchéev, and tutti\nquanti.... You will agree that if you did not look after your estates\nyourself but only wanted a quiet life, the harsher your steward was the\nmore readily your object might be attained,” he said to Nicholas.\n\n* Without faith or law.\n\n“Well, what does that lead up to?” said Nicholas.\n\n“Well, everything is going to ruin! ', 'Such is the fate not of great men (grands hommes) whom the Russian mind\ndoes not acknowledge, but of those rare and always solitary individuals\nwho, discerning the will of Providence, submit their personal will to\nit. The hatred and contempt of the crowd punish such men for discerning\nthe higher laws.\n\nFor Russian historians, strange and terrible to say, Napoleon—that most\ninsignificant tool of history who never anywhere, even in exile, showed\nhuman dignity—Napoleon is the object of adulation and enthusiasm; he\nis grand. ', 'At that moment it seemed to\nhim that he was chosen to give a new direction to the whole of Russian\nsociety and to the whole world.\n\n“I only wished to say that ideas that have great results are always\nsimple ones. My whole idea is that if vicious people are united and\nconstitute a power, then honest folk must do the same. Now that’s simple\nenough.”\n\n“Yes.”\n\n“And what were you going to say?”\n\n“I? Only nonsense.”\n\n“But all the same?”\n\n“Oh nothing, only a trifle,” said Natásha, smiling still more brightly.\n']

for texto in retrieval_:
    print (f"aqui: {texto}")


#Limpiar el retrieval de caracteres distractores ****
def limpiar_texto(list_of_retrieval):
    texto_limpio = []
    for texto in list_of_retrieval:
        texto_sin_saltos = texto.replace("\\n", " ")
        texto_limpio_ = texto_sin_saltos.replace("\\", " ")
        texto_limpio_ = texto_limpio_.replace("\n", " ")
        texto_limpio.append(texto_limpio_)
    return texto_limpio


#Buscar cada retrieval en el PDF ***
def buscar_pagina(texto_buscado, lista):
    for indice, texto in enumerate(lista):
        if texto_buscado in texto:
            return indice + 1
    return -1

#Entrega valores únicos, útiles y ordenados
def paginas_a_mostrar(list):
    conjunto = set(list)
    filter_list = [num for num in conjunto if num > 0]
    return filter_list

#Generador de respuesta
def obtener_contexto(total_pages):
    if len(total_pages) > 1:
        pages = ", ".join(map(str, sorted(total_pages[:-1])))
        last_pages = str(total_pages[-1])
        texto_final = f"You can find more context for these questions on pages {pages} and {last_pages}"
    elif len(total_pages) == 1:
        texto_final = f"You can find more context for these question on page {total_pages[0]}"
    else:
        texto_final = "There is no specific context for this question"
    return texto_final

#OUTPUT FINAL
def funcion_todo(list_of_retrieval, book):
    texto_limpio = limpiar_texto(list_of_retrieval)
    tmp = []
    for texto in texto_limpio:
        texto_in = texto[1:20]
        tmp.append(buscar_pagina(texto_in, book))
    pages = paginas_a_mostrar(tmp)
    final_answer = obtener_contexto(pages)
    return final_answer


#print(funcion_todo(retrieval_,book))
