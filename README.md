Customer and Product Segmentation using E-Commerce Data

Capstone Project ini menampilkan analisis segmentasi pelanggan menggunakan data RFM (Recency, Frequency, Monetary), (Quantity, Country) dan (Quantity, Total Price, Unit Price, Invoiceno). Project ini juga mennggunakan 2 Algoritma yaitu K-Means dan DBscan. Aplikasi ini dibangun dengan Colab, Github dan Streamlit.

Langkah-langkah Setup dari Google Colab ke GitHub lalu ke Streamlit

1. Membuat file di Google Colab
Pertama, buka Google Colab lalu buat file bernama app.py.
Tulis seluruh kode Streamlit yang dibutuhkan sampai aplikasi bisa berjalan dengan baik.
Setelah selesai, download file app.py ke komputer.

2. Membuat repository di GitHub
Masuk ke akun GitHub, lalu buat repository baru untuk project tersebut.
Setelah repository jadi, upload file-file yang diperlukan untuk deployment, seperti:
app.py
file dataset (jika digunakan)
requirements.txt
Pastikan semua file sudah ada di dalam repository.

3. Masuk ke Streamlit Cloud
Buka situs https://streamlit.io/
lalu login. Hubungkan akun Streamlit dengan akun GitHub kamu jika belum terhubung.

4. Membuat aplikasi di Streamlit Cloud
Setelah login, klik tombol Create App di pojok kanan.
Pilih repository GitHub yang ingin kamu deploy.
Tentukan branch yang digunakan dan pilih file utama app.py.

5. Deploy aplikasi
Klik tombol Deploy dan tunggu beberapa saat.
Jika proses berhasil, aplikasi Streamlit akan langsung tampil dalam bentuk website dan bisa diakses melalui link yang diberikan.
