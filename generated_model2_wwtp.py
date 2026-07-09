import pandas as pd
import numpy as np

# Setup Seed agar data konsisten
np.random.seed(2026)

# Generate Rentang Tanggal (01 Jan 2026 - 31 Mar 2026)
date_range = pd.date_range(start="2026-01-01", end="2026-03-31", freq='D')
data_rows = []

for current_date in date_range:
    # --- KONDISI BASELINE (NORMAL) ---
    flow_rate = round(np.random.normal(2500, 100), 2)       # m3/hari
    inlet_tss = round(np.random.normal(220, 15), 2)         # Kandungan padatan masuk (mg/L)
    
    # Efisiensi normal: menyaring ~92% tss
    outlet_tss = round(inlet_tss * np.random.uniform(0.06, 0.09), 2) 
    
    # Kebutuhan Koagulan Normal: Proporsional dengan Flow & Inlet TSS
    # Rumus dasar: 0.15 Kg per m3 + penyesuaian beban TSS
    normal_coagulant_ratio = 0.15 + (inlet_tss / 1500)
    coagulant_dosage = round(flow_rate * normal_coagulant_ratio * np.random.uniform(0.98, 1.02), 2)
    
    chemical_cost_per_kg = 1.5 # USD per Kg
    op_mode = "Auto"
    is_anomaly = 0

    # --- INJEKSI SKENARIO ANOMALI (Overdosing Manual di Bulan 2) ---
    # Kejadian: Tanggal 12 Feb s/d 22 Feb 2026
    if current_date.month == 2 and 12 <= current_date.day <= 22:
        op_mode = "Manual"
        is_anomaly = 1
        # Operator menyuntikkan koagulan 3x lipat dari dosis normal (Overdosing)
        coagulant_dosage = round(coagulant_dosage * np.random.uniform(2.8, 3.3), 2)
        # Efek kimia berlebih: Outlet TSS sedikit lebih jernih, tapi biaya bengkak hancur-hancuran
        outlet_tss = round(outlet_tss * 0.3, 2)

    # Hitung Total Biaya Kimia Harian
    total_cost = round(coagulant_dosage * chemical_cost_per_kg, 2)

    data_rows.append({
        "Date": current_date.strftime("%Y-%m-%d"),
        "Wastewater_Flow_m3": flow_rate,
        "Inlet_TSS_mgL": inlet_tss,
        "Outlet_TSS_mgL": outlet_tss,
        "Coagulant_Used_Kg": coagulant_dosage,
        "Chemical_Cost_USD": total_cost,
        "Control_Mode": op_mode,
        "Is_Anomaly": is_anomaly
    })

# Eksport ke CSV
df = pd.DataFrame(data_rows)
df.to_csv("model2_wwtp_operational.csv", index=False)
print("Sukses: File 'model2_wwtp_operational.csv' berhasil dibuat.")