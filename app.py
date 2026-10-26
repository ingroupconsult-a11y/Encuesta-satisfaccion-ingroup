import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Encuesta de Satisfacción - Ingroup", page_icon="⭐", layout="centered")

st.title("Encuesta de satisfacción")
st.subheader("¿Cómo ha sido tu experiencia con Ingroup?")
st.write("Tu opinión nos ayuda a seguir mejorando nuestro servicio de selección.")
st.markdown("---")

# Formulario de la encuesta con el texto del Word
with st.form("form_encuesta"):
    cliente = st.text_input("Nombre de tu empresa / Cliente (Opcional)")
    
    st.markdown("### Valoración del servicio")
    st.write("Marca de 1 a 5 estrellas cada aspecto, donde 1 es «Muy insatisfecho/a» y 5 es «Muy satisfecho/a».")
    
    sat_general = st.slider("Satisfacción general con el servicio.", 1, 5, 5)
    necesidades = st.slider("Comprensión de las necesidades de tu empresa.", 1, 5, 5)
    candidatos = st.slider("Adecuación de los candidatos presentados.", 1, 5, 5)
    rapidez = st.slider("Rapidez del proceso de selección.", 1, 5, 5)
    comunicacion = st.slider("Comunicación y seguimiento durante el proceso.", 1, 5, 5)
    
    st.markdown("### Tu opinión nos ayuda a mejorar")
    valora_mas = st.text_area("¿Qué es lo que más valoras de nuestro servicio?")
    mejorar = st.text_area("¿Qué podríamos mejorar?")
    
    fidelizacion = st.radio(
        "¿Volverías a confiar en Ingroup para futuros procesos de selección?",
        ["Sí, sin duda", "Probablemente sí", "No lo tengo claro", "Probablemente no"]
    )
    
    enviado = st.form_submit_button("Enviar respuestas")

# Lógica al enviar el formulario para guardarlo en tu Excel/Google Sheets privado
if enviado:
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_existente = conn.read(ttl=0)
        
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Empresa": cliente if cliente else "Anónimo",
            "Satisfaccion_General": sat_general,
            "Comprension_Necesidades": necesidades,
            "Adecuacion_Candidatos": candidatos,
            "Rapidez": rapidez,
            "Comunicacion": comunicacion,
            "Lo_Que_Mas_Valora": valora_mas,
            "Que_Mejorar": mejorar,
            "Volveria_A_Confiar": fidelizacion
        }])
        
        df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
        conn.update(data=df_actualizado)
        
        st.success("¡Muchas gracias por tu tiempo y confianza! Tus respuestas han sido guardadas.")
        st.balloons()
    except Exception as e:
        st.error(f"Hubo un error al guardar los datos: {e}")
