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
import requests

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.15&longitude=26.40&daily=temperature_2m_max,sunshine_duration&timezone=auto"
    response = requests.get(url)
    data = response.json()
    
    temp = data["daily"]["temperature_2m_max"][0]
    sun = data["daily"]["sunshine_duration"][0] / 3600  # saniyeden saate
    
    return temp, sun
