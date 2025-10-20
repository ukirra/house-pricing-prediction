# Prediksi Harga Rumah

---

Aplikasi web berbasis Flask untuk mengestimasi harga rumah menggunakan lima masukan: **Luas Bangunan (meter persegi)**, **Luas Tanah (meter persegi)**, **Jumlah Kamar Tidur**, **Jumlah Kamar Mandi**, dan **Kapasitas Mobil di Garasi**. Model regresi dimuat dari berkas `model/model.joblib`, hasil ditampilkan dalam format Rupiah melalui popup ringkas di antarmuka.

---

## Teknologi yang Dipakai
- **Python 3.10+**
- **Flask**
- **NumPy, Pandas, Joblib**
- **HTML/CSS** + **SweetAlert2** (popup hasil)
- **Model**: `model/model.joblib` (regresi, output 1 nilai numerik)

---

## Fitur
- **Form input properti**: Luas Bangunan (m²), Luas Tanah (m²), Jumlah Kamar Tidur, Jumlah Kamar Mandi, Kapasitas Mobil di Garasi.
- **Input numerik**: field angka (tipe number), **tidak bisa** diisi huruf/simbol.
- **Validasi nilai**: angka **negatif ditolak** untuk semua isian.
- **Pilihan KT/KM/GRS**:
  - Opsi **0–10** melalui tombol pilihan (radio).
  - Opsi **“10+”** akan memunculkan **field angka tambahan** (wajib diisi untuk jumlah pastinya).
- **Hasil prediksi**: ditampilkan sebagai **pop up (SweetAlert2)** berisi ringkasan input dan estimasi harga.
- **Format harga**: hasil **dibulatkan ke ribuan terdekat** dan diformat dalam **Rupiah**.

---

## Dataset
- **Sumber**: Kaggle – *Daftar Harga Rumah* oleh **wisnu anggara**  
  Link: `https://www.kaggle.com/datasets/wisnuanggara/daftar-harga-rumah/data`
- **Jumlah data**: **1.010 baris**
- **Kolom**:
  - `LB` — Luas Bangunan (m²)
  - `LT` — Luas Tanah (m²)
  - `KT` — Jumlah Kamar Tidur
  - `KM` — Jumlah Kamar Mandi
  - `GRS` — Kapasitas Mobil dalam Garasi
  - `HARGA` — Target untuk pelatihan model (Rupiah)

---

## Struktur Direktori
  ```
  house-pricing-prediction/
  │── model/
  │   ├── model.joblib
  │── templates/
  │   ├── templates
  │── static/
  │   ├── style.css
  │── app.py
  │── requirements.txt
  │── README.md
  ```

> Pastikan berkas model berada di `model/`. Urutan fitur pada saat training harus sesuai dengan `["LB", "LT", "KT", "KM", "GRS"]`.

---

## Cara Menjalankan
1. Clone repository:

    ```bash
    git clone https://github.com/ukirra/house-pricing-prediction.git
    cd house-pricing-prediction
    ```

2. Buat dan aktifkan virtual environment:

    Windows (PowerShell)

    ```bash
    py -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

    macOS / Linux

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install semua dependensi:

    ```bash
    pip install -r requirements.txt
    ```

4. Jalankan aplikasi:

    ```bash
    python app.py
    ```

> Dapat diakses di `http://127.0.0.1:5000/`
