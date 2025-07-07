-- Buat database
CREATE DATABASE IF NOT EXISTS spk_pupuk;
USE spk_pupuk;

-- Tabel pengguna (hanya role staff, tanpa nama_lengkap)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel tanaman palawija
CREATE TABLE plants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_tanaman VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel pupuk (alternatif)
CREATE TABLE fertilizers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pupuk VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    satuan VARCHAR(20) NOT NULL,
    gambar VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel kriteria
CREATE TABLE criteria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_kriteria VARCHAR(100) NOT NULL,
    tipe_kriteria ENUM('benefit', 'cost') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel sub-kriteria
CREATE TABLE sub_criteria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    criteria_id INT NOT NULL,
    nama_sub_kriteria VARCHAR(100) NOT NULL,
    nilai_bobot DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (criteria_id) REFERENCES criteria(id) ON DELETE CASCADE
);

-- Tabel hasil perhitungan PSI
CREATE TABLE psi_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plant_id INT NOT NULL,
    user_id INT NOT NULL,
    tanggal_perhitungan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    catatan TEXT,
    FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabel detail hasil PSI (ranking pupuk)
CREATE TABLE psi_result_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    psi_result_id INT NOT NULL,
    fertilizer_id INT NOT NULL,
    psi_value DECIMAL(10,6) NOT NULL,
    ranking INT NOT NULL,
    FOREIGN KEY (psi_result_id) REFERENCES psi_results(id) ON DELETE CASCADE,
    FOREIGN KEY (fertilizer_id) REFERENCES fertilizers(id) ON DELETE CASCADE
);

-- Tabel penilaian alternatif (input nilai kriteria terhadap pupuk)
CREATE TABLE assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    psi_result_id INT NOT NULL,
    fertilizer_id INT NOT NULL,
    criteria_id INT NOT NULL,
    nilai DECIMAL(10,2) NOT NULL,
    sub_criteria_id INT NULL,
    FOREIGN KEY (psi_result_id) REFERENCES psi_results(id) ON DELETE CASCADE,
    FOREIGN KEY (fertilizer_id) REFERENCES fertilizers(id) ON DELETE CASCADE,
    FOREIGN KEY (criteria_id) REFERENCES criteria(id) ON DELETE CASCADE,
    FOREIGN KEY (sub_criteria_id) REFERENCES sub_criteria(id) ON DELETE SET NULL
);

-- Tabel rekomendasi publik (untuk ditampilkan tanpa login)
CREATE TABLE public_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plant_id INT NOT NULL,
    psi_result_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE,
    FOREIGN KEY (psi_result_id) REFERENCES psi_results(id) ON DELETE CASCADE
);
