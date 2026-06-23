import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
# 1. Menyiapkan data historis sederhana
# Fitur: [Iklan (Juta), Diskon (%)]
X_train = np.array([[5, 10], [10, 20], [15, 5], [20, 25], [25, 15]])
# Target: Keuntungan (Juta)
y_train = np.array([50, 80, 110, 90, 150])
# 2. Melatih model (Mesin Replika)
model = LinearRegression().fit(X_train, y_train)
# 3. Menetapkan Skenario Dasar (Baseline)

# Kondisi saat ini: Iklan 10 Juta, Diskon 10%
baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]
print(f"Prediksi Keuntungan Baseline: Rp {baseline_pred:.2f} Juta")

def run_simulation(new_iklan, new_diskon):
  # Input baru dari user (Intervensi)
  intervention_input = np.array([[new_iklan, new_diskon]])
  # Prediksi hasil intervensi
  prediction = model.predict(intervention_input)[0]
  # Menghitung Delta (Selisih)
  delta_y = prediction - baseline_pred
  return prediction, delta_y

import streamlit as st
st.set_page_config(
    page_title="Simulator Kebijakan Keuntungan Toko",
    page_icon="🔮",
    layout="wide"
)

# ==========================
# HEADER
# ==========================
st.title("🔮 Simulator Kebijakan Keuntungan Toko")
st.caption("Analisis skenario kebijakan bisnis menggunakan simulasi What-If.")

# ==========================
# SIDEBAR
# ==========================
with st.sidebar:
    st.header("⚙️ Tuas Kebijakan")

    iklan_slider = st.slider(
        "Anggaran Iklan (Juta)",
        min_value=0,
        max_value=50,
        value=10
    )

    diskon_slider = st.slider(
        "Besaran Diskon (%)",
        min_value=0,
        max_value=50,
        value=10
    )

    st.divider()

    st.info(
        """
        **Petunjuk**
        - Geser slider untuk membuat skenario baru.
        - Hasil akan dibandingkan dengan kondisi baseline.
        """
    )

# ==========================
# ENGINE
# ==========================
hasil_pred, delta = run_simulation(
    iklan_slider,
    diskon_slider
)

# ==========================
# KPI SECTION
# ==========================
st.subheader("📊 Ringkasan Hasil")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Prediksi Keuntungan",
        f"Rp {hasil_pred:.2f} Jt",
        f"{delta:.2f} Jt"
    )

with col2:
    st.metric(
        "Anggaran Iklan",
        f"{iklan_slider} Jt"
    )

with col3:
    st.metric(
        "Diskon",
        f"{diskon_slider}%"
    )

# ==========================
# ALERT HASIL
# ==========================
if delta > 0:
    st.success(
        f"✅ Skenario meningkatkan keuntungan sebesar {delta:.2f} Juta dibanding baseline."
    )
elif delta < 0:
    st.error(
        f"⚠️ Skenario menurunkan keuntungan sebesar {abs(delta):.2f} Juta dibanding baseline."
    )
else:
    st.info(
        "ℹ️ Tidak ada perubahan terhadap kondisi baseline."
    )

# ==========================
# PROGRESS TERHADAP BASELINE
# ==========================
persentase = max(
    0,
    min(
        int((hasil_pred / baseline_pred) * 100),
        200
    )
)

st.write("### 📈 Performa terhadap Baseline")
st.progress(min(persentase, 100))

st.caption(
    f"Kinerja saat ini: {persentase:.1f}% dari nilai baseline."
)

# ==========================
# TABS
# ==========================
tab1, tab2, tab3 = st.tabs(
    [
        "📋 Analisis",
        "📊 Tabel",
        "📈 Grafik"
    ]
)

# ==========================
# TAB ANALISIS
# ==========================
with tab1:

    with st.container(border=True):
        st.markdown("### Insight Skenario")

        st.write(
            f"""
            Dengan anggaran iklan **{iklan_slider} juta**
            dan diskon **{diskon_slider}%**,
            model memprediksi keuntungan sebesar
            **Rp {hasil_pred:.2f} juta**.
            """
        )

        st.write(
            f"Perubahan terhadap baseline adalah **{delta:.2f} juta**."
        )

    with st.expander("🔍 Detail Interpretasi"):
        st.write(
            """
            Nilai positif menunjukkan peningkatan performa
            dibanding kondisi awal, sedangkan nilai negatif
            menunjukkan penurunan performa.
            """
        )

# ==========================
# TAB TABEL
# ==========================
with tab2:

    data_tabel = pd.DataFrame({
        'Komponen': [
            'Anggaran Iklan (Juta)',
            'Besaran Diskon (%)',
            'Prediksi Keuntungan (Juta)'
        ],
        'Baseline': [
            10,
            10,
            baseline_pred
        ],
        'Skenario Baru': [
            iklan_slider,
            diskon_slider,
            hasil_pred
        ]
    })

    st.dataframe(
        data_tabel,
        use_container_width=True,
        hide_index=True
    )

# ==========================
# TAB GRAFIK
# ==========================
with tab3:

    data_plot = pd.DataFrame({
        'Skenario': [
            'Baseline',
            'Intervensi'
        ],
        'Keuntungan': [
            baseline_pred,
            hasil_pred
        ]
    })

    st.bar_chart(
        data=data_plot.set_index('Skenario'),
        use_container_width=True
    )

# ==========================
# FOOTER
# ==========================
st.divider()

st.caption(
    "Dashboard simulasi kebijakan bisnis • What-If Analysis"
)
