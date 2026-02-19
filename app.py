import streamlit as st
import requests
import math
import matplotlib.pyplot as plt

st.title("Ulva lactuca Gelişmiş Büyüme Tahmin Motoru - Çanakkale")

# --- 7 GÜNLÜK TAHMİN VERİSİ ---
def get_weather_forecast():
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.15&longitude=26.40&daily=temperature_2m_max,sunshine_duration&timezone=auto"
    response = requests.get(url)
    data = response.json()

    temps = data["daily"]["temperature_2m_max"][:7]
    sun_hours = [s / 3600 for s in data["daily"]["sunshine_duration"][:7]]

    return temps, sun_hours

temps, sun_hours_list = get_weather_forecast()

st.subheader("Önümüzdeki 7 Günlük Tahmin")
for i in range(7):
    st.write(f"Gün {i+1} - Sıcaklık: {temps[i]} °C | Güneş: {round(sun_hours_list[i],2)} saat")

# --- MODEL PARAMETRELERİ ---
initial_biomass = st.number_input("Başlangıç biyokütle (gram)", value=100)

r = 0.30
K = 1500
opt_temp = 20
sigma = 5

biomass = initial_biomass
biomass_list = []
growth_list = []

# --- 7 GÜNLÜK DİNAMİK SİMÜLASYON ---
for day in range(7):

    temp_factor = math.exp(-((temps[day] - opt_temp) ** 2) / (2 * sigma ** 2))
    light_factor = min(1, sun_hours_list[day] / 10)
    environment_factor = temp_factor * light_factor

    growth = r * biomass * (1 - biomass / K)
    biomass = biomass + growth * environment_factor

    biomass_list.append(biomass)
    growth_list.append(growth * environment_factor)

# --- GRAFİK ---
st.subheader("7 Günlük Dinamik Büyüme")

fig, ax = plt.subplots()
ax.plot(biomass_list)
ax.set_xlabel("Gün")
ax.set_ylabel("Biyokütle (gram)")
st.pyplot(fig)

st.subheader("7 Gün Sonraki Tahmini Biyokütle:")
st.write(round(biomass_list[-1], 2), "gram")

# --- AKILLI ALARM SİSTEMİ ---
if max(growth_list) > 200:
    st.warning("Ani büyüme tespit edildi! Alg patlaması riski.")

if min(growth_list) < 0:
    st.warning("Negatif büyüme! Çevresel stres olabilir.")

if sum(growth_list) < 50:
    st.warning("Genel büyüme düşük. Besin sınırlaması olabilir.")
