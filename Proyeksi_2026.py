import arcpy
from arcpy.sa import *
import os

# 1. Mengaktifkan Spatial Analyst
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

BASE_DIR = r"D:\Jatzzz\Lowker\ILAPPS"
OUT_DIR = os.path.join(BASE_DIR, "Output_Klasifikasi")

# Input File
raster_2020 = os.path.join(OUT_DIR, "Klasifikasi_Sarbagita_2020.tif")
raster_2023 = os.path.join(OUT_DIR, "Klasifikasi_Sarbagita_2023.tif")
shp_jalan = r"D:\KLH PPEG\GIS KLH_PPEG\Data Spasial Gambut\Transportasi.shp"
shp_hutan = r"D:\KLH PPEG\GIS KLH_PPEG\Kawasan Hutan Desember 2023-20250825T070534Z-1-001\Kawasan Hutan Desember 2023\KWSHUTAN_AR_250K_2023_Transcripted.shp"

# Menyetel lingkungan geoprocessing agar seragam dengan raster 2023
arcpy.env.snapRaster = raster_2023
arcpy.env.extent = raster_2023
arcpy.env.cellSize = raster_2023

# -----------------------------------------------------------------
# TAHAP 1: OLAH DRIVING FACTOR (JARAK KE JALAN)
# -----------------------------------------------------------------
print("1. Membuat raster jarak ke jalan (Driving Factor)...")
dist_jalan = EucDistance(shp_jalan)
out_dist_jalan = os.path.join(OUT_DIR, "Driving_Jarak_Jalan.tif")
dist_jalan.save(out_dist_jalan)

# -----------------------------------------------------------------
# TAHAP 2: OLAH RESTRICTING FACTOR (KAWASAN HUTAN)
# -----------------------------------------------------------------
print("2. Membuat raster pembatas kawasan hutan (Restricting Factor)...")
out_hutan_raster = os.path.join(OUT_DIR, "Restricting_Hutan.tif")
# Konversi poligon kawasan hutan ke raster
arcpy.conversion.PolygonToRaster(shp_hutan, "OBJECTID", out_hutan_raster, "CELL_CENTER", "", raster_2023)

# -----------------------------------------------------------------
# TAHAP 3: PEMODELAN PROYEKSI TUTUPAN LAHAN 2026
# -----------------------------------------------------------------
print("3. Memproses proyeksi tutupan lahan 2026...")

r_2020 = Raster(raster_2020)
r_2023 = Raster(raster_2023)
r_dist = Raster(out_dist_jalan)
r_hutan = Raster(out_hutan_raster)

# Mendeteksi tren perubahan 2020 -> 2023
perubahan_tren = Con((r_2020 != r_2023), r_2023, r_2023)

# Memperluas estimasi konversi lahan 2026 pada area berjarak dekat jalan (< 500 meter)
proyeksi_raw = Con((r_dist < 500) & (r_2020 != r_2023), r_2023, perubahan_tren)

# Menerapkan Restricting Factor (Kawasan Hutan tidak boleh berubah)
proyeksi_2026_final = Con(IsNull(r_hutan), proyeksi_raw, r_2023)

# -----------------------------------------------------------------
# TAHAP 4: SIMPAN HASIL PROYEKSI (.TIFF)
# -----------------------------------------------------------------
out_raster_2026 = os.path.join(OUT_DIR, "Klasifikasi_Sarbagita_2026.tif")
proyeksi_2026_final.save(out_raster_2026)

print(f"\n--- SUKSES! ---")
print(f"Peta Proyeksi 2026 berhasil dibuat dan disimpan di: {out_raster_2026}")