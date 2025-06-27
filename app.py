import streamlit as st
import pandas as pd
import joblib

pipeline = joblib.load('Data\modelo_sismos.pkl')

st.title("Predicción de Magnitud de los Sismos en CDMX")

#inputs del usuario

anio = st.number_input("Año", 1900,2100,2025)
mes = st.selectbox("Mes", list(range(1,13)))
dia = st.number_input("Día", 1,31,1)
dia_semana = st.selectbox("Día de la semana (0= lunes, 6= Domingo)", list(range(7)))
hora = st.slider("Hora", 0, 23,12)
latitud = st.number_input("Latitud", value= 19.36)
longitud = st.number_input("Longitud", value= -99.2)
profundidad = st.number_input("Profundidad (km)", value= 1.0)

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

    pred = pipeline.predict(entrada)[0]
    st.success(f"Magnitud estimada: {pred:.2f}")