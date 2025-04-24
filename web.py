
import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime

# Cargar archivo con la columna "Ubicacion" ya generada
fecha = datetime.now().strftime("%Y-%m-%d")
df = pd.read_excel(f"airbnb_scrape_{fecha}.xlsx")

# Título de la app
st.title("Análisis de Alojamientos en Airbnb")

# Filtro de ubicación
ubicaciones = df["Ubicacion"].unique()
ubicacion_seleccionada = st.selectbox("Filtrar por ubicación", sorted(ubicaciones))

# Mostrar los datos filtrados
df_filtrado = df[df["Ubicacion"] == ubicacion_seleccionada].copy()

df_filtrado["Precio"] =(
    df_filtrado["Precio"].astype(str)
    .str.replace("S/","",regex=False)
    .str.strip()
)

df_filtrado["Precio"] = pd.to_numeric(df_filtrado["Precio"], errors="coerce")
df_filtrado = df_filtrado.dropna(subset=["Precio"])

st.dataframe(df_filtrado)

# Verificar si existe la columna "Precio"

bins = [100, 120, 140, 160, 180, 200, 230, 250, 300, float("inf")]
etiquetas = ["100-119", "120-139", "140-159", "160-179", "180-199", 
                "200-229", "230-249", "250-299", "300+"]

df_filtrado["RangoPrecio"] = pd.cut(df_filtrado["Precio"], bins=bins, labels=etiquetas, right=False)

    # Contar cuántos alojamientos hay por rango
conteo_rangos = df_filtrado["RangoPrecio"].value_counts().sort_index().reset_index()
conteo_rangos.columns = ["RangoPrecio", "Cantidad"]

    # Crear gráfico de líneas
chart = alt.Chart(conteo_rangos).mark_line(point=True).encode(
    x=alt.X("RangoPrecio", sort=etiquetas, title="Rango de Precios (S/)"),
    y=alt.Y("Cantidad", title="Cantidad de Alojamientos"),
    tooltip=["RangoPrecio", "Cantidad"]
).properties(
    title=f"Distribución de Precios en {ubicacion_seleccionada}",
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)



