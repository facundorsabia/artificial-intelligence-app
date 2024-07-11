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

genero = st.selectbox('¿Qué género literario prefieres?', ['No Ficción', 'Filosofía', 'Poesía', 'Fantasía',  'Misterio', 'Terror', 'Romance', 'Ciencia Ficción', 'Histórico', 'Biográfico', 'Autoayuda'])
tipo = st.radio('¿Estás buscando libros, blogs o artículos?', ['Libros', 'Blogs', 'Artículos'])
temas = st.text_input('¿Qué temas específicos te interesan actualmente?')

def obtener_recomendaciones(genero, tipo, temas):
    prompt = f"Quiero que seas un experto en literatura. Recomienda {tipo} sobre {temas} en el género {genero} para alguien que suele dedicar horas por día a la lectura." 

    response = model.generate_content(prompt)
    
    # Imprimir la respuesta completa para ver su estructura JSON
    #st.write(response)
    
    if not response.candidates:
        return ["Lo siento, no se encontraron recomendaciones. Por favor, intenta con diferentes parámetros."]
    
    # Parsear la respuesta de la API para extraer las recomendaciones
    recomendations = response.candidates[0].content.parts[0].text.split('\n')
    
    # Parsear las recomendaciones
    parsed_recomendations = []
    for rec in recomendations:
        if ' de ' in rec:
            title_author = rec.split(' de ')
            title = title_author[0].replace('* ', '').replace('*', '').strip()
            author = title_author[1].strip()
            parsed_recomendations.append({"title": title, "author": author, "description": ""})
    
    return parsed_recomendations

# Función para crear tarjetas (cards) con recomendaciones
def create_card(recommendation):
    card_html = f"""
    <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin:10px; max-width: 300px;">
        <h2 style="color:#333;">{recommendation['title']}</h2>
        <h4 style="color:#666;">{recommendation['author']}</h4>
        <p style="color:#999;">{recommendation['description']}</p>
    </div>
    """
    return card_html

if st.button('Obtener Recomendaciones'):
    st.write('Aguarda un momento, estoy buscando las mejores recomendaciones para ti:')
    recomendations = obtener_recomendaciones(genero, tipo, temas)
    
    # Generar y mostrar las tarjetas
    cards_html = "".join([create_card(rec) for rec in recomendations])
    components.html(cards_html, height=600, scrolling=True)
