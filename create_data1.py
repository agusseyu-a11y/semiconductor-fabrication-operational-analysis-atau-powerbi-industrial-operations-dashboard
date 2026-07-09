
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# 1. INPUT PARAMETER (Pabrik Kelas TSMC)
# ==========================================
start_date = datetime(2026, 1, 1)
total_days = 90  # 3 Bulan harian
lines = ['FAB_Line_A', 'FAB_Line_B', 'FAB_Line_C']
shifts = ['Shift_1', 'Shift_2', 'Shift_3']

# Target dasar produksi per shift (Kapasitas tinggi)
base_wafer_start = 1100 

print("Memulai proses generasi data simulasi semikonduktor...")

# ==========================================
# 2. OPERASI GENERASI DATA (Looping & Math)
# ==========================================
data_rows = []

# Melakukan perulangan untuk setiap hari selama 3 bulan
for day in range(total_days):
    current_date = start_date + timedelta(days=day)
    
    for line in lines:
        for shift in shifts:
            
            # --- Kondisi Normal (Menggunakan NumPy untuk Variasi Acak) ---
            # Angka wafer start dibuat naik turun secara natural di sekitar target 1100
            wafer_start = int(np.random.normal(base_wafer_start, 20))
            
            # Yield normal pabrik semikonduktor kelas dunia (95% - 98%)
            yield_rate = np.random.uniform(0.95, 0.98)
            
            # OEE Mesin normal (85% - 95%)
            oee = np.random.uniform(85, 95)
            
            unplanned_downtime = 0
            defect_reason = 'None'
            
            # --- MENYUNTIKKAN SKENARIO AKAR MASALAH (ANOMALI) ---
            
            # Skenario Bulan 1: Masalah Kelistrikan di FAB_Line_A (Tanggal 15-16 Januari 2026)
            if current_date in [datetime(2026, 1, 15), datetime(2026, 1, 16)] and line == 'FAB_Line_A':
                oee = np.random.uniform(40, 55)  # OEE Drop parah
                unplanned_downtime = int(np.random.uniform(180, 240))  # Mati listrik 3-4 jam
                defect_reason = 'Lithography Misalignment'
                yield_rate = 0.90  # Yield ikut turun

            # Skenario Bulan 2: Kontaminasi Kimia Massal di Semua Line (Tanggal 12-14 Februari 2026)
            elif current_date in [datetime(2026, 2, 12), datetime(2026, 2, 13), datetime(2026, 2, 14)]:
                yield_rate = np.random.uniform(0.80, 0.85)  # Gagal QC massal
                defect_reason = 'Particle Contamination'

            # Skenario Bulan 3: Kelalaian SOP Kalibrasi di Shift 3 (Tanggal 5-10 Maret 2026)
            elif current_date >= datetime(2026, 3, 5) and current_date <= datetime(2026, 3, 10) and shift == 'Shift_3':
                yield_rate = np.random.uniform(0.85, 0.88)  # Khusus shift malam defect melonjak
                defect_reason = 'Pattern Distortion'

            # --- Hitung Kalkulasi Akhir ---
            wafer_good = int(wafer_start * yield_rate)
            wafer_defect = wafer_start - wafer_good
            
            # Simpan baris data ke dalam list
            data_rows.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Line_ID': line,
                'Shift': shift,
                'Wafer_Starts': wafer_start,
                'Wafer_Good_Output': wafer_good,
                'Wafer_Defect_Qty': wafer_defect,
                'Defect_Reason': defect_reason,
                'Machine_OEE_Percentage': round(oee, 2),
                'Unplanned_Downtime_Min': unplanned_downtime
            })

# ==========================================
# 3. OUTPUT (Mengubah List Menjadi Dataframe & CSV)
# ==========================================
# Pandas mengubah tumpukan data di atas menjadi format tabel struktur (DataFrame)
df = pd.DataFrame(data_rows)

# Ekspor tabel tersebut menjadi file CSV siap pakai untuk Power BI
output_filename = 'data_produksi_semikonduktor.csv'
df.to_csv(output_filename, index=False)

print(f"Sukses! File data mentah berhasil dibuat dengan nama: {output_filename}")
print(f"Total baris data yang dihasilkan: {len(df)} baris.")