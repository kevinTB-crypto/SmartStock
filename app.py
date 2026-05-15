import streamlit as st
import sqlite3
from utils.db import crear_tablas

crear_tablas()

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

st.set_page_config(page_title="SmartStock", layout="wide")

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state.logueado = False

if not st.session_state.logueado:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("## 📦 SmartStock")
        st.markdown("### Iniciar sesión")

        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            cursor.execute(
                "SELECT * FROM usuarios WHERE usuario=? AND password=?",
                (usuario, password)
            )
            user = cursor.fetchone()

            if user:
                st.session_state.logueado = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
else:
    st.title("📦 SmartStock")
    st.success("Sesión iniciada correctamente")
    st.write("Usa el menú lateral para navegar por el sistema.")