import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

st.title("📑 Reportes")

conn = sqlite3.connect("database.db", check_same_thread=False)

productos = pd.read_sql_query("SELECT * FROM productos", conn)
ventas = pd.read_sql_query("SELECT * FROM ventas", conn)

tab1, tab2 = st.tabs(["Inventario", "Ventas"])

with tab1:
    st.subheader("Reporte de inventario")
    st.dataframe(productos, use_container_width=True)

    if not productos.empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            productos.to_excel(writer, index=False, sheet_name="Inventario")
        st.download_button(
            "Descargar inventario Excel",
            data=output.getvalue(),
            file_name="inventario.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with tab2:
    st.subheader("Reporte de ventas")
    st.dataframe(ventas, use_container_width=True)

    if not ventas.empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            ventas.to_excel(writer, index=False, sheet_name="Ventas")
        st.download_button(
            "Descargar ventas Excel",
            data=output.getvalue(),
            file_name="ventas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )