import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Configuración Profesional
st.set_page_config(page_title="Análisis Energético - Miguel Sierra", layout="wide")
sns.set_theme(style="whitegrid")
plt.rcParams['figure.facecolor'] = '#f0f2f6'

# 2. Carga de Datos Local
@st.cache_data
def load_local_data():
    # CAMBIA 'tu_archivo.csv' por el nombre real del archivo que subas a GitHub
    df = pd.read_csv('climate_and_energy_data.csv') 
    return df

# --- INTERFAZ ---
st.sidebar.title("⚡ Navegación")
menu = st.sidebar.radio("Ir a:", ["Inicio", "Dashboard Integrador"])

if menu == "Inicio":
    st.title("🌍 Análisis de Energías Limpias y Clima")
    try:
        st.image("Energias limpias.jpg", use_container_width=True)
    except:
        st.info("🖼️ (Imagen principal del proyecto)")

    st.markdown("""
    ## Bienvenida
    Este proyecto analiza la relación entre el clima y el consumo de energía (2020-2024).
    
    **👨‍💻 Desarrollado por:** Miguel Sierra
    **🎓 Institución:** Talento Tech - Nivel Integrador
    """)
    if st.button("Explorar Datos"):
        st.balloons()

else:
    st.title("📊 Panel de Análisis de Datos")
    try:
        data = load_local_data()
        
        tab1, tab2 = st.tabs(["📈 Tendencias", "🌡️ Clima vs Energía"])
        
        with tab1:
            st.subheader("Consumo Energético Mensual")
            fig, ax = plt.subplots(figsize=(10, 4))
            # Ajustamos color a verde profesional
            sns.lineplot(data=data, x=data.columns[0], y=data.columns[1], color="#27ae60", ax=ax)
            st.pyplot(fig)
            st.write("**Análisis:** Se observa el comportamiento histórico de la demanda.")

        with tab2:
            st.subheader("Relación Temperatura y Demanda")
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            sns.scatterplot(data=data, x=data.columns[2], y=data.columns[1], color="#2980b9", ax=ax2)
            st.pyplot(fig2)
            st.write("**Análisis:** Correlación entre variables climáticas y carga eléctrica.")

    except Exception as e:
        st.error(f"Falta subir el archivo CSV a GitHub. Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Realizado por Miguel Sierra")
