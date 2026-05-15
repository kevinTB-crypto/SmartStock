import streamlit as st
import sqlite3
import pandas as pd
import time
from utils.barcode_generator import generar_codigo

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

st.title("📦 Inventario")

with st.form("producto_form"):
    nombre = st.text_input("Nombre")
    categoria = st.text_input("Categoría")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    minimo = st.number_input("Stock mínimo", min_value=0)

    guardar = st.form_submit_button("Guardar")

    if guardar:
        codigo = int(time.time())  # genera ID único

        try:
            cursor.execute("""
                ALTER TABLE productos ADD COLUMN codigo TEXT
            """)
            conn.commit()
        except:
            pass

        cursor.execute(
            "INSERT INTO productos (nombre,categoria,precio,stock,minimo,codigo) VALUES (?,?,?,?,?,?)",
            (nombre, categoria, precio, stock, minimo, str(codigo))
        )
        conn.commit()
        st.success("Producto agregado")

st.subheader("Productos")

df = pd.read_sql_query("SELECT * FROM productos", conn)

if not df.empty:
    st.dataframe(df, use_container_width=True)

    producto = st.selectbox("Ver código de barras", df["nombre"])
    fila = df[df["nombre"] == producto].iloc[0]

    codigo_img = generar_codigo(fila["codigo"])
    st.image(codigo_img, caption=f"Código: {fila['codigo']}")