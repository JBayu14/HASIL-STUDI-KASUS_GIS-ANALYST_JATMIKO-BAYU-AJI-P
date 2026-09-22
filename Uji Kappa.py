
import arcpy
from arcpy.sa import ExtractValuesToPoints
import pandas as pd
import numpy as np
import os

# 1. Mengaktifkan Spatial Analyst dan Menyiapkan Variabel
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

BASE_DIR = r"D:\Jatzzz\Lowker\ILAPPS"
OUT_DIR = os.path.join(BASE_DIR, "Output_Klasifikasi")
ground_truth_shp = os.path.join(BASE_DIR, "titik_grounth.shp")

out_raster_2020 = os.path.join(OUT_DIR, "Klasifikasi_Sarbagita_2020.tif")
out_raster_2023 = os.path.join(OUT_DIR, "Klasifikasi_Sarbagita_2023.tif")

# Sesuaikan dengan nama kolom yang berisi nilai ground truth
kolom_aktual = "GrndTruth" 

def hitung_dan_ekspor_akurasi(raster_path, points_shp, tahun):
    print(f"\n--- Memproses Uji Akurasi Tahun {tahun} ---")
    
    extracted_pts = os.path.join(OUT_DIR, f"Extracted_GT_{tahun}.shp")
    ExtractValuesToPoints(points_shp, raster_path, extracted_pts)
    
    data = []
    with arcpy.da.SearchCursor(extracted_pts, [kolom_aktual, "RASTERVALU"]) as cursor:
        for row in cursor:
            if row[1] != -9999: # Mengabaikan data kosong/NoData
                data.append({'Aktual': row[0], 'Prediksi': row[1]})
                
    df = pd.DataFrame(data)
    
    # 2. Membuat Matriks Konfusi dengan Pandas
    # Menyeleraskan kelas aktual dan prediksi jika ada kelas yang tidak terprediksi
    classes = sorted(list(set(df['Aktual']).union(set(df['Prediksi']))))
    cm = pd.crosstab(df['Aktual'], df['Prediksi']).reindex(index=classes, columns=classes, fill_value=0)
    
    # Ekstraksi nilai untuk perhitungan
    N = cm.sum().sum()
    tp = np.diag(cm)
    row_totals = cm.sum(axis=1).values # Total Aktual
    col_totals = cm.sum(axis=0).values # Total Prediksi
    
    # 3. Menghitung Metrik Akurasi secara Manual
    # Overall Accuracy
    oa = tp.sum() / N
    
    # Cohen's Kappa
    pe = ((row_totals * col_totals) / N).sum() / N
    kappa = (oa - pe) / (1 - pe) if pe != 1 else 1.0
    
    # Producer's Accuracy (PA) dan User's Accuracy (UA)
    pa = np.where(row_totals > 0, tp / row_totals, 0)
    ua = np.where(col_totals > 0, tp / col_totals, 0)
    
    # 4. Menyusun Tabulasi Hasil 
    hasil_kelas = []
    for i, cls in enumerate(classes):
        hasil_kelas.append({
            'Tahun': tahun,
            'Kelas': cls,
            'Producer_Accuracy': round(pa[i], 4),
            'User_Accuracy': round(ua[i], 4)
        })
    
    df_hasil = pd.DataFrame(hasil_kelas)
    
    # Menambahkan Global Metrics ke baris bawah
    df_hasil.loc[len(df_hasil)] = ['Global', 'Overall Accuracy', round(oa, 4), None]
    df_hasil.loc[len(df_hasil)] = ['Global', 'Cohens Kappa', round(kappa, 4), None]
    
    # 5. Ekspor ke CSV
    out_csv = os.path.join(OUT_DIR, f"Tabulasi_Akurasi_{tahun}.csv")
    df_hasil.to_csv(out_csv, index=False)
    
    print(f"Overall Accuracy: {oa:.4f}")
    print(f"Cohen's Kappa: {kappa:.4f}")
    print(f"File CSV tersimpan di: {out_csv}")

# Menjalankan fungsi
hitung_dan_ekspor_akurasi(out_raster_2020, ground_truth_shp, "2020")
hitung_dan_ekspor_akurasi(out_raster_2023, ground_truth_shp, "2023")