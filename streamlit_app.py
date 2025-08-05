import streamlit as st
import pandas as pd
from invoice_parser import parse_invoice

st.set_page_config(page_title="Taric AI-Mentor – demo")

st.title("📄 Factura → ENS demo")

pdf = st.file_uploader("Sube una factura (PDF)", type=["pdf"])
if pdf:
    tmp_path = "/tmp/invoice.pdf"
    with open(tmp_path, "wb") as f:
        f.write(pdf.read())

    with st.spinner("Extrayendo datos con Azure…"):
        df = parse_invoice(tmp_path)

    st.success("Extracción completada")
    st.dataframe(df, use_container_width=True)

    st.button("Clasificar (próximo paso)", disabled=True)
else:
    st.info("Cargaré tu factura aquí y te mostraré los datos extraídos")
