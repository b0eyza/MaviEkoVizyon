import streamlit as st
import pandas as pd
import numpy as np

# Uygulama Başlığı ve Tema Ayarı
st.set_page_config(page_title="Mavi Eko Vizyon | SeaYield", layout="wide", page_icon="🌊")

# Üst Başlık
st.title("🌊 Mavi Eko Vizyon: SeaYield")
st.subheader("Akıllı Yosun Yetiştiriciliği ve Karbon Yönetim Paneli")
st.markdown("---")

# --- SOL PANEL: KONTROL MERKEZİ ---
with st.sidebar:
    st.header("⚙️ Proje Ayarları")
    ulke = st.selectbox("Analiz Edilecek Ülke", ["Türkiye", "Yunanistan", "İtalya", "İspanya"])
    bolge = st.text_input("Bölge Seçimi", "Çanakkale Dardanos")
    
    st.markdown("---")
    st.header("🌱 Üretim Parametreleri")
    yosun_turu = st.selectbox("Yosun Türü", 
                                ["Posidonia oceanica (Deniz Eriştesi)", 
                                 "Ulva lactuca (Deniz Marulu)", 
                                 "Gracilaria (Kırmızı Alg)"])
    
    hedef_alan = st.number_input("Planlanan Üretim Alanı (m2)", min_value=100, value=5000)
    yatirim_suresi = st.slider("Proje Süresi (Ay)", 1, 36, 12)
    
    st.button("Analizi Güncelle")

# --- ANA PANEL: ANALİZ VE GRAFİKLER ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Bölgesel Uygunluk ve Mevcut Stok")
    st.info(f"📍 {ulke} - {bolge} bölgesi uydudan analiz ediliyor...")
    # Temsili analiz görseli
    st.image("https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&q=80&w=1000", 
             caption="Sentinel-2 Uydu Analiz Katmanı (Biyokütle Yoğunluğu)")

with col2:
    st.subheader("📊 Ekonomik Projeksiyon")
    
    # Tür bazlı katsayı hesaplama
    k_katsayi = 1.4 if "Posidonia" in yosun_turu else 0.8
    tahmini_karbon = (hedef_alan * k_katsayi) / 1000
    karbon_geliri = tahmini_karbon * 85 # 85 Euro/Ton (ETS Fiyatı)
    
    st.metric("Tahmini Karbon Kredisi (Ton)", f"{tahmini_karbon:.2f}")
    st.metric("Tahmini Karbon Geliri (€)", f"€{karbon_geliri:,.2f}")
    st.success(f"Tür Uygunluk Skoru: %92 (Optimum)")

st.markdown("---")

# --- GRAFİKLER ---
st.subheader("📈 Zaman Serisi Analizi")
tab_growth, tab_carbon = st.tabs(["Aylık Büyüme Hızı", "Karbon Birikimi"])

with tab_growth:
    chart_data = pd.DataFrame(np.random.randn(yatirim_suresi, 1) + 50, columns=['Biyokütle (kg)'])
    st.line_chart(chart_data)

with tab_carbon:
    carbon_data = pd.DataFrame(np.random.randn(yatirim_suresi, 1).cumsum() + 10, columns=['Karbon Stok (Ton)'])
    st.area_chart(carbon_data)

# --- MÜHENDİSLİK NOTLARI ---
st.subheader("🔍 Mühendislik ve AI Tavsiyeleri")
st.warning(f"ℹ️ **Akustik Entegrasyon:** {bolge} bölgesindeki akıntı hızı dikkate alındığında, besleme sistemini kıyıdan 150m açığa kurmanız önerilir.")
st.error("🚨 **Kirlilik Uyarısı:** Bölgede müsilaj riski düşük, su berraklığı yosun gelişimi için ideal seviyededir.")
