# Opciones puras de estrellas (sin números)
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
    
    # Botón de envío
    enviar = st.form_submit_button("Enviar valoración")

if enviar:
    # Como ahora guardamos solo las estrellas, contamos cuántas hay para sacar el número (1 a 5)
    def extraer_numero(texto_estrella):
        return len(texto_estrella) # "⭐" da 1, "⭐⭐" da 2, "⭐⭐⭐⭐⭐" da 5

    # Conexión con Google Sheets
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
    
    import pandas as pd
    df_nuevo = pd.concat([df_actual, pd.DataFrame([nueva_fila])], ignore_index=True)
    conn.update(data=df_nuevo)
    
    st.success("¡Muchas gracias! Tu respuesta se ha enviado correctamente.")
