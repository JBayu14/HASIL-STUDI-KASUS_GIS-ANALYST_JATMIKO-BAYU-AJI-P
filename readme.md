\# Proyeksi Perubahan Tutupan Lahan Kawasan Aglomerasi Sarbagita (2020–2026)



Dokumen ini disusun sebagai penyelesaian \*\*Penugasan Rekrutmen Tenaga Ahli GIS Analyst (Analis SIG)\*\* dalam kegiatan \*Penyusunan Peta Tematik Derivatif Proyeksi Perubahan Tutupan Lahan untuk Mendukung Tata Kelola Pemanfaatan Ruang\*.



Pemodelan ini mencakup Kawasan Aglomerasi Sarbagita (Kota Denpasar, Kabupaten Badung, Kabupaten Gianyar, dan Kabupaten Tabanan), Provinsi Bali.



\---



\## 🛠️ Metodologi Analisis



Proses pengolahan data dilakukan secara otomatis berbasis skrip pemrograman Python memanfaatkan ekosistem `arcpy` (Spatial Analyst) pada ArcGIS Pro:



1\. \*\*Pengambilan Training Sample (Supervised Classification)\*\*

&#x20;  - Sampel pelatihan tutupan lahan didigitasi berdasarkan citra Composited Sentinel-2A tahun 2020 dan 2023.

&#x20;  - Mengelompokkan tutupan lahan ke dalam kelas utama (Badan Air, Vegetasi, Lahan Terbangun, Lahan Terbuka/Pertanian).



2\. \*\*Klasifikasi Tutupan Lahan (Machine Learning)\*\*

&#x20;  - Algoritma \*\*Random Forest\*\* (\*TrainRandomTreesClassifier\*) digunakan untuk melakukan klasifikasi supervised pada citra Sentinel-2A tahun 2020 dan 2023.



3\. \*\*Uji Validasi Model (Akurasi Spasial)\*\*

&#x20;  - Uji validasi diekstraksi dari \*titik ground truth\* independen menggunakan matriks konfusi (\*confusion matrix\*).

&#x20;  - Metrik yang dihitung secara matematis meliputi: \*Overall Accuracy (OA)\*, \*Cohen's Kappa Index\*, \*Producer's Accuracy (PA)\*, dan \*User's Accuracy (UA)\*.



4\. \*\*Pemodelan Proyeksi Tutupan Lahan Tahun 2026\*\*

&#x20;  - \*\*Driving Factor (Faktor Pendorong):\*\* Aksesibilitas jaringan jalan (\*Euclidean Distance\* dari layer Transportasi) yang merepresentasikan pemicu utama konversi lahan terbangun.

&#x20;  - \*\*Restricting Factor (Faktor Pembatas):\*\* Kawasan Hutan Lindung/Konservasi (\*KWSHUTAN\_AR\_250K\_2023\*) sebagai \*spatial mask\* untuk mengunci area agar tidak berubah secara ilegal dalam proyeksi.



\---



\## 📊 Hasil Uji Akurasi Klasifikasi



Hasil evaluasi matriks konfusi antara titik validasi (\*ground truth\*) dengan peta hasil klasifikasi menunjukkan tingkat akurasi yang sangat tinggi (\*Highly Reliable\*):



| Tahun | Overall Accuracy (OA) | Cohen's Kappa Index | Status Validasi |

| :---: | :-------------------: | :-----------------: | :-------------: |

| \*\*2020\*\* | \*\*92.31%\*\* (0.9231) | \*\*0.8974\*\* | Sangat Layak (\*Strong\*) |

| \*\*2023\*\* | \*\*94.23%\*\* (0.9423) | \*\*0.9231\*\* | Sangat Layak (\*Almost Perfect\*) |



\*Catatan: Tabulasi lengkap Producer's Accuracy (PA) dan User's Accuracy (UA) per kelas dapat dilihat pada file `Tabulasi\_Akurasi\_2020.csv` dan `Tabulasi\_Akurasi\_2023.csv`.\*



\---



\## 📁 Struktur Repositori \& Keluaran Analisis



Seluruh file keluaran penugasan telah diunggah dan terstruktur sebagai berikut:



```text

├── Data\_Output/

│   ├── Training Sample.shp             # Training sample tutupan lahan (.shp)

│   ├── Training Sample2.shp            # Training sample pendukung

│   ├── Klasifikasi\_Sarbagita\_2020.tif  # Peta Klasifikasi Tutupan Lahan 2020 (raster)

│   ├── Klasifikasi\_Sarbagita\_2023.tif  # Peta Klasifikasi Tutupan Lahan 2023 (raster)

│   ├── Klasifikasi\_Sarbagita\_2026.tif  # Peta Proyeksi Tutupan Lahan 2026 (raster)

│   ├── Tabulasi\_Akurasi\_2020.csv       # Tabulasi Uji Akurasi Tahun 2020

│   └── Tabulasi\_Akurasi\_2023.csv       # Tabulasi Uji Akurasi Tahun 2023

├── scripts/

│   ├── 01\_klasifikasi\_rf.py            # Skrip pelatihan \& klasifikasi Random Forest

│   ├── 02\_uji\_akurasi.py               # Skrip ekstraksi \& perhitungan matriks akurasi

│   └── 03\_proyeksi\_2026.py             # Skrip pemodelan proyeksi lahan 2026

└── README.md                           # Penjelasan metode dan dokumen laporan

