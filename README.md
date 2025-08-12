###
![Dashboard Aplikasi](./dashboard.png) <br>
**Travel Mind** adalah platform web perencanaan itinerary perjalanan cerdas yang dirancang untuk membantu wisatawan individu dalam membuat, mengelola, dan memvisualisasikan rencana perjalanan mereka. Sistem ini memanfaatkan preferensi wisatawan untuk memberikan rekomendasi destinasi dan membantu menyusun jadwal perjalanan yang dipersonalisasi.

**Tujuan Utama Sistem:**
<br>
●	Perencanaan Perjalanan yang Dipersonalisasi: Menyediakan alat bagi wisatawan untuk membuat itinerary yang disesuaikan dengan minat, gaya perjalanan, durasi, dan tujuan spesifik mereka, dengan bantuan rekomendasi berbasis AI. <br>
●	Efisiensi dan Kemudahan Wisatawan: Mengurangi kompleksitas dan waktu yang dibutuhkan untuk merencanakan perjalanan dengan antarmuka yang intuitif dan fitur pengelolaan itinerary yang terpusat.<br>
●	Visualisasi Perjalanan yang Jelas: Membantu wisatawan memahami rencana perjalanan mereka melalui tampilan daftar destinasi per hari yang terstruktur dan representasi visual di peta interaktif.<br>
●	Fleksibilitas Pengelolaan: Memberikan kemampuan kepada wisatawan untuk dengan mudah memodifikasi, mengatur ulang, dan menyimpan berbagai versi itinerary mereka.<br>

**Ruang Lingkup Sistem:**<br>
●	Perencanaan Perjalanan yang Dipersonalisasi: Menyediakan alat bagi wisatawan untuk membuat itinerary yang disesuaikan dengan minat, gaya perjalanan, durasi, dan tujuan spesifik mereka, dengan bantuan rekomendasi berbasis AI.<br>
●	Efisiensi dan Kemudahan Wisatawan: Mengurangi kompleksitas dan waktu yang dibutuhkan untuk merencanakan perjalanan dengan antarmuka yang intuitif dan fitur pengelolaan itinerary yang terpusat.<br>
●	Visualisasi Perjalanan yang Jelas: Membantu wisatawan memahami rencana perjalanan mereka melalui tampilan daftar destinasi per hari yang terstruktur dan representasi visual di peta interaktif.<br>
●	Fleksibilitas Pengelolaan: Memberikan kemampuan kepada wisatawan untuk dengan mudah memodifikasi, mengatur ulang, dan menyimpan berbagai versi itinerary mereka.<br>

**Panduan Instalasi Proyek "Travel Mind" Secara Manual**

Berikut adalah cara untuk menjalankan proyek "Travel Mind" di komputermu. Proyek ini terdiri dari dua bagian: **Backend** (server) dan **Frontend** (tampilan website). Kamu perlu menjalankan keduanya secara bersamaan.

**Prasyarat (Software yang Perlu Diinstal Terlebih Dahulu):**

1.  **Python:** Pastikan kamu sudah menginstal Python (versi 3.8 atau lebih baru). Cek dengan membuka Command Prompt/Terminal dan mengetik `python --version`.
2.  **Node.js dan npm:** Pastikan kamu sudah menginstal Node.js (versi 16 atau lebih baru direkomendasikan). Ini biasanya sudah termasuk npm. Cek dengan mengetik `node -v` dan `npm -v`.
3.  **MySQL Server:** Kamu perlu server database MySQL yang berjalan di komputermu. Kamu bisa menginstal MySQL Community Server atau menggunakan XAMPP/WAMP yang sudah termasuk MySQL.

---

**Langkah 1: Dapatkan Kode Proyek**

1.  Saya akan memberikanmu folder proyek dalam bentuk file ZIP (misalnya `travel-mind.zip`).
2.  Ekstrak file ZIP ini ke lokasi yang kamu inginkan di komputermu (misalnya, di `C:\Projects\` atau `~/Documents/Projects/`).
3.  Sekarang kamu akan memiliki folder bernama `travel-mind` yang berisi subfolder `backend` dan `frontend`.

---

**Langkah 2: Menyiapkan dan Menjalankan Backend (Flask)**

1.  **Buka Terminal atau Command Prompt.**

2.  **Masuk ke Direktori Backend:**
    ```bash
    cd path/ke/folder/travel-mind/backend
    ```
    (Ganti `path/ke/folder` dengan lokasi sebenarnya).

3.  **Buat Virtual Environment:** Ini penting untuk mengisolasi library Python proyek ini.
    ```bash
    python -m venv venv
    ```

4.  **Aktifkan Virtual Environment:**
    *   **Di Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **Di macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    Setelah ini, kamu akan melihat `(venv)` di awal baris terminalmu.

5.  **Install Semua Library yang Dibutuhkan:**
    Saya sudah menyertakan file `requirements.txt` yang berisi daftar semua library. Jalankan perintah:
    ```bash
    pip install -r requirements.txt
    ```

6.  **Setup Database MySQL:**
    *   Buka tool database MySQL Anda (MySQL Workbench, DBeaver, phpMyAdmin, dll.).
    *   Buat database baru dengan nama persis: `travel_mind_db`.
        ```sql
        CREATE DATABASE travel_mind_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        ```

7.  **Konfigurasi Koneksi Database:**
    *   Di dalam folder `backend`, cari file `.env`. Jika tidak ada, buat file baru bernama `.env`.
    *   Salin konten ini ke dalamnya dan **sesuaikan dengan konfigurasi MySQL-mu**:
        ```ini
        # backend/.env
        FLASK_APP=app.py
        FLASK_DEBUG=True
        
        # GANTI DENGAN USERNAME, PASSWORD, HOST, DAN PORT MYSQL KAMU
        # Contoh jika pakai XAMPP/default: user 'root', password kosong
        DATABASE_URL="mysql+pymysql://root:PASSWORD_ANDA@localhost:3306/travel_mind_db"

        # Ganti ini dengan string acak yang panjang
        SECRET_KEY="ganti-dengan-kunci-rahasia-yang-sangat-aman"
        JWT_SECRET_KEY="ganti-juga-ini-dengan-kunci-rahasia-lain"
        ORS_API_KEY="masukkan-api-key-openrouteservice-di-sini"
        ```
    *   Pastikan kamu mengganti `PASSWORD_ANDA` dan `ORS_API_KEY`.

8.  **Terapkan Struktur Database (Migrasi):**
    Jalankan dua perintah ini secara berurutan di terminal (pastikan `venv` masih aktif):
    ```bash
    flask db upgrade
    ```
    Ini akan membuat semua tabel yang dibutuhkan di dalam database `travel_mind_db`.

9.  **Jalankan Server Backend:**
    ```bash
    flask run
    ```
    Jika berhasil, kamu akan melihat pesan bahwa server berjalan di `http://127.0.0.1:5000`. **Biarkan terminal ini tetap terbuka.**

---

**Langkah 3: Menyiapkan dan Menjalankan Frontend (Vue.js)**

1.  **Buka Terminal atau Command Prompt BARU.** (Jangan tutup terminal backend).

2.  **Masuk ke Direktori Frontend:**
    ```bash
    cd path/ke/folder/travel-mind/frontend
    ```

3.  **Install Semua Dependensi JavaScript:**
    Perintah ini akan membaca file `package.json` dan mengunduh semua library yang dibutuhkan. Ini mungkin butuh beberapa menit.
    ```bash
    npm install
    ```

4.  **Jalankan Server Development Frontend:**
    ```bash
    npm run dev
    ```
    Jika berhasil, kamu akan melihat pesan bahwa server berjalan di alamat seperti `http://localhost:5173` (port bisa berbeda).

---

**Langkah 4: Selesai!**

1.  Buka browser web Anda (Chrome, Firefox, dll.).
2.  Akses alamat frontend yang muncul di terminal, misalnya **`http://localhost:5173`**.
3.  Sekarang kamu bisa menggunakan aplikasi "Travel Mind"! Kamu bisa mendaftar akun baru, login, dan mencoba semua fiturnya.

Kedua terminal (satu untuk backend, satu untuk frontend) harus tetap berjalan selama kamu menggunakan aplikasi. Untuk menghentikannya, tekan `Ctrl + C` di masing-masing terminal.

Selamat mencoba
