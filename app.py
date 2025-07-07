from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import config
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = 'ini_kunci_rahasia_yang_panjang'

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql = MySQL(app)

@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# =========================
# CRUD ALTERNATIF (PUPUK)
# =========================
@app.route('/alternatif')
def alternatif():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM fertilizers")
    data = cur.fetchall()
    cur.close()
    return render_template('alternatif.html', pupuk=data)

@app.route('/alternatif/tambah', methods=['GET', 'POST'])
def tambah_alternatif():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']
        satuan = request.form['satuan']
        kategori = request.form['kategori']
        gambar = request.files['gambar']

        nama_file = None
        if gambar:
            nama_file = secure_filename(gambar.filename)
            gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], nama_file))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO fertilizers (nama_pupuk, deskripsi, satuan, kategori, gambar) VALUES (%s, %s, %s, %s,%s)",
                    (nama, deskripsi, satuan,kategori, nama_file))
        mysql.connection.commit()
        cur.close()

        flash('Data pupuk berhasil ditambahkan!')
        return redirect(url_for('alternatif'))

    return render_template('tambah_alternatif.html')

@app.route('/alternatif/edit/<int:id>', methods=['GET', 'POST'])
def edit_alternatif(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM fertilizers WHERE id = %s", (id,))
    pupuk = cur.fetchone()

    if request.method == 'POST':
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']
        satuan = request.form['satuan']
        kategori = request.form['kategori']
        gambar = request.files['gambar']

        nama_file = pupuk[4]  # default gambar lama
        if gambar and gambar.filename != '':
            nama_file = secure_filename(gambar.filename)
            gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], nama_file))

        cur.execute("UPDATE fertilizers SET nama_pupuk=%s, deskripsi=%s, satuan=%s,kategori=%s, gambar=%s WHERE id=%s",
                    (nama, deskripsi, satuan,kategori, nama_file, id))
        mysql.connection.commit()
        cur.close()

        flash('Data pupuk berhasil diubah!')
        return redirect(url_for('alternatif'))

    cur.close()
    return render_template('edit_alternatif.html', pupuk=pupuk)

@app.route('/alternatif/hapus/<int:id>')
def hapus_alternatif(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM fertilizers WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash('Data pupuk berhasil dihapus!')
    return redirect(url_for('alternatif'))

# =========================
# END CRUD ALTERNATIF (PUPUK)
# =========================

# =========================
# CRUD KRITERIA
# =========================

@app.route('/kriteria')
def kriteria():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM criteria")
    data = cur.fetchall()
    cur.close()
    return render_template('kriteria.html', kriteria=data)

@app.route('/kriteria/tambah', methods=['GET', 'POST'])
def tambah_kriteria():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nama = request.form['nama']
        tipe = request.form['tipe']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO criteria (nama_kriteria, tipe_kriteria) VALUES (%s, %s)", (nama, tipe))
        mysql.connection.commit()
        cur.close()

        flash('Kriteria berhasil ditambahkan!')
        return redirect(url_for('kriteria'))

    return render_template('tambah_kriteria.html')

@app.route('/kriteria/edit/<int:id>', methods=['GET', 'POST'])
def edit_kriteria(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM criteria WHERE id = %s", (id,))
    data = cur.fetchone()

    if request.method == 'POST':
        nama = request.form['nama']
        tipe = request.form['tipe']

        cur.execute("UPDATE criteria SET nama_kriteria = %s, tipe_kriteria = %s WHERE id = %s",
                    (nama, tipe, id))
        mysql.connection.commit()
        cur.close()

        flash('Kriteria berhasil diperbarui!')
        return redirect(url_for('kriteria'))

    cur.close()
    return render_template('edit_kriteria.html', kriteria=data)

@app.route('/kriteria/hapus/<int:id>')
def hapus_kriteria(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM criteria WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash('Kriteria berhasil dihapus!')
    return redirect(url_for('kriteria'))

# =========================
# END CRUD KRITERIA
# =========================

# =========================
# CRUD SUB-KRITERIA
# =========================

@app.route('/sub_kriteria')
def sub_kriteria():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT sc.id, c.nama_kriteria, sc.nama_sub_kriteria, sc.nilai_bobot 
        FROM sub_criteria sc 
        JOIN criteria c ON sc.criteria_id = c.id
    """)
    data = cur.fetchall()
    cur.close()
    return render_template('sub_kriteria.html', subkriteria=data)

@app.route('/sub_kriteria/tambah', methods=['GET', 'POST'])
def tambah_sub_kriteria():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nama_kriteria FROM criteria")
    daftar_kriteria = cur.fetchall()

    if request.method == 'POST':
        criteria_id = request.form['criteria_id']
        nama = request.form['nama']
        bobot = request.form['bobot']

        cur.execute("INSERT INTO sub_criteria (criteria_id, nama_sub_kriteria, nilai_bobot) VALUES (%s, %s, %s)",
                    (criteria_id, nama, bobot))
        mysql.connection.commit()
        cur.close()

        flash('Sub-kriteria berhasil ditambahkan!')
        return redirect(url_for('sub_kriteria'))

    return render_template('tambah_sub_kriteria.html', kriteria=daftar_kriteria)

@app.route('/sub_kriteria/edit/<int:id>', methods=['GET', 'POST'])
def edit_sub_kriteria(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nama_kriteria FROM criteria")
    daftar_kriteria = cur.fetchall()

    cur.execute("SELECT * FROM sub_criteria WHERE id = %s", (id,))
    data = cur.fetchone()

    if request.method == 'POST':
        criteria_id = request.form['criteria_id']
        nama = request.form['nama']
        bobot = request.form['bobot']

        cur.execute("""
            UPDATE sub_criteria 
            SET criteria_id = %s, nama_sub_kriteria = %s, nilai_bobot = %s 
            WHERE id = %s
        """, (criteria_id, nama, bobot, id))
        mysql.connection.commit()
        cur.close()

        flash('Sub-kriteria berhasil diperbarui!')
        return redirect(url_for('sub_kriteria'))

    cur.close()
    return render_template('edit_sub_kriteria.html', sub=data, kriteria=daftar_kriteria)

@app.route('/sub_kriteria/hapus/<int:id>')
def hapus_sub_kriteria(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM sub_criteria WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash('Sub-kriteria berhasil dihapus!')
    return redirect(url_for('sub_kriteria'))

# =========================
# END CRUD SUB-KRITERIA
# =========================

# =========================
# PENILAIAN
# =========================
@app.route('/penilaian', methods=['GET', 'POST'])
def penilaian():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    kategori = request.args.get('kategori')

    # Handle simpan/edit penilaian
    if request.method == 'POST':
        fertilizer_id = request.form['fertilizer_id']
        criteria_id = request.form['criteria_id']
        nilai = request.form['nilai']
        # sub_criteria_id = request.form.get('sub_criteria_id') or None
        raw_sub = request.form.get('sub_criteria_id')
        sub_criteria_id = int(raw_sub) if raw_sub and raw_sub.isdigit() else None


        # Sementara pakai plant_id = 1, user_id = 1
        cur.execute("SELECT id FROM psi_results WHERE plant_id=1 AND user_id=%s ORDER BY id DESC LIMIT 1",(session['user_id'],))
        result = cur.fetchone()
        if result:
            psi_result_id = result[0]
        else:
            cur.execute("INSERT INTO psi_results (plant_id, user_id, catatan) VALUES (1, %s, 'penilaian manual')",(session['user_id'],))
            psi_result_id = cur.lastrowid

        # Cek apakah sudah ada
        cur.execute("""
            SELECT id FROM assessments WHERE psi_result_id=%s AND fertilizer_id=%s AND criteria_id=%s
        """, (psi_result_id, fertilizer_id, criteria_id))
        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE assessments SET nilai=%s, sub_criteria_id=%s 
                WHERE id=%s
            """, (nilai, sub_criteria_id, existing[0]))
        else:
            cur.execute("""
                INSERT INTO assessments (psi_result_id, fertilizer_id, criteria_id, nilai, sub_criteria_id) 
                VALUES (%s, %s, %s, %s, %s)
            """, (psi_result_id, fertilizer_id, criteria_id, nilai, sub_criteria_id))
        mysql.connection.commit()
        return redirect(url_for('penilaian', kategori=kategori))

    # Handle tampilkan tabel
    fertilizers = []
    kriteria = []
    sub_kriteria = []
    nilai_map = {}

    if kategori:
        # Ambil pupuk sesuai kategori
        cur.execute("SELECT * FROM fertilizers WHERE kategori = %s", (kategori,))
        fertilizers = cur.fetchall()

        cur.execute("SELECT * FROM criteria")
        kriteria = cur.fetchall()

        cur.execute("SELECT * FROM sub_criteria")
        sub_kriteria = cur.fetchall()

        # Ambil nilai penilaian terakhir
        cur.execute("""
            SELECT a.fertilizer_id, a.criteria_id, a.nilai, a.sub_criteria_id
            FROM assessments a
            JOIN psi_results pr ON a.psi_result_id = pr.id
            WHERE pr.plant_id=1 AND pr.user_id=%s
        """,(session['user_id'],))
        for row in cur.fetchall():
            key = f"{row[0]}_{row[1]}"
            nilai_map[key] = {'nilai': row[2], 'sub_id': row[3]}

    cur.close()
    return render_template("penilaian.html", kategori=kategori,
                           fertilizers=fertilizers,
                           kriteria=kriteria,
                           sub_kriteria=sub_kriteria,
                           nilai_map=nilai_map)


@app.route('/penilaian/hapus/<int:fertilizer_id>/<int:criteria_id>')
def hapus_penilaian(fertilizer_id, criteria_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    kategori = request.args.get('kategori')
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id FROM psi_results WHERE plant_id=1 AND user_id=%s ORDER BY id DESC LIMIT 1
    """,(session['user_id'],))
    result = cur.fetchone()
    if result:
        psi_result_id = result[0]
        cur.execute("""
            DELETE FROM assessments WHERE psi_result_id=%s AND fertilizer_id=%s AND criteria_id=%s
        """, (psi_result_id, fertilizer_id, criteria_id))
        mysql.connection.commit()

    cur.close()
    return redirect(url_for('penilaian', kategori=kategori))

# =========================
# END PENILAIAN
# =========================

# =========================
# PERHITUNGAN
# =========================

@app.route('/perhitungan')
def perhitungan():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    # Ambil psi_result_id terbaru
    cur.execute("SELECT id FROM psi_results ORDER BY id DESC LIMIT 1")
    result = cur.fetchone()
    if not result:
        flash("Belum ada data penilaian untuk dihitung.")
        return redirect(url_for('penilaian'))

    psi_result_id = result[0]

    # Ambil data penilaian (Xij)
    cur.execute("""
        SELECT a.fertilizer_id, f.nama_pupuk, a.criteria_id, c.nama_kriteria, c.tipe_kriteria, a.nilai
        FROM assessments a
        JOIN fertilizers f ON a.fertilizer_id = f.id
        JOIN criteria c ON a.criteria_id = c.id
        WHERE a.psi_result_id = %s
    """, (psi_result_id,))
    rows = cur.fetchall()

    # Struktur data: pupuk_id -> {nama, nilai per kriteria}
    pupuk_dict = {}
    kriteria_set = set()
    nilai_dict = {}

    for pid, nama, kid, knama, ktipe, nilai in rows:
        kriteria_set.add((kid, knama, ktipe))
        if pid not in pupuk_dict:
            pupuk_dict[pid] = {'nama': nama, 'nilai': {}}
        pupuk_dict[pid]['nilai'][kid] = float(nilai)

    kriteria_list = sorted(list(kriteria_set))  # (id, nama, tipe)

    # Normalisasi
    normalisasi = {}
    for kid, _, tipe in kriteria_list:
        nilai_k = [pupuk_dict[pid]['nilai'][kid] for pid in pupuk_dict if kid in pupuk_dict[pid]['nilai']]
        max_k = max(nilai_k)
        min_k = min(nilai_k)

        for pid in pupuk_dict:
            if pid not in normalisasi:
                normalisasi[pid] = {}
            xij = pupuk_dict[pid]['nilai'].get(kid, 0)
            if tipe == 'benefit':
                normalisasi[pid][kid] = xij / max_k if max_k else 0
            elif tipe == 'cost':
                normalisasi[pid][kid] = min_k / xij if xij else 0

    # Rata-rata preferensi tiap alternatif
    rata_rata = {}
    for pid in normalisasi:
        nilai_list = list(normalisasi[pid].values())
        rata_rata[pid] = sum(nilai_list) / len(nilai_list)

    # Simpan ke psi_result_details
    cur.execute("DELETE FROM psi_result_details WHERE psi_result_id = %s", (psi_result_id,))
    ranking_list = sorted(rata_rata.items(), key=lambda x: x[1], reverse=True)

    for i, (pid, nilai_psi) in enumerate(ranking_list, start=1):
        cur.execute("""
            INSERT INTO psi_result_details (psi_result_id, fertilizer_id, psi_value, ranking)
            VALUES (%s, %s, %s, %s)
        """, (psi_result_id, pid, round(nilai_psi, 6), i))

    mysql.connection.commit()
    cur.close()

    return render_template("perhitungan.html",
                           kriteria_list=kriteria_list,
                           pupuk_dict=pupuk_dict,
                           normalisasi=normalisasi,
                           rata_rata=rata_rata,
                           ranking_list=ranking_list)

# =========================
# END PERHITUNGAN
# =========================

# =========================
# RANKING
# =========================
@app.route('/ranking')
def ranking():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    # Ambil hasil ranking PSI terbaru
    cur.execute("""
        SELECT prd.fertilizer_id, f.nama_pupuk, prd.psi_value, prd.ranking
        FROM psi_result_details prd
        JOIN fertilizers f ON prd.fertilizer_id = f.id
        WHERE prd.psi_result_id = (
            SELECT id FROM psi_results ORDER BY id DESC LIMIT 1
        )
        ORDER BY prd.ranking ASC
    """)
    hasil_ranking = cur.fetchall()
    cur.close()

    return render_template("ranking.html", hasil_ranking=hasil_ranking)
# =========================
# END RANKING
# =========================


bcrypt = Bcrypt(app)
app.secret_key = 'your-secret-key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        if action == 'register':
            # Cek apakah username/email sudah terdaftar
            cur.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
            if cur.fetchone():
                flash("Username atau email sudah digunakan!")
            else:
                hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
                cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                            (username, email, hashed_pw))
                mysql.connection.commit()
                flash("Registrasi berhasil! Silakan login.")
            cur.close()
            return redirect(url_for('login'))

        elif action == 'login':
            cur.execute("SELECT id, password FROM users WHERE username=%s AND email=%s", (username, email))
            user = cur.fetchone()
            if user and bcrypt.check_password_hash(user[1], password):
                session['user_id'] = user[0]
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Login gagal: username/email/password salah")
            cur.close()
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True,port=5050)
