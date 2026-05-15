import streamlit as st
import sqlite3
import pandas as pd
import os
import time
from utils.barcode_generator import generar_codigo
from utils.db import crear_tablas

crear_tablas()

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# asegurar columnas extra
for columna, tipo in [("codigo", "TEXT"), ("imagen", "TEXT")]:
    try:
        cursor.execute(f"ALTER TABLE productos ADD COLUMN {columna} {tipo}")
        conn.commit()
    except:
        pass

st.title("📦 Inventario")

# formulario
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
            os.makedirs("uploads", exist_ok=True)
            ruta_imagen = f"uploads/{imagen.name}"
            with open(ruta_imagen, "wb") as f:
                f.write(imagen.getbuffer())

        cursor.execute("""
            INSERT INTO productos (nombre, categoria, precio, stock, minimo, codigo, imagen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, categoria, precio, stock, minimo, codigo, ruta_imagen))

        cursor.execute(
            "INSERT INTO movimientos (producto, tipo, cantidad) VALUES (?, ?, ?)",
            (nombre, "entrada", stock)
        )

        conn.commit()
        st.success("Producto agregado")
        st.rerun()

# listado
df = pd.read_sql_query("SELECT * FROM productos", conn)

st.subheader("🔍 Buscar productos")

buscar = st.text_input("Buscar por nombre")
categoria_filtro = st.text_input("Filtrar por categoría")

if not df.empty:
    if buscar:
        df = df[df["nombre"].str.contains(buscar, case=False, na=False)]

    if categoria_filtro:
        df = df[df["categoria"].str.contains(categoria_filtro, case=False, na=False)]

    st.dataframe(df, use_container_width=True)

    producto = st.selectbox("Ver detalle", df["nombre"])
    fila = df[df["nombre"] == producto].iloc[0]

    if fila["imagen"] and os.path.exists(str(fila["imagen"])):
        st.image(str(fila["imagen"]), width=220)

    if fila["codigo"]:
        codigo_img = generar_codigo(str(fila["codigo"]))
        st.image(codigo_img, caption=f"Código: {fila['codigo']}")
else:
    st.info("No hay productos registrados")