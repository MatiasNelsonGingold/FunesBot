import streamlit as st
from PIL import Image


def generate_response(input_text):
    # Aquí puedes agregar la lógica para generar la respuesta del modelo GPT
    # Basado en el texto de entrada
    # Puedes utilizar tu propio modelo o una API de chatbot como OpenAI GPT-3

    # Ejemplo de respuesta estática
    response = "Hola, soy un chatbot. ¿En qué puedo ayudarte?"

    return response

def main():
    # Configuración de la página
    st.set_page_config(page_title="Chatbot con Streamlit", page_icon=":speech_balloon:")

    # Imagen de fondo
    image = Image.open("iamegenfondo.jpg")  # Reemplaza "background-image.jpg" con el nombre de tu imagen local
    st.image(image, use_column_width=True)

    # Título y texto de bienvenida
    st.title("Chatbot con Streamlit")
    st.write("¡Bienvenido! Este es un chatbot que puede responder tus preguntas. Por favor, ingresa tus preguntas en el campo de texto a continuación.")

    # Área de texto para ingresar el contexto del chat
    context = st.text_area("Contexto del chat:")

    # Lista para almacenar el historial de preguntas y respuestas
    chat_history = []

    # Bucle continuo de preguntas y respuestas
    while True:
        # Área de texto para que el usuario ingrese la pregunta
        user_input = st.text_input("Ingresa tu pregunta:")

        # Verificar si se presiona la tecla Enter en el teclado
        if user_input and (st.button("Enviar") or st.session_state.enter_pressed):
            # Generar respuesta
            response = generate_response(user_input)

            # Agregar la pregunta y respuesta al historial
            chat_history.append((user_input, response))

            # Restablecer el valor de enter_pressed
            st.session_state.enter_pressed = False

        # Mostrar el historial de preguntas y respuestas
        with st.expander("Historial completo"):
            for i, (question, answer) in enumerate(chat_history, 1):
                st.write(f"**Pregunta {i}:** {question}")
                st.write(f"**Respuesta {i}:** {answer}")

        # Mostrar la respuesta más reciente
        if len(chat_history) > 0:
            st.subheader("Respuesta más reciente:")
            st.text(chat_history[-1][1])

        # Opción para hacer otra pregunta
        another_question = st.button("Hacer otra pregunta")
        if not another_question:
            break

if __name__ == "__main__":
    main()
