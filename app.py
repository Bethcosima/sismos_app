import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium

pipeline = joblib.load('modelo_sismos.pkl')

st.title("Predicción de Magnitud de los Sismos en CDMX")

#inputs del usuario
st.header("Ingresa los datos del sismo")

anio = st.number_input("Año", 1900,2100,2025)
mes = st.selectbox("Mes", list(range(1,13)))
dia = st.number_input("Día", 1,31,1)
dia_semana = st.selectbox("Día de la semana (0= lunes, 6= Domingo)", list(range(7)))
hora = st.slider("Hora", 0, 23,12)
latitud = st.number_input("Latitud", value= 19.36)
longitud = st.number_input("Longitud", value= -99.2)
profundidad = st.number_input("Profundidad (km)", value= 1.0)

#contenedor para resultado
resultado = st.empty()
prediccion_hecha = False
magnitud_predicha = None

if st.button("Predecir magnitud"):
    entrada = pd.DataFrame([{
        'Año': anio,
        'Mes': mes,
        'Dia': dia,
        'Dia_semana': dia_semana,
        'Hora': hora,
        'Latitud': latitud,
        'Longitud': longitud,
        'Profundidad': profundidad
    }])

    magnitud_predicha = pipeline.predict(entrada)[0]
    resultado.success(f"Magnitud estimada: {magnitud_predicha:.2f}")
    prediccion_hecha = True

# Mostramos el mapa con datos reales

st.subheader("🗺️ Mapa Histórico de sismos en CDMX")


#cargamos dataset limpio

df= pd.read_csv('Data/sismos_cdmx_cleanData.csv')

#crear mapa centrado en CDMX

mapa = folium.Map(location= [19.36,-99.13], zoom_start= 10)

#añadimos puntos al mapa

for _,row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitud'], row['Longitud']],
        radius = 3,
        popup = f"{row['Fecha']} - M{row['Magnitud']:.1f}",
        color = 'red' if row['Magnitud'] >=2 else 'blue',
        fill= True,
        fill_opacity = 0.7

    ).add_to(mapa)

# si hay una prediccion, agregamos el punto del usuario
if prediccion_hecha:
    folium.Marker(
        location = [latitud, longitud],
        popup= f"Prediccion: M{magnitud_predicha:.2f}",
        icon = folium.Icon(color='green', icon= 'info-sign')
    ).add_to(mapa)
    
#mostrar en streamlit
st_folium(mapa, width=700, height= 500)