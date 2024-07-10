##To work with any IA API first install library with terminal
##Gemini IA library !pip install -q -U google-generativeai
##Python library user pip install ipython

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display 
from IPython.display import Markdown

import streamlit as st

#GEMINI API Configuration

def to_markdown(text):
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


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

genero = st.selectbox('¿Qué género literario prefieres?', ['Ciencia Ficción', 'Fantasía', 'No Ficción', 'Misterio', 'Romance'])
tipo = st.radio('¿Estás buscando libros, blogs o artículos?', ['Libros', 'Blogs', 'Artículos'])
tiempo = st.slider('¿Cuánto tiempo por día sueles dedicar a la lectura? (en horas)', 1, 20)
temas = st.text_input('¿Qué temas te interesan actualmente?')

def obtener_recomendaciones(genero, tipo, tiempo, temas):
    prompt = f"Recomienda {tipo} sobre {temas} en el género {genero} para alguien que suele dedicar {tiempo} horas por día a la lectura."
    
    response = model.generate_content(prompt)
    
    # Imprimir la respuesta completa para ver su estructura JSON
    #st.write(response) 
    
    # Parsear la respuesta de la API para extraer las recomendaciones
    recomendations = response.candidates[0].content.parts[0].text.split('\n')
    
    return recomendations

if st.button('Obtener Recomendaciones'):
    st.write('Recomendaciones para ti:')
    recomendations = obtener_recomendaciones(genero, tipo, tiempo, temas)
    for rec in recomendations:
        st.markdown(f"- {rec}")
