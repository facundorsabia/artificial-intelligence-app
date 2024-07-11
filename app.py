##To work with any IA API first install library with terminal
##Gemini IA library !pip install -q -U google-generativeai
##Python library user pip install ipython

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display 
from IPython.display import Markdown

import streamlit as st
import streamlit.components.v1 as components

#GEMINI API Configuration

def to_markdown(text):
    lines = text.strip().split('\n')
    indented_lines = [f"> {line}" for line in lines]
    indented_text = '\n'.join(indented_lines)
    return Markdown(indented_text)



GOOGLE_API_KEY= 'AIzaSyCMlwNbVEoIuhqxm63jeTf4a44ckVc2_kI'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.0-pro')

# APP Streamlit

st.set_page_config(
    page_title="Recomendador de Lecturas",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Recomendador de Lecturas')

genero = st.selectbox('¿Qué género literario prefieres?', ['Fantasía', 'No Ficción', 'Filosofía', 'Poesía', 'Misterio', 'Terror', 'Romance', 'Ciencia Ficción', 'Histórico', 'Biográfico', 'Autoayuda', 'Política'])
tipo = st.radio('¿Estás buscando libros, blogs o artículos?', ['Libros', 'Blogs', 'Artículos'])
temas = st.text_input('¿Qué temas específicos te interesan actualmente?')


def obtener_recomendaciones(genero, tipo, temas):
    prompt = f"Quiero que seas un experto en literatura. Recomienda {tipo} sobre {temas} en el género {genero}. Además agrega una pequeña reflexión final acerca de {temas} en {genero}" 

    response = model.generate_content(prompt)
    
    # Imprimir la respuesta completa para ver su estructura JSON
    #st.write(response)
    
    if not response.candidates:
        return ["Lo siento, no se encontraron recomendaciones. Por favor, intenta con diferentes parámetros."]
    
# Parsear las recomendaciones
    try:
        recomendations = response.candidates[0].content.parts[0].text.split('\n')
        return recomendations
    except IndexError:
        return ["Lo siento, no pudimos encontrar recomendaciones. Por favor intenta nuevamente."]

if st.button('Obtener Recomendaciones'):
    st.write('Aguarda un momento, estoy buscando las mejores recomendaciones para ti.')
    recomendations = obtener_recomendaciones(genero, tipo, temas)
    for rec in recomendations:
        st.markdown(f"{rec}")
