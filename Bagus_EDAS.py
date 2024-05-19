
import numpy as np
import pandas as pd

# C1 = Luas Tanah, C2 = Harga, C3 = Tipe, C4 = Sumber Air, C5 = Kamar Tidur, C6 = Kamar Mandi, C7 = Pos Satpam, C8 = Lokasi

kriteria = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
bobot = [0.2904, 0.2133, 0.1708, 0.0441, 0.1399, 0.0293, 0.0624, 0.0498]
jenis = ['Benefit', 'Cost', 'Benefit', 'Benefit', 'Benefit', 'Benefit', 'Benefit', 'Benefit']

# Data alternatif Matriks Keputusan (X)
alternatif = [
    
        [7, 7,  9,  7,  1,  9,  1,  6],
        [4, 3,  5,  3,  3,  10, 7,  4],
        [5, 5,  7,  4,  9,  2,  6,  1],
        [9, 5,  10, 9,  7,  8,  6,  7],
        [10,1,  9,  2,  10, 6, 10,  2],
        [6, 7,  2,  7,  10, 2,  8,  7],
        [10,9,  10, 2,  6,  7,  10, 4],
        [7, 6,  6,  4,  7,  2,  3,  9],
        [4, 9,  9,  1,  6,  1,  6,  1],
        [9, 8,  2,  4,  5,  3,  2,  5],
        [4, 4,  2,  5,  4,  10, 6,  5],
        [10,6,  9,  9,  10, 10, 2,  6],
        [6, 8,  8,  5,  4,  9,  2,  3],
        [8, 6,  3,  3,  6,  7,  8,  7],
        [4, 9,  3,  5, 10,  5, 10,  6],
        [6, 2,  7,  6,  5,  6,  5,  9],
        [8, 4,  1,  8,  3, 10,  7,  4],
        [4, 1,  8,  5, 10,  5,  2,  6],
        [9, 8,  9,  5,  1,  3,  10, 6],
        [3, 1, 10,  4,  7,  5,  10, 8]
        
]

# Buat DataFrame untuk kriteria, bobot, dan tipe
df_kriteria = pd.DataFrame({
    'Kriteria': kriteria,
    'Bobot': bobot,
    'Tipe': jenis
})

# Tampilkan DataFrame kriteria
print("Data Kriteria, Bobot, dan Tipe:")
print(df_kriteria)

# Konversi data ke dalam DataFrame
df_alternatif = pd.DataFrame(alternatif, columns=kriteria)

# Tampilkan DataFrame alternatif [MATRIK KEPUTUSAN]
print("\nMatriks Keputusan (Data Alternatif):")
print(df_alternatif)

# Hitung nilai rata-rata untuk setiap kriteria
avg_kriteria = df_alternatif.mean()

# Mencetak solusi rata-rata
print("Average Solution:")
print(avg_kriteria)

# Fungsi untuk menghitung PDA (Positive Distance from Average) dan NDA (Negative Distance from Average)
def calculate_distances(df, avg, jenis):
    PDA = np.zeros(df.shape)
    NDA = np.zeros(df.shape)
    for i, t in enumerate(jenis):
        if t == 'Benefit':
            PDA[:, i] = np.maximum(0, df.iloc[:, i] - avg[i])
            NDA[:, i] = np.maximum(0, avg[i] - df.iloc[:, i])
        else:  # Cost criteria
            PDA[:, i] = np.maximum(0, avg[i] - df.iloc[:, i])
            NDA[:, i] = np.maximum(0, df.iloc[:, i] - avg[i])
    return PDA, NDA

# Hitung PDA dan NDA
PDA, NDA = calculate_distances(df_alternatif, avg_kriteria, jenis)


# Konversi hasilnya menjadi DataFrame
df_PDA = pd.DataFrame(PDA, columns=kriteria)
df_NDA = pd.DataFrame(NDA, columns=kriteria)

# Tampilkan hasil
print("PDA (Positive Distance from Average):")
print(df_PDA)

print("\nNDA (Negative Distance from Average):")
print(df_NDA)

# Hitung SP dan SN
SP = (PDA * bobot).sum(axis=1)
SN = (NDA * bobot).sum(axis=1)

# Normalisasi SP dan SN
NSP = SP / SP.max()
NSN = 1 - (SN / SN.max())

# Konversi hasilnya menjadi DataFrame
df_result = pd.DataFrame({
    'Alternatif': ['A' + str(i+1) for i in range(df_alternatif.shape[0])],
    'SP': SP,
    'SN': SN,
    'NSP': NSP,
    'NSN': NSN
})

# Tampilkan hasil
print("Hasil SP (Summed Positive distance) dan SN (Summed Negative distance):")
print(df_result[['Alternatif', 'SP', 'SN']])

print("\nHasil NSP (Normalized SP) dan NSN (Normalized SN):")
print(df_result[['Alternatif', 'NSP', 'NSN']])

# Hitung AS (Assessment Score)
AS = 0.5 * (NSP + NSN)

print("\nHasil AS (Assessment Score):")
print(df_result[['Alternatif', 'AS']])

# Buat DataFrame untuk hasil akhir
df_result = pd.DataFrame({
    'Alternatif': ['A' + str(i+1) for i in range(df_alternatif.shape[0])],
    'SP': SP,
    'SN': SN,
    'NSP': NSP,
    'NSN': NSN,
    'AS': AS
})

# Urutkan alternatif berdasarkan AS
df_result = df_result.sort_values(by='AS', ascending=False)

print(df_result)

# Hasil akhir, alternatif terbaik
best_alternative = df_result.iloc[0]['Alternatif']
print(f"Alternatif terbaik adalah: {best_alternative}")