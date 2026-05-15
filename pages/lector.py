import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import sqlite3
import pandas as pd

st.title("📷 Lector de código de barras")

conn = sqlite3.connect("database.db", check_same_thread=False)

archivo = st.file_uploader(
    "Sube una imagen del código de barras",
    type=["png", "jpg", "jpeg"]
)

if archivo is not None:
    imagen = Image.open(archivo)
    st.image(imagen, caption="Imagen subida", use_container_width=True)

    codigos = decode(imagen)

    if codigos:
        codigo = codigos[0].data.decode("utf-8")
        st.success(f"Código detectado: {codigo}")

        try:
            producto = pd.read_sql_query(
                "SELECT * FROM productos WHERE codigo=?",
                conn,
                params=(codigo,)
            )

            if not producto.empty:
                st.dataframe(producto, use_container_width=True)
            else:
                st.warning("Producto no encontrado")
        except Exception as e:
            st.error(f"Error al buscar producto: {e}")
    else:
        st.warning("No se detectó ningún código")