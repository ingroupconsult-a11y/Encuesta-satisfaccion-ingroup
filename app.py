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
    st.markdown("Marca de 1 a 5 estrellas cada aspecto, donde 1 es «Muy insatisfecho/a» y 5 es «Muy satisfecho/a».")

with col_der:
    st.image("ingroup - negroberde.png", width=140)

st.divider()

# Formulario de la encuesta
with st.form("encuesta_form"):
    
    opciones_estrellas = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    
    st.subheader("Valoración del servicio")
    
    sat_general = st.radio(
        "Satisfacción general con el servicio.",
        options=opciones_estrellas,
        horizontal=True
    )
    
    comprension = st.radio(
        "Comprensión de las necesidades de tu empresa.",
        options=opciones_estrellas,
        horizontal=True
    )
    
    adecuacion = st.radio(
        "Adecuación de los candidatos presentados.",
        options=opciones_estrellas,
        horizontal=True
    )
    
    rapidez = st.radio(
        "Rapidez del proceso de selección.",
        options=opciones_estrellas,
        horizontal=True
    )
    
    comunicacion = st.radio(
        "Comunicación y seguimiento durante el proceso.",
        options=opciones_estrellas,
        horizontal=True
    )
    
    comentarios = st.text_area("Comentarios o sugerencias adicionales (opcional):")
    
    enviar = st.form_submit_button("Enviar valoración")

if enviar:
    def extraer_numero(texto_estrella):
        return len(texto_estrella)

    conn = st.connection("gsheets", type=GSheetsConnection)
    df_actual = conn.read(ttl=0)
    
    nueva_fila = {
        "Satisfacción General": extraer_numero(sat_general),
        "Comprensión Necesidades": extraer_numero(comprension),
        "Adecuación Candidatos": extraer_numero(adecuacion),
        "Rapidez": extraer_numero(rapidez),
        "Comunicación": extraer_numero(comunicacion),
        "Comentarios": comentarios
    }
    
    df_nuevo = pd.concat([df_actual, pd.DataFrame([nueva_fila])], ignore_index=True)
    conn.update(data=df_nuevo)
    
    st.success("¡Muchas gracias! Tu respuesta se ha enviado correctamente.")
 
