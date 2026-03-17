import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import os

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción de Streamlit)
st.set_page_config(page_title="Energy & Climate Analysis", layout="wide")

# Estilo de Seaborn para gráficos profesionales
sns.set_theme(style="whitegrid")

# 2. FUNCIÓN DE CARGA DE DATOS (Con caché para evitar esperas infinitas)
@st.cache_data(show_spinner=False)
def get_data():
    try:
        # Descarga desde Kaggle
        path = kagglehub.dataset_download("emirhanakku/climate-and-energy-consumption-dataset-20202024")
        
        # Buscar el archivo CSV en la carpeta descargada
        files = [f for f in os.listdir(path) if f.endswith('.csv')]
        if not files:
            return None
        
        full_path = os.path.join(path, files[0])
        df = pd.read_csv(full_path)
        
        # Limpieza básica de fechas si existen
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        if date_cols:
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]])
            
        return df
    except Exception as e:
        st.error(f"Error al conectar con Kaggle: {e}")
        return None

# --- LÓGICA DE NAVEGACIÓN ---
st.sidebar.title("🛠️ Panel de Control")
app_mode = st.sidebar.radio("Selecciona una sección:", ["Inicio", "Dashboard de Análisis"])

# --- PÁGINA 1: LANDING PAGE ---
if app_mode == "Inicio":
    st.title("🌍 Análisis de Energías Limpias y Clima")
    
    # Intentar cargar la imagen que subiste
    try:
        st.image("Energias limpias.jpg", use_container_width=True)
    except:
        st.warning("⚠️ Imagen 'Energias limpias.jpg' no encontrada en el repositorio.")

    st.markdown("""
    ---
    ### 📊 Sobre el Proyecto
    Este tablero interactivo ha sido diseñado para el curso de **Talento Tech (Nivel Integrador)**. 
    El objetivo es analizar cómo las variaciones climáticas entre 2020 y 2024 han afectado el consumo global de energía.
    
    **¿Qué encontrarás aquí?**
    * **Tendencias Temporales:** Evolución del consumo año tras año.
    * **Correlaciones:** Impacto de la temperatura en la demanda eléctrica.
    * **Distribuciones:** Comportamiento de las variables energéticas.
    
    ---
    **👤 Autor:** Miguel Sierra  
    *Nivel: Integrador - Análisis de Datos*
    """)
    
    if st.button("🚀 Comenzar Análisis"):
        st.info("Por favor, selecciona 'Dashboard de Análisis' en el menú de la izquierda.")

# --- PÁGINA 2: PANEL DE TRABAJO ---
else:
    st.title("📊 Panel de Trabajo Integrador")
    
    with st.status("📥 Conectando con el dataset de Kaggle...", expanded=True) as status:
        df = get_data()
        if df is not None:
            status.update(label="✅ ¡Datos cargados con éxito!", state="complete", expanded=False)
        else:
            status.update(label="❌ Error al cargar datos", state="error")

    if df is not None:
        # Pestañas para organizar los gráficos
        tab1, tab2, tab3 = st.tabs(["📈 Tendencias", "🌡️ Correlaciones", "📊 Distribución"])

        with tab1:
            st.subheader("Evolución del Consumo Energético")
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            # Usamos las primeras dos columnas como fallback si no conocemos los nombres exactos
            sns.lineplot(data=df, x=df.columns[0], y=df.columns[1], ax=ax1, color='#2ecc71', linewidth=2)
            plt.xticks(rotation=45)
            st.pyplot(fig1)
            st.info("**Explicación:** Este gráfico lineal permite visualizar la estacionalidad del consumo. Los picos suelen coincidir con meses de verano o invierno extremo.")

        with tab2:
            st.subheader("Impacto Climático en la Energía")
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            sns.scatterplot(data=df, x=df.columns[2], y=df.columns[1], hue=df.columns[1], palette="magma", ax=ax2)
            st.pyplot(fig2)
            st.info("**Explicación:** El diagrama de dispersión muestra la relación entre temperatura y demanda. Una tendencia clara indicaría una dependencia directa del clima.")

        with tab3:
            st.subheader("Histograma de Consumo")
            fig3, ax3 = plt.subplots(figsize=(10, 4))
            sns.histplot(df[df.columns[1]], kde=True, color="#3498db", ax=ax3)
            st.pyplot(fig3)
            st.info("**Explicación:** Aquí observamos la concentración de los datos. La curva KDE nos ayuda a entender si el consumo energético es constante o varía drásticamente.")
            
        # Mostrar tabla de datos opcional
        with st.expander("👀 Ver datos crudos"):
            st.dataframe(df.head(10))

# Pie de página lateral
st.sidebar.markdown("---")
st.sidebar.caption("Proyecto Talento Tech | 2024")
