import streamlit as st
import sqlite3
import pandas as pd
from utils.db import crear_tablas

crear_tablas()

st.title("⚙ Panel Administrador")

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

df = pd.read_sql_query("SELECT * FROM productos", conn)

if df.empty:
    st.warning("No hay productos registrados")
else:
    st.subheader("Editar / Eliminar productos")

    producto = st.selectbox("Selecciona producto", df["nombre"])
    fila = df[df["nombre"] == producto].iloc[0]

    nuevo_nombre = st.text_input("Nombre", fila["nombre"])
    nueva_categoria = st.text_input("Categoría", fila["categoria"])
    nuevo_precio = st.number_input("Precio", value=float(fila["precio"]))
    nuevo_stock = st.number_input("Stock", value=int(fila["stock"]))
    nuevo_minimo = st.number_input("Mínimo", value=int(fila["minimo"]))

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Guardar cambios"):
            cursor.execute("""
                UPDATE productos
                SET nombre=?, categoria=?, precio=?, stock=?, minimo=?
                WHERE id=?
            """, (
                nuevo_nombre,
                nueva_categoria,
                nuevo_precio,
                nuevo_stock,
                nuevo_minimo,
                int(fila["id"])
            ))
            conn.commit()
            st.success("Producto actualizado")
            st.rerun()

    with col2:
        if st.button("Eliminar producto"):
            cursor.execute(
                "DELETE FROM productos WHERE id=?",
                (int(fila["id"]),)
            )
            conn.commit()
            st.warning("Producto eliminado")
            st.rerun()

st.subheader("📋 Inventario actual")
st.dataframe(df, use_container_width=True)