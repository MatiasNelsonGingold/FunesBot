#Limpiar el retrieval de caracteres distractores ****
def limpiar_texto(list_of_retrieval):
    texto_limpio = []
    for texto in list_of_retrieval:
        texto_sin_saltos = texto.replace("\\n", " ")
        texto_limpio_ = texto_sin_saltos.replace("\\", " ")
        texto_limpio_ = texto_limpio_.replace("\n", " ")
        texto_limpio.append(texto_limpio_)
    return texto_limpio

#Buscar cada retrieval en el PDF
def buscar_pagina(texto_buscado, lista):
    for indice, texto in enumerate(lista):
        if texto_buscado in texto:
            return indice + 1
    return -1

#Buscar libro capítulo y página del retrieval
def book_chapter_page(page,texto_limpio,meta_datos,tmp,book):
    metadatos = meta_datos[meta_datos.apply(lambda row: row['started_page'] < int(page) < row['end_page'], axis=1)]
    if not metadatos.empty:
        chapter = metadatos['Chapter'].iloc[0]
        books = metadatos['Book'].iloc[0]
        return page, chapter, books
    else:
        n_texto = tmp.index(page)
        p_chapter = book[page-1].find('CHAPTER')
        p_texto = book[page-1].find(texto_limpio[n_texto])

        if p_chapter > p_texto:
            metadatos = meta_datos[meta_datos['end_page'] == page]
            if not metadatos.empty:
                chapter = metadatos['Chapter'].iloc[0]
                book = metadatos['Book'].iloc[0]
                return page, chapter, book
        else:
            metadatos = meta_datos[meta_datos['started_page'] == page]
            if not metadatos.empty:
                chapter = metadatos['Chapter'].iloc[0]
                book = metadatos['Book'].iloc[0]
                return page, chapter, book
        return page, None, None
        
#Entrega valores únicos, útiles y ordenados
def contexto_a_mostrar(metadatos):
    step1 = [metadato for metadato in metadatos if metadato[0] != -1]
    step2 = set(step1)
    step3 = sorted(step2, key=lambda x: x[0])
    return step3

#Extraer cada concepto
def obtener_capitulo_libro(chapter, book, page):
    return f"{chapter} of {book} (page {page})"

#Generador de respuesta
def obtener_contexto(total_pages):
    if len(total_pages) > 1:
        context_pages = [obtener_capitulo_libro(chapter, book, page) for page, chapter, book in total_pages[:-1]]
        contexto_paginas = ", ".join(context_pages)
        last_page = context_pages[-1]
        texto_final = f"You can find more context for these questions on {contexto_paginas} and {last_page}."
    elif len(total_pages) == 1:
        page, chapter, book = total_pages[0]
        texto_final = f"You can find more context for this question on {obtener_capitulo_libro(chapter, book, page)}."
    else:
        texto_final = "There is no specific context for this question."
    return texto_final

#OUTPUT FINAL
def funcion_todo(list_of_retrieval, book, meta_datos):
    texto_limpio = limpiar_texto(list_of_retrieval)
    tmp = []
    for texto in texto_limpio:
        texto_in = texto[1:20]
        tmp.append(buscar_pagina(texto_in, book))
    metadatos_paginas = []
    for page in tmp:
        metadatos_paginas.append(book_chapter_page(page,texto_limpio,meta_datos,tmp,book))
    context1 = contexto_a_mostrar(metadatos_paginas)
    final_answer = obtener_contexto(context1)
    return final_answer
