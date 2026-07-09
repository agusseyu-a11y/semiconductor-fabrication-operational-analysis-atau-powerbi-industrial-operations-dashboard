import pandas as pd
import numpy as np

# Setup Seed
np.random.seed(2026)

# Generate Rentang Tanggal (01 Jan 2026 - 31 Mar 2026)
date_range = pd.date_range(start="2026-01-01", end="2026-03-31", freq='D')
data_rows = []

for i, current_date in enumerate(date_range):
    # --- KONDISI BASELINE (NORMAL) ---
    raw_water_feed = round(np.random.normal(150, 4), 2)       # m3/hour
    uf_diff_pressure = round(np.random.uniform(0.8, 1.2), 2)  # Bar (Normal di bawah 1.5)
    ro_permeate_flow = round(raw_water_feed * 0.75 * np.random.uniform(0.98, 1.02), 2) # Recovery ~75%
    
    # --- INJEKSI DEGRADASI BERTAHAP (Maret 2026 - Membrane Fouling) ---
    # Mulai terjadi akumulasi penyumbatan dari tanggal 05 Maret sampai 26 Maret
    if current_date.month == 3 and 5 <= current_date.day <= 26:
        # Menghitung faktor kenaikan bertahap berdasarkan deret hari
        days_into_anomaly = current_date.day - 5
        
        # Tekanan filter UF naik perlahan setiap harinya akibat mampet
        uf_diff_pressure = round(uf_diff_pressure + (days_into_anomaly * 0.09), 2)
        # Debit air keluar RO drop akibat tekanan balik dari filter mampet
        ro_permeate_flow = round(ro_permeate_flow - (days_into_anomaly * 1.5), 2)

    data_rows.append({
        "Date": current_date.strftime("%Y-%m-%d"),
        "Raw_Water_Feed_m3h": raw_water_feed,
        "UF_Differential_Pressure_Bar": uf_diff_pressure,
        "RO_Permeate_Flow_m3h": ro_permeate_flow
    })

# Eksport ke CSV
df = pd.DataFrame(data_rows)
df.to_csv("model3_wtp_predictive.csv", index=False)
print("Sukses: File 'model3_wtp_predictive.csv' berhasil dibuat.")