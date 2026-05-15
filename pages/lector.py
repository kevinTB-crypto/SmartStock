import streamlit as st
import sqlite3
import pandas as pd

st.title("🔎 Buscar producto por código")

conn = sqlite3.connect("database.db", check_same_thread=False)

codigo = st.text_input("Ingresa el código del producto")

if st.button("Buscar"):
    if codigo:
        try:
            producto = pd.read_sql_query(
                "SELECT * FROM productos WHERE codigo=?",
                conn,
                params=(codigo,)
            )

            if not producto.empty:
                st.success("Producto encontrado")
                st.dataframe(producto, use_container_width=True)
            else:
                st.warning("No existe producto con ese código")
        except:
            st.error("La columna código aún no existe en algunos registros")