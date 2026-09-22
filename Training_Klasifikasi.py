
import arcpy
from arcpy.sa import *
import os

# ============================================================
# 1. KONFIGURASI PATH -- sesuaikan jika perlu
# ============================================================
BASE_DIR = r"D:\Jatzzz\Lowker\ILAPPS"
CITRA_DIR = os.path.join(
    BASE_DIR,
    r"Data Citra Sentinel Sarbagita-20260922T142232Z-1-001\Data Citra Sentinel Sarbagita"
)

# Citra input
raster_2020 = os.path.join(CITRA_DIR, "Sarbagita_2020.tif")
raster_2023 = os.path.join(CITRA_DIR, "Sarbagita_2023.tif")

# Training sample (shapefile hasil Training Samples Manager)
# Training sample terpisah untuk tiap tahun (mengikuti kondisi tutupan lahan
# masing-masing citra).
training_2020 = os.path.join(BASE_DIR, "Training Sample2.shp")
training_2023 = os.path.join(BASE_DIR, "Training Sample.shp")

# Folder output
OUT_DIR = os.path.join(BASE_DIR, "Output_Klasifikasi")
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

ecd_2020 = os.path.join(OUT_DIR, "RF_Classifier_2020.ecd")
ecd_2023 = os.path.join(OUT_DIR, "RF_Classifier_2023.ecd")
out_raster_2020 = os.path.join(OUT_DIR, "Klasifikasi_Sarbagita_2020.tif")
out_raster_2023 = os.path.join(OUT_DIR, "Klasifikasi_Sarbagita_2023.tif")

# ============================================================
# 2. CEK / CHECKOUT EXTENSION
# ============================================================
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("ImageAnalyst")

arcpy.env.overwriteOutput = True
arcpy.env.workspace = OUT_DIR

# ============================================================
# 3. PENGECEKAN FIELD ATRIBUT TRAINING SAMPLE
# ============================================================
# Training Samples Manager biasanya mengekspor field "Classname" dan
# "Classvalue" (integer). Fungsi ini mengecek nama field otomatis.
def get_class_field(shp_path):
    fields = [f.name for f in arcpy.ListFields(shp_path)]
    for candidate in ["Classvalue", "ClassValue", "classvalue", "CLASS_VAL", "Value"]:
        if candidate in fields:
            return candidate
    raise ValueError(
        f"Field kelas tidak ditemukan pada {shp_path}. "
        f"Field yang ada: {fields}. Cek nama field integer kelas Anda "
        f"lalu sesuaikan fungsi get_class_field()."
    )

class_field_2020 = get_class_field(training_2020)
class_field_2023 = get_class_field(training_2023)
print(f"Field kelas 2020: {class_field_2020}")
print(f"Field kelas 2023: {class_field_2023}")


# ============================================================
# 4. FUNGSI TRAINING + KLASIFIKASI (dipakai untuk 2020 & 2023)
# ============================================================
def train_and_classify(in_raster, in_training_features, class_field,
                        out_ecd, out_classified_raster,
                        max_trees=100, max_tree_depth=30, max_samples_per_class=1000):
    """
    Melatih Random Trees (Random Forest) classifier lalu mengklasifikasikan raster.
    """
    print(f"\n--- Melatih classifier untuk: {in_raster} ---")

    # a) Training Random Trees Classifier -> menghasilkan file .ecd
    arcpy.sa.TrainRandomTreesClassifier(
        in_raster=in_raster,
        in_training_features=in_training_features,
        out_classifier_definition=out_ecd,
        max_num_trees=max_trees,
        max_tree_depth=max_tree_depth,
        max_samples_per_class=max_samples_per_class,
        used_attributes="COLOR;MEAN;STD;COUNT;COMPACTNESS;RECTANGULARITY",
        dimension_value_field=class_field,
        in_additional_raster=None
    )
    print(f"Classifier definition tersimpan: {out_ecd}")

    # b) Klasifikasi raster memakai hasil training
    print(f"--- Menjalankan ClassifyRaster ---")
    classified = arcpy.sa.ClassifyRaster(
        in_raster=in_raster,
        in_classifier_definition=out_ecd,
        in_additional_raster=None
    )
    classified.save(out_classified_raster)
    print(f"Hasil klasifikasi tersimpan: {out_classified_raster}")
    return out_classified_raster


# ============================================================
# 5. JALANKAN UNTUK 2020 DAN 2023
# ============================================================
train_and_classify(
    in_raster=raster_2020,
    in_training_features=training_2020,
    class_field=class_field_2020,
    out_ecd=ecd_2020,
    out_classified_raster=out_raster_2020
)

train_and_classify(
    in_raster=raster_2023,
    in_training_features=training_2023,
    class_field=class_field_2023,
    out_ecd=ecd_2023,
    out_classified_raster=out_raster_2023
)

# ============================================================
# 6. TUTUP LISENSI
# ============================================================
arcpy.CheckInExtension("Spatial")
arcpy.CheckInExtension("ImageAnalyst")

print("\n=== SELESAI: klasifikasi 2020 & 2023 tersimpan di folder Output_Klasifikasi ===")