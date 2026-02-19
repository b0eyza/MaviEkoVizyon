import streamlit as st
import streamlit.components.v1 as components

# Streamlit'in kendi arayüzünü tamamen gizle
st.set_page_config(layout="wide", page_title="SeaYield", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important;}
    iframe {border: none !important;}
    </style>
    """, unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Tam ekran yüksekliği veriyoruz (Apple hissi için)
components.html(html_code, height=1500, scrolling=False)
