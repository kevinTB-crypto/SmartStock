import streamlit as st
import sqlite3
import pandas as pd
from utils.db import crear_tablas

crear_tablas()

st.title("📜 Historial de movimientos")

conn = sqlite3.connect("database.db", check_same_thread=False)

try:
    movimientos = pd.read_sql_query(
        "SELECT * FROM movimientos ORDER BY id DESC",
        conn
    )

    if not movimientos.empty:
        st.dataframe(movimientos, use_container_width=True)
    else:
        st.info("Aún no hay movimientos registrados")
except:
    st.warning("La tabla se creará al primer movimiento")