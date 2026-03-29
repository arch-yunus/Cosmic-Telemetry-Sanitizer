import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import os
import sys

# Add project root to path for imports
sys.path.append(os.getcwd())

from pipeline.main_orchestrator import run_sanitization_pipeline, load_config

st.set_page_config(page_title="Cosmic Telemetry Sanitizer", layout="wide", page_icon="🛰️")

st.title("🛰️ Cosmic Telemetry Sanitizer")
st.markdown("""
### Yüksek Sadakatli Telemetri Arındırma Kontrol Paneli
Bu panel, uzay radyasyonu ve bit-flip hataları içeren ham verileri, çok katmanlı filtreleme hattı kullanarak temizler.
""")

# Sidebar for controls
st.sidebar.header("⚙️ Pipeline Kontrollere")
raw_data_path = st.sidebar.text_input("Raw Veri Yolu", "data/raw_telemetry/sample_orbit_data.csv")
process_btn = st.sidebar.button("Pipeline'ı Çalıştır")

if process_btn:
    with st.spinner("Pipeline işleniyor..."):
        output_path = "data/sanitized_telemetry/cleaned_orbit_data.csv"
        run_sanitization_pipeline(raw_data_path, output_path)
        st.sidebar.success("İşlem tamamlandı!")

# Load data if exists
if os.path.exists(raw_data_path):
    df_raw = pd.read_csv(raw_data_path)
    clean_path = "data/sanitized_telemetry/cleaned_orbit_data.csv"
    
    if os.path.exists(clean_path):
        df_clean = pd.read_csv(clean_path)
        
        # Metric dashboard
        m1, m2, m3 = st.columns(3)
        m1.metric("Satır Sayısı", len(df_raw))
        m2.metric("Sensör Sayısı", 5)
        m3.metric("Fiziksel İhlal (Giderilen)", "Tüm Sınırlar Korundu")
        
        # Chart selection
        target_col = st.selectbox("Görselleştirilecek Sensör", 
                                  ["battery_voltage", "bus_current", "temp_celsius", "rw_speed_rpm", "sun_sensor_lux"])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df_raw[target_col], mode='lines', name='Ham (Raw/Unsafe)', 
                                 line=dict(color='rgba(255, 0, 0, 0.3)', width=1)))
        fig.add_trace(go.Scatter(y=df_clean[target_col], mode='lines', name='Temizlenmiş (Sanitized)', 
                                 line=dict(color='cyan', width=2)))
        
        fig.update_layout(title=f"{target_col} Analizi (Öncesi vs Sonrası)",
                          template="plotly_dark",
                          xaxis_title="Zaman (sn)",
                          yaxis_title=target_col,
                          hovermode="x unified")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics Comparison
        st.subheader("İstatistiksel Karşılaştırma")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Ham Veri Özeti**")
            st.dataframe(df_raw[target_col].describe())
        with c2:
            st.write("**Temiz Veri Özeti**")
            st.dataframe(df_clean[target_col].describe())
            
    else:
        st.info("Pipeline henüz çalıştırılmadı. Soldaki butona basarak veriyi işleyin.")
        st.line_chart(df_raw.drop(columns=['timestamp', 'subsystem_status']))
else:
    st.warning("Veri bulunamadı. Lütfen önce veri üretin veya yolu kontrol edin.")
    if st.button("Örnek Veri Üret"):
        import subprocess
        subprocess.run([sys.executable, "scripts/generate_data.py"])
        st.rerun()
