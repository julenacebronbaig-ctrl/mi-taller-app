import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración visual
st.set_page_config(page_title="App Taller", page_icon="🔧")
st.title("🔧 Control de Taller")

ARCHIVO = "registro_taller.csv"

# Campos de entrada
nombre = st.text_input("Nombre del Mecánico")
tarea = st.text_input("Tarea o Vehículo (Matrícula)")

# Usamos el "session_state" para que el cronómetro no se borre al refrescar la página
if 'inicio' not in st.session_state:
    st.session_state.inicio = None

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Iniciar", use_container_width=True):
        if nombre and tarea:
            st.session_state.inicio = datetime.now()
            st.success(f"Iniciado a las: {st.session_state.inicio.strftime('%H:%M:%S')}")
        else:
            st.warning("Faltan datos")

with col2:
    if st.button("⏹️ Terminar", use_container_width=True):
        if st.session_state.inicio:
            fin = datetime.now()
            duracion = fin - st.session_state.inicio
            
            # Guardar datos
            datos = pd.DataFrame([{
                "Mecánico": nombre,
                "Tarea": tarea,
                "Inicio": st.session_state.inicio.strftime("%H:%M:%S"),
                "Fin": fin.strftime("%H:%M:%S"),
                "Duración": str(duracion).split(".")[0]
            }])
            datos.to_csv(ARCHIVO, mode='a', index=False, header=not os.path.exists(ARCHIVO))
            
            st.balloons()
            st.info(f"Tiempo total: {str(duracion).split('.')[0]}")
            st.session_state.inicio = None # Reset
        else:
            st.error("No hay ninguna tarea iniciada")

# Mostrar historial abajo
if os.path.exists(ARCHIVO):
    st.write("---")
    st.subheader("Últimos registros")
    df = pd.read_csv(ARCHIVO)
    st.dataframe(df.tail(5), use_container_width=True)
