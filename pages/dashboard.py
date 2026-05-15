import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db', check_same_thread=False)

df = pd.read_sql_query('SELECT * FROM productos', conn)

st.title('📊 Dashboard')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Total productos', len(df))

with col2:
    st.metric('Stock total', int(df['stock'].sum()) if not df.empty else 0)

with col3:
    bajos = len(df[df['stock'] <= df['minimo']]) if not df.empty else 0
    st.metric('Alertas', bajos)

st.subheader('Productos con bajo stock')

if not df.empty:
    alertas = df[df['stock'] <= df['minimo']]
    st.dataframe(alertas, use_container_width=True)

    if not alertas.empty:
        st.warning('Hay productos por agotarse')
else:
    st.info('No hay productos registrados')