import streamlit as st
import requests
import math

st.title("Ulva lactuca Büyüme Simülasyonu - Çanakkale")

# --- 1. HAVA VERİSİ ÇEKME ---
def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.15&longitude=26.40&daily=temperature_2m_max,sunshine_duration&timezone=auto"
    response = requests.get(url)
    data = response.json()

    temp = data["daily"]["temperature_2m_max"][0]
    sun_hours = data["daily"]["sunshine_duration"][0] / 3600

    return temp, sun_hours

temperature, sun_hours = get_weather()

st.write("Bugünkü maksimum sıcaklık (°C):", temperature)
st.write("Bugünkü güneşlenme süresi (saat):", round(sun_hours,2))

# --- 2. KULLANICI GİRDİSİ ---
initial_biomass = st.number_input("Başlangıç biyokütle (gram)", value=100)

# --- 3. BASİT BÜYÜME MODELİ ---
# Logistic Growth Model
r = 0.15  # büyüme katsayısı
K = 1000  # taşıma kapasitesi

# Çevresel etki faktörü
temp_factor = max(0, 1 - abs(temperature - 20) / 15)
light_factor = min(1, sun_hours / 12)

environment_factor = temp_factor * light_factor

biomass = initial_biomass

for day in range(7):  # 7 günlük simülasyon
    growth = r * biomass * (1 - biomass / K)
    biomass = biomass + growth * environment_factor

st.subheader("7 Gün Sonraki Tahmini Biyokütle:")
st.write(round(biomass, 2), "gram")

# --- 4. UYARI SİSTEMİ ---
if temperature > 28:
    st.warning("Yüksek sıcaklık! Alg stres altında olabilir.")

if sun_hours < 4:
    st.warning("Düşük ışık seviyesi! Büyüme yavaşlayabilir.")
