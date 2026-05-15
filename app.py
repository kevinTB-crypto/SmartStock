import streamlit as st
from utils.db import crear_tablas

st.set_page_config(page_title='SmartStock', layout='wide')
crear_tablas()

st.title('📦 SmartStock')
st.write('Sistema de inventario')