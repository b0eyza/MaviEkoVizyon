import streamlit as st
import requests
import math
import matplotlib.pyplot as plt

st.title("Ulva lactuca Akıllı Büyüme Simülasyonu - Çanakkale")

# --- GERÇEK HAVA VERİSİ ---
def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.15&longitude=26.40&daily=temperature_2m_max,sunshine_duration&timezone=auto"
    response = requests.get(url)
    data = response.json()

    temp = data["daily"]["temperature_2m_max"][0]
    sun_hours = data["daily"]["sunshine_duration"][0] / 3600

    return temp, sun_hours

temperature, sun_hours = get_weather()

st.write("Bugünkü maksimum sıcaklık (°C):", temperature)
st.write("Bugünkü güneşlenme süresi (saat):", round(sun_hours, 2))

# --- KULLANICI GİRDİSİ ---
initial_biomass = st.number_input("Başlangıç biyokütle (gram)", value=100)

# --- MODEL PARAMETRELERİ ---
r = 0.25   # maksimum büyüme oranı
K = 1500   # taşıma kapasitesi
opt_temp = 20
sigma = 5  # sıcaklık tolerans aralığı

# --- SICAKLIK FONKSİYONU (GAUSSIAN) ---
temp_factor = math.exp(-((temperature - opt_temp) ** 2) / (2 * sigma ** 2))

# --- IŞIK FAKTÖRÜ ---
light_factor = min(1, sun_hours / 10)

environment_factor = temp_factor * light_factor

# --- 30 GÜNLÜK SİMÜLASYON ---
days = 30
biomass = initial_biomass
biomass_list = []
growth_rates = []

for day in range(days):
    growth = r * biomass * (1 - biomass / K)
    biomass = biomass + growth * environment_factor
    biomass_list.append(biomass)
    growth_rates.append(growth * environment_factor)

# --- GRAFİK ---
st.subheader("30 Günlük Biyokütle Değişimi")

fig, ax = plt.subplots()
ax.plot(biomass_list)
ax.set_xlabel("Gün")
ax.set_ylabel("Biyokütle (gram)")
st.pyplot(fig)

st.subheader("30 Gün Sonraki Tahmini Biyokütle:")
st.write(round(biomass_list[-1], 2), "gram")

# --- AKILLI UYARI SİSTEMİ ---
if temperature > 28:
    st.warning("Yüksek sıcaklık! Termal stres riski.")

if biomass_list[-1] > K * 0.8:
    st.warning("Alg patlaması (bloom) riski artıyor!")

if sum(growth_rates[-5:]) < 0:
    st.warning("Son günlerde büyüme düşüşte. Stres faktörü olabilir.")

if sun_hours < 4:
    st.warning("Düşük ışık seviyesi büyümeyi baskılıyor.")
