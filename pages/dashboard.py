import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from utils.db import crear_tablas

crear_tablas()

conn = sqlite3.connect("database.db", check_same_thread=False)

productos = pd.read_sql_query("SELECT * FROM productos", conn)
ventas = pd.read_sql_query("SELECT * FROM ventas", conn)

# detectar productos bajos
if not productos.empty:
    productos_bajos = productos[productos["stock"] <= productos["minimo"]]
else:
    productos_bajos = pd.DataFrame()
st.title("📊 Dashboard SmartStock")

if not productos_bajos.empty:
    st.error(f"⚠ Hay {len(productos_bajos)} producto(s) con stock bajo")
else:
    st.success("✅ Todo el inventario está en buen estado")

if not productos_bajos.empty:
    st.audio(
        "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"
    )

# métricas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total productos", len(productos))

with col2:
    total_stock = int(productos["stock"].sum()) if not productos.empty else 0
    st.metric("Stock total", total_stock)

with col3:
    total_ventas = len(ventas)
    st.metric("Ventas registradas", total_ventas)

# alertas
st.subheader("⚠ Productos con bajo stock")

if not productos.empty:
    bajos = productos[productos["stock"] <= productos["minimo"]]
    if not bajos.empty:
        st.dataframe(bajos, use_container_width=True)
        st.warning("Hay productos por agotarse")
    else:
        st.success("Todo el inventario está en buen estado")

# gráfica inventario
st.subheader("📦 Stock por producto")

if not productos.empty:
    fig = px.bar(
        productos,
        x="nombre",
        y="stock",
        title="Cantidad disponible",
        text="stock"
    )
    st.plotly_chart(fig, use_container_width=True)

# gráfica ventas
st.subheader("💰 Historial de ventas")

if not ventas.empty:
    resumen = ventas.groupby("producto")["cantidad"].sum().reset_index()

    fig2 = px.pie(
        resumen,
        names="producto",
        values="cantidad",
        title="Productos más vendidos"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Aún no hay ventas para mostrar")

st.subheader("🚨 Productos críticos")

if not productos_bajos.empty:
    st.dataframe(productos_bajos, use_container_width=True)
else:
    st.info("No hay productos críticos")