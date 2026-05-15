import streamlit as st
import sqlite3
import pandas as pd

# conexión
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

st.title('💰 Registro de Ventas')

# obtener productos
productos = pd.read_sql_query("SELECT * FROM productos", conn)

if productos.empty:
    st.warning("No hay productos registrados en inventario.")
else:
    nombres = productos['nombre'].tolist()

    producto_seleccionado = st.selectbox("Selecciona producto", nombres)

    fila = productos[productos['nombre'] == producto_seleccionado].iloc[0]
    stock_actual = int(fila['stock'])
    precio = float(fila['precio'])

    st.info(f"Stock disponible: {stock_actual}")
    st.info(f"Precio: ${precio:.2f}")

    cantidad = st.number_input(
        "Cantidad a vender",
        min_value=1,
        max_value=stock_actual if stock_actual > 0 else 1,
        step=1
    )

    if st.button("Registrar venta"):
        if stock_actual <= 0:
            st.error("Este producto ya no tiene stock.")
        elif cantidad > stock_actual:
            st.error("No hay suficiente stock.")
        else:
            total = cantidad * precio
            nuevo_stock = stock_actual - cantidad

            # guardar venta
            cursor.execute(
                "INSERT INTO ventas (producto, cantidad, total) VALUES (?, ?, ?)",
                (producto_seleccionado, cantidad, total)
            )

            # actualizar inventario
            cursor.execute(
                "UPDATE productos SET stock = ? WHERE nombre = ?",
                (nuevo_stock, producto_seleccionado)
            )

            conn.commit()

            st.success(f"Venta registrada correctamente. Total: ${total:.2f}")
            st.rerun()

# historial de ventas
st.subheader("📋 Historial de ventas")

ventas = pd.read_sql_query("SELECT * FROM ventas ORDER BY id DESC", conn)

if not ventas.empty:
    st.dataframe(ventas, use_container_width=True)
else:
    st.info("Aún no hay ventas registradas.")