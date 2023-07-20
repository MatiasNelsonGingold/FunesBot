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
