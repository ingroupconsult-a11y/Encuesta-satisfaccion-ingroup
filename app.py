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
    st.markdown("**Marca de 1 a 5 cada aspecto, donde 1 es «Muy insatisfecho/a» y 5 es «Muy satisfecho/a».**")

with col_der:
    st.image("ingroup - negroberde.png", width=140)

st.divider()

# Formulario de la encuesta completo
with st.form("encuesta_form"):
    
    st.subheader("Valoración del servicio")
    
    # Barras deslizantes (st.slider) del 1 al 5
    sat_general = st.slider(
        "Satisfacción general con el servicio.",
        min_value=1,
        max_value=5,
        value=3
    )
    
    comprension = st.slider(
        "Comprensión de las necesidades de tu empresa.",
        min_value=1,
        max_value=5,
        value=3
    )
    
    adecuacion = st.slider(
        "Adecuación de los candidatos presentados.",
        min_value=1,
        max_value=5,
        value=3
    )
    
    rapidez = st.slider(
        "Rapidez del proceso de selección.",
        min_value=1,
        max_value=5,
        value=3
    )
    
    comunicacion = st.slider(
        "Comunicación y seguimiento durante el proceso.",
        min_value=1,
        max_value=5,
        value=3
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
        ],
        horizontal=False
    )
    
    enviar = st.form_submit_button("Enviar valoración")

if enviar:
    # Conexión con Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_actual = conn.read(ttl=0)
    
    nueva_fila = {
        "Satisfacción General": sat_general,
        "Comprensión Necesidades": comprension,
        "Adecuación Candidatos": adecuacion,
        "Rapidez": rapidez,
        "Comunicación": comunicacion,
        "Lo que más valoras": lo_que_mas_valoras,
        "Qué podríamos mejorar": podriamos_mejorar,
        "Volvería a confiar": volveria
    }
    
    df_nuevo = pd.concat([df_actual, pd.DataFrame([nueva_fila])], ignore_index=True)
    conn.update(data=df_nuevo)
    
    st.success("¡Muchas gracias por tu tiempo y confianza! Tu respuesta se ha enviado correctamente.")
