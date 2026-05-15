import streamlit as st
import sqlite3
import pandas as pd
import os
import time
from utils.barcode_generator import generar_codigo

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# asegurar columna codigo e imagen
try:
    cursor.execute("ALTER TABLE productos ADD COLUMN codigo TEXT")
    conn.commit()
except:
    pass

try:
    cursor.execute("ALTER TABLE productos ADD COLUMN imagen TEXT")
    conn.commit()
except:
    pass

st.title("📦 Inventario")

with st.form("producto_form"):
    nombre = st.text_input("Nombre")
    categoria = st.text_input("Categoría")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    minimo = st.number_input("Stock mínimo", min_value=0)
    imagen = st.file_uploader("Imagen del producto", type=["png", "jpg", "jpeg"])

    guardar = st.form_submit_button("Guardar")

    if guardar:
        codigo = str(int(time.time()))
        ruta_imagen = ""

        if imagen is not None:
            ruta_imagen = f"uploads/{imagen.name}"
            with open(ruta_imagen, "wb") as f:
                f.write(imagen.getbuffer())

        cursor.execute(
            """
            INSERT INTO productos (nombre,categoria,precio,stock,minimo,codigo,imagen)
            VALUES (?,?,?,?,?,?,?)
            """,
            (nombre, categoria, precio, stock, minimo, codigo, ruta_imagen)
        )
        conn.commit()
        st.success("Producto agregado")

                cursor.execute(
            "INSERT INTO movimientos (producto, tipo, cantidad) VALUES (?, ?, ?)",
            (nombre, "entrada", stock)
        )
        conn.commit()

st.subheader("Lista de productos")

df = pd.read_sql_query("SELECT * FROM productos", conn)

if not df.empty:
    st.dataframe(df, use_container_width=True)

    producto = st.selectbox("Ver detalle", df["nombre"])
    fila = df[df["nombre"] == producto].iloc[0]

    if fila["imagen"] and os.path.exists(fila["imagen"]):
        st.image(fila["imagen"], width=220)

    codigo_img = generar_codigo(fila["codigo"])
    st.image(codigo_img, caption=f"Código: {fila['codigo']}")