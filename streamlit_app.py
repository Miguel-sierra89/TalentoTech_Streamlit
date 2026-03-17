import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import os

# Configuración de la página
st.set_page_config(page_title="Energy & Climate Analysis", layout="wide")
sns.set_theme(style="whitegrid") # Estilo profesional

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    path = kagglehub.dataset_download("emirhanakku/climate-and-energy-consumption-dataset-20202024")
    # Buscamos el archivo CSV en el path descargado
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    df = pd.read_csv(os.path.join(path, csv_files[0]))
    # Convertir fecha si existe la columna 'Date' o similar
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error al cargar el dataset: {e}")
    df = pd.DataFrame()

# --- BARRA LATERAL (Navegación) ---
st.sidebar.title("Navegación")
app_mode = st.sidebar.radio("Ir a:", ["Inicio", "Panel de Trabajo"])

# --- LÓGICA DE PÁGINAS ---
if app_mode == "Inicio":
    st.title("🌍 Análisis de Energías Limpias y Clima")
    
    # Mostrar la imagen del usuario
    st.image("Energias limpias.jpg", use_container_width=True)
    
    st.markdown(f"""
    ## Bienvenida al Proyecto Integrador
    Este sistema analiza la intersección crítica entre el **cambio climático** y los **patrones de consumo energético**. 
    A través de este tablero, exploraremos cómo las variables meteorológicas impactan en la demanda de energía.

    **Sobre el Dataset:**
    Contiene registros desde 2020 hasta 2024, incluyendo:
    * Variables climáticas (Temperatura, Humedad).
    * Consumo de energía (MW/h).
    * Fuentes de generación.

    **Autor:** Miguel Sierra  
    **Curso:** Talento Tech - Nivel Integrador
    """)
    
    if st.button("Ingresar al Panel de Trabajo"):
        st.info("Usa el menú de la izquierda para cambiar a 'Panel de Trabajo'")

elif app_mode == "Panel de Trabajo":
    st.title("📊 Dashboard de Análisis de Datos")
    
    if df.empty:
        st.warning("Cargando datos...")
    else:
        tab1, tab2, tab3 = st.tabs(["Tendencias", "Correlaciones", "Distribuciones"])

        with tab1:
            st.subheader("📈 Evolución del Consumo Energético")
            fig, ax = plt.subplots(figsize=(10, 5))
            # Ajustar 'Date' y 'Energy_Consumption' según nombres reales de columnas
            sns.lineplot(data=df, x=df.columns[0], y=df.columns[1], ax=ax, color='#2ecc71')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            st.write("**Explicación:** Este gráfico muestra la serie temporal del consumo. Permite identificar picos estacionales donde la demanda de energía aumenta, posiblemente debido a temperaturas extremas.")

        with tab2:
            st.subheader("🌡️ Temperatura vs Consumo")
            fig, ax = plt.subplots(figsize=(10, 5))
            # Asumiendo columnas de Temp y Consumo
            sns.scatterplot(data=df, x=df.columns[2], y=df.columns[1], hue=df.columns[1], palette="viridis", ax=ax)
            st.pyplot(fig)
            st.write("**Explicación:** Analizamos la dispersión para entender si existe una relación lineal. Si los puntos forman una 'U' o una línea ascendente, confirmamos que el clima es un driver directo del consumo.")

        with tab3:
            st.subheader("📊 Distribución de Variables")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(df[df.columns[1]], kde=True, color="#3498db", ax=ax)
            st.pyplot(fig)
            st.write("**Explicación:** El histograma nos permite ver la frecuencia del consumo. La curva de densidad (KDE) ayuda a identificar si los datos siguen una distribución normal o si tenemos valores atípicos (outliers).")

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.write("Realizado por: **Miguel Sierra**")
