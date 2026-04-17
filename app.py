import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración visual
st.set_page_config(page_title="App Taller Pro", page_icon="🔧")
st.title("🔧 Control de Tiempos")

ARCHIVO = "registro_taller.csv"

# --- LÓGICA DE ESTADO ---
if 'inicio' not in st.session_state:
    st.session_state.inicio = None
if 'tarea_actual' not in st.session_state:
    st.session_state.tarea_actual = ""
if 'mostrando_confirmacion' not in st.session_state:
    st.session_state.mostrando_confirmacion = False

# --- FORMULARIO DE INICIO ---
st.subheader("Datos de la Tarea")
nombre = st.text_input("Nombre del Mecánico", placeholder="Ej: Juan")
tarea_input = st.text_input("Tarea Inicial / Vehículo", placeholder="Ej: Revisión Seat Ibiza")

# Botón de Inicio
if not st.session_state.mostrando_confirmacion:
    if st.button("▶️ Iniciar Trabajo", use_container_width=True, disabled=st.session_state.inicio is not None):
        if nombre and tarea_input:
            st.session_state.inicio = datetime.now()
            st.session_state.tarea_actual = tarea_input
            st.success(f"¡Cronómetro en marcha! Empezaste a las {st.session_state.inicio.strftime('%H:%M:%S')}")
        else:
            st.error("Por favor, rellena el nombre y la tarea antes de empezar.")

# --- SECCIÓN DE FINALIZACIÓN ---
if st.session_state.inicio is not None:
    st.divider()
    st.warning(f"Trabajando en: **{st.session_state.tarea_actual}**")
    
    # Al pulsar este botón, activamos el modo confirmación
    if st.button("⏹️ Terminar y Registrar", use_container_width=True):
        st.session_state.mostrando_confirmacion = True

    # Si estamos en modo confirmación, aparece este cuadro extra
    if st.session_state.mostrando_confirmacion:
        st.info("¿Quieres corregir el nombre de la tarea antes de guardar?")
        tarea_final = st.text_input("Nombre final de la tarea:", value=st.session_state.tarea_actual)
        
        if st.button("💾 Confirmar y Guardar Todo", use_container_width=True, color="primary"):
            fin = datetime.now()
            duracion = fin - st.session_state.inicio
            
            # Guardar en el archivo CSV
            datos = pd.DataFrame([{
                "Mecánico": nombre,
                "Tarea Final": tarea_final,
                "Inicio": st.session_state.inicio.strftime("%d/%m/%Y %H:%M:%S"),
                "Fin": fin.strftime("%d/%m/%Y %H:%M:%S"),
                "Duración": str(duracion).split(".")[0]
            }])
            
            datos.to_csv(ARCHIVO, mode='a', index=False, header=not os.path.exists(ARCHIVO))
            
            # Resetear todo para la siguiente tarea
            st.session_state.inicio = None
            st.session_state.mostrando_confirmacion = False
            st.balloons()
            st.success("¡Registro guardado correctamente!")
            st.rerun() # Recarga la app para limpiar la pantalla

# --- HISTORIAL ---
if os.path.exists(ARCHIVO):
    st.write("---")
    st.subheader("📋 Últimos Trabajos Realizados")
    df = pd.read_csv(ARCHIVO)
    # Mostramos los últimos 10 registros, los más nuevos arriba
    st.dataframe(df.iloc[::-1].head(10), use_container_width=True)
