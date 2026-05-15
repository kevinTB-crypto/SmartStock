import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

st.title('📦 Inventario')

with st.form('producto_form'):
    nombre = st.text_input('Nombre del producto')
    categoria = st.text_input('Categoría')
    precio = st.number_input('Precio', min_value=0.0)
    stock = st.number_input('Stock', min_value=0)
    minimo = st.number_input('Stock mínimo', min_value=0)
    guardar = st.form_submit_button('Guardar')

    if guardar:
        cursor.execute(
            'INSERT INTO productos (nombre,categoria,precio,stock,minimo) VALUES (?,?,?,?,?)',
            (nombre, categoria, precio, stock, minimo)
        )
        conn.commit()
        st.success('Producto agregado')

st.subheader('Lista de productos')

df = pd.read_sql_query('SELECT * FROM productos', conn)
st.dataframe(df, use_container_width=True)