README.md
====================================================================
# 🍽️ Aplikasi Manajemen Restoran & F&B (OOP Python)

Aplikasi ini adalah sistem manajemen operasional restoran berbasis *Command Line Interface* (CLI) yang dibangun menggunakan bahasa pemrograman Python. Proyek ini dikembangkan untuk memenuhi Tugas Proyek Mata Kuliah Pemrograman Berorientasi Objek (PBO) di Universitas Mikroskil.

## ✨ Fitur Utama
- **Manajemen Menu**: Registrasi makanan dan minuman dengan validasi stok dan harga secara ketat (Enkapsulasi).
- **Manajemen Meja**: Pendaftaran meja dan pemantauan kapasitas serta status (Kosong/Terisi).
- **Pencatatan Pesanan**: Penambahan pesanan dengan sistem validasi nama menu dan pengurangan stok otomatis.
- **Kitchen Display**: Pengiriman pesanan ke area dapur dan pembaruan status masakan (Draft -> Dikonfirmasi -> Dimasak -> Siap).
- **Sistem Kasir (Billing)**: Pencetakan struk tagihan pelanggan secara instan dan akurat.

## 🚀 Cara Menjalankan Program 
Pastikan Python 3.x sudah terinstal di komputer/laptop Anda. Anda dapat mengunduh dan menjalankan aplikasi ini menggunakan salah satu dari dua cara berikut:
#Opsi 1: Menggunakan Git (Direkomendasikan)
Buka terminal atau Command Prompt (CMD).
Clone repository ini ke komputer Anda dengan menjalankan perintah:
```bash
   git clone https://github.com/jhivincent86/Aplikasi-Manajemen-Restoran-FB.git
   ```
Masuk ke dalam direktori folder proyek:
```bash
   cd Aplikasi-Manajemen-Restoran-FB
   ```
#Opsi 2: Tanpa Git (Download ZIP)
Unduh kode sumber aplikasi ini dengan cara:
Klik tombol hijau `<> Code` di bagian atas halaman GitHub.
Pilih `Download ZIP`.
Atau langsung klik Link Download Ini.
Ekstrak (Unzip) file yang baru saja diunduh tersebut ke folder pilihan Anda.
Buka terminal atau Command Prompt (CMD), lalu arahkan ke dalam folder hasil ekstrak tersebut. Contoh:
```bash
   cd Downloads/Aplikasi-Manajemen-Restoran-FB-main
   ```
Menjalankan Aplikasi
Setelah Anda berada di dalam direktori proyek (menggunakan Opsi 1 atau Opsi 2), jalankan program utama dengan perintah:
```bash
python main.py
```
(Catatan: Gunakan perintah `py main.py` atau `python3 main.py` jika perintah di atas tidak dikenali oleh sistem Anda).

   
## 🛠️ Konsep OOP yang Diterapkan

Aplikasi ini diarsiteki dengan prinsip Object-Oriented Programming (OOP) murni:

- Abstract Class (ABC): Diimplementasikan pada cetak biru MenuItemBase.
- Inheritance (Pewarisan): Pemisahan karakteristik objek pada FoodItem dan BeverageItem.
- Encapsulation (Pengkapsulan): Perlindungan data sensitif seperti harga, stok, dan nomor meja menggunakan dekorator @property (Getter/Setter).
- Polymorphism (Polimorfisme): Method overriding pada fungsi tampilkan_info().
- Custom Exception: Penanganan error spesifik domain seperti MenuItemNotFoundException dan TableNotAvailableException.
