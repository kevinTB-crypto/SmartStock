import streamlit as st
import sqlite3
import pandas as pd
from utils.db import crear_tablas

# asegurar que exista la tabla
crear_tablas()

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

st.title("💰 Registro de Ventas")

productos = pd.read_sql_query("SELECT * FROM productos", conn)

if productos.empty:
    st.warning("No hay productos registrados.")
else:
    nombres = productos["nombre"].tolist()
    producto = st.selectbox("Producto", nombres)

    fila = productos[productos["nombre"] == producto].iloc[0]
    stock = int(fila["stock"])
    precio = float(fila["precio"])

    st.write(f"Stock disponible: {stock}")
    st.write(f"Precio: ${precio}")

    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        max_value=max(stock, 1),
        step=1
    )

    if st.button("Vender"):
        if stock >= cantidad:
            total = precio * cantidad

            cursor.execute(
                "INSERT INTO ventas (producto, cantidad, total) VALUES (?, ?, ?)",
                (producto, cantidad, total)
            )

            cursor.execute(
                "UPDATE productos SET stock = ? WHERE nombre = ?",
                (stock - cantidad, producto)
            )

            conn.commit()
            st.success("Venta registrada")
            st.rerun()
        else:
            st.error("Stock insuficiente")

            cursor.execute(
                "INSERT INTO movimientos (producto, tipo, cantidad) VALUES (?, ?, ?)",
                (producto, "venta", cantidad)
            )

st.subheader("Historial de ventas")

try:
    ventas = pd.read_sql_query("SELECT * FROM ventas ORDER BY id DESC", conn)
    if not ventas.empty:
        st.dataframe(ventas, use_container_width=True)
    else:
        st.info("Sin ventas registradas")
except:
    st.info("La tabla de ventas se creará automáticamente al registrar la primera venta")