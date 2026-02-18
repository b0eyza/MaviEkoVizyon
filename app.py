import streamlit as st
import streamlit.components.v1 as components

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

st.set_page_config(layout="wide")
components.html(html_code, height=2000, scrolling=True)
