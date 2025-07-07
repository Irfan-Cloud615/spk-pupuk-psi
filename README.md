# 🌿 Sistem Pendukung Keputusan Pemilihan Pupuk Terbaik
> Metode Preference Selection Index (PSI) — Dibangun dengan Flask

Aplikasi web untuk membantu pegawai toko menentukan pupuk terbaik berdasarkan penilaian terhadap kriteria seperti **harga, mutu, stok, dan cara kerja**, dengan pendekatan objektif menggunakan metode **PSI (Preference Selection Index)**.

---

## 🖼️ Tampilan & Fitur

- ✅ Login & Register User
- 🌱 CRUD Alternatif (Pupuk)
- 🧮 CRUD Kriteria & Subkriteria
- 📝 Halaman Penilaian Pupuk berdasarkan kategori (Masa Pertumbuhan / Buah)
- 📊 Perhitungan PSI otomatis (normalisasi, preferensi, ranking)
- 🏆 Halaman Ranking Pupuk terbaik

---

## 📁 Struktur Folder
<pre> ```
SPK_PUPUK_PSI/
├── app.py # Entry point utama
├── config.py # Konfigurasi koneksi database
├── /database/schema.sql # Struktur tabel MySQL
├── /models/db_models.py # (opsional) fungsi query
├── /templates/ # Semua file HTML
├── /static/
│ ├── css/
│ ├── js/
│ ├── img/
│ └── uploads/ # Gambar pupuk
├── /venv/ # Virtual environment (jangan diupload)
├── README.md
``` </pre>

---

## 🚀 Cara Menjalankan Aplikasi

### 1. 📦 Install Dependency

Gunakan Python `3.13.4` dan pip `25.1.1`.

<pre>bash</pre>
<pre>pip install flask flask-mysqldb flask-bcrypt</pre>

🔧 Konfigurasi MySQL

Buat database bernama: spk_pupuk
Import SQL:
<pre>mysql -u root -p spk_pupuk < database/schema.sql</pre>    

```
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'passwordmu'
MYSQL_DB = 'spk_pupuk'
```

▶️ Jalankan Aplikasi
```
python app.py
```
Buka di browser: http://localhost:5050<br>
📚 Library yang Digunakan
```
Flask
Flask-MySQLdb
Flask-Bcrypt
Werkzeug
Jinja2 (template engine bawaan Flask)
```

📄 Lisensi <br>
MIT License © 2025
