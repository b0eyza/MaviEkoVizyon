import streamlit as st
import requests
import numpy as np

st.set_page_config(page_title="Ulva lactuca - Çanakkale Modeli")

st.title("🌊 Ulva lactuca Büyüme Modeli")
st.write("Pilot Bölge: Çanakkale Boğazı")

# ---------------------------
# Deniz yüzeyi sıcaklığı çekme
# ---------------------------
@st.cache_data
def get_sst():
    url = "https://marine-api.open-meteo.com/v1/marine?latitude=40.15&longitude=26.40&daily=sea_surface_temperature_max&timezone=Europe/Istanbul"
    response = requests.get(url)
    data = response.json()
    temps = data["daily"]["sea_surface_temperature_max"]
    return temps

try:
    sst_data = get_sst()
except:
    st.error("Deniz verisi alınamadı.")
    st.stop()

# ---------------------------
# Model parametreleri
# ---------------------------
r = st.slider("Büyüme katsayısı (r)", 0.05, 1.0, 0.3)
K = st.slider("Taşıma kapasitesi (K)", 500, 5000, 1500)
optimal_temp = st.slider("Optimum sıcaklık (°C)", 10.0, 25.0, 18.0)
sigma = st.slider("Sıcaklık toleransı", 1.0, 10.0, 5.0)

# ---------------------------
# Büyüme modeli
# ---------------------------
biomass = 100
biomass_list = []

for temp in sst_data:
    temp_factor = np.exp(-((temp - optimal_temp) ** 2) / (2 * sigma ** 2))
    growth = r * biomass * (1 - biomass / K) * temp_factor
    biomass += growth
    biomass_list.append(biomass)

# ---------------------------
# Grafik
# ---------------------------
st.subheader("Deniz Yüzeyi Sıcaklığı (°C)")
st.line_chart(sst_data)

st.subheader("Tahmini Ulva Biyokütlesi")
st.line_chart(biomass_list)

# ---------------------------
# Risk analizi
# ---------------------------
if biomass_list[-1] > K * 0.8:
    st.error("⚠️ Yüksek Bloom Riski")
elif biomass_list[-1] > K * 0.5:
    st.warning("⚠️ Orta Seviye Risk")
else:
    st.success("🌱 Düşük Risk")
