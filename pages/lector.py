import streamlit as st
import cv2
from pyzbar.pyzbar import decode
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import sqlite3
import pandas as pd

st.title("📷 Lector de código de barras")

conn = sqlite3.connect("database.db", check_same_thread=False)

class BarcodeScanner(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        codigos = decode(img)

        for codigo in codigos:
            datos = codigo.data.decode("utf-8")
            st.session_state["codigo_detectado"] = datos

            pts = codigo.polygon
            if len(pts) == 4:
                pts = [(p.x, p.y) for p in pts]
                cv2.polylines(img, [cv2.convexHull(
                    cv2.UMat(
                        cv2.array(pts)
                    )
                )], True, (0, 255, 0), 2)

        return img

webrtc_streamer(
    key="lector",
    video_transformer_factory=BarcodeScanner
)

if "codigo_detectado" in st.session_state:
    codigo = st.session_state["codigo_detectado"]
    st.success(f"Código detectado: {codigo}")

    try:
        producto = pd.read_sql_query(
            f"SELECT * FROM productos WHERE codigo='{codigo}'",
            conn
        )

        if not producto.empty:
            st.dataframe(producto, use_container_width=True)
        else:
            st.warning("Producto no encontrado")
    except:
        st.error("Aún no hay productos con código registrado")