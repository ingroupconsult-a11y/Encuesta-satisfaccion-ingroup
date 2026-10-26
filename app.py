import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Encuesta de Satisfacción | Ingroup",
    page_icon="📊",
    layout="centered"
)

# Cabecera con el Título a la izquierda y el Logo a la derecha
col_izq, col_der = st.columns([3, 1])

with col_izq:
    st.markdown("# Valoración del servicio")
    st.markdown("¿Cómo ha sido tu experiencia con Ingroup? Tu opinión nos ayuda a seguir mejorando nuestro servicio de selección.")
    st.markdown("**Marca de 1 a 5 estrellas cada aspecto, donde 1 es «Muy insatisfecho/a» y 5 es «Muy satisfecho/a».**")

with col_der:
    st.image("ingroup - negroberde.png", width=140)

st.divider()

# Formulario de la encuesta completo
with st.form("encuesta_form"):
    
    st.subheader("Valoración del servicio")
    
    # Opciones numéricas claras del 1 al 5 con estrellas limpias
    opciones_estrellas = {
        "⭐ (1 - Muy insatisfecho/a)": 1,
        "⭐⭐ (2)": 2,
        "⭐⭐⭐ (3)": 3,
        "⭐⭐⭐⭐ (4)": 4,
        "⭐⭐⭐⭐⭐ (5 - Muy satisfecho/a)": 5
    }
    
    sat_general = st.radio(
        "Satisfacción general con el servicio.",
        options=list(opciones_estrellas.keys()),
        horizontal=True
    )
    
    comprension = st.radio(
        "Comprensión de las necesidades de tu empresa.",
        options=list(opciones_estrellas.keys()),
        horizontal=True
    )
    
    adecuacion = st.radio(
        "Adecuación de los candidatos presentados.",
        options=list(opciones_estrellas.keys()),
        horizontal=True
    )
    
    rapidez = st.radio(
        "Rapidez del proceso de selección.",
        options=list(opciones_estrellas.keys()),
        horizontal=True
    )
    
    comunicacion = st.radio(
        "Comunicación y seguimiento durante el proceso.",
        options=list(opciones_estrellas.keys()),
        horizontal=True
    )
    
    st.divider()
    st.subheader("Tu opinión nos ayuda a mejorar")
    
    lo_que_mas_valoras = st.text_area("¿Qué es lo que más valoras de nuestro servicio?")
    podriamos_mejorar = st.text_area("¿Qué podríamos mejorar?")
    
    volveria = st.radio(
        "¿Volverías a confiar en Ingroup para futuros procesos de selección?",
        options=[
            "Sí, sin duda",
            "Probablemente sí",
            "No lo tengo claro",
            "Probablemente no"
        ]
    )
    
    enviar = st.form_submit_button("Enviar valoración")

if enviar:
    # Conexión con Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_actual = conn.read(ttl=0)
    
    nueva_fila = {
        "Satisfacción General": opciones_estrellas[sat_general],
        "Comprensión Necesidades": opciones_estrellas[comprension],
        "Adecuación Candidatos": opciones_estrellas[adecuacion],
        "Rapidez": opciones_estrellas[rapidez],
        "Comunicación": opciones_estrellas[comunicacion],
        "Lo que más valoras": lo_que_mas_valoras,
        "Qué podríamos mejorar": podriamos_mejorar,
        "Volvería a confiar": volveria
    }
    
    df_nuevo = pd.concat([df_actual, pd.DataFrame([nueva_fila])], ignore_index=True)
    conn.update(data=df_nuevo)
    
    st.success("¡Muchas gracias por tu tiempo y confianza! Tu respuesta se ha enviado correctamente.")
