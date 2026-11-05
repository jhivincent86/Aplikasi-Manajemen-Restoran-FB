import os
import msvcrt
from models.menu_items import FoodItem, BeverageItem

def membersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def jeda_sebelum_kembali():
    print("\nTekan tombol apa saja untuk kembali ke menu awal...")
    msvcrt.getch()

def tampilkan_menu_utama():
    membersihkan_layar()
    print("="*45)
    print("🍽️ APLIKASI MANAJEMEN RESTORAN & F&B")
    print("="*45)
    print("1. Registrasi Menu Baru")
    print("2. Registrasi Meja Baru")
    print("3. Buka Meja (Terima Tamu)")
    print("4. Tambah Pesanan")
    print("5. [Pelayan] Kirim Order ke Dapur")
    print("6. [Dapur] Update Status Masakan")
    print("7. Cetak Tagihan (Billing)")
    print("0. Keluar")
    print("="*45)

def tampilkan_header(judul: str):
    membersihkan_layar()
    print(f"[{judul.upper()}]")
    print("-" * 45)

def tampilkan_list_meja(daftar_meja: dict):
    print("Daftar Meja Saat Ini:")
    for nomor_meja, obj_meja in daftar_meja.items():
        simbol = "🟢" if obj_meja.status == "KOSONG" else "🔴"
        print(f"{simbol} Meja {nomor_meja} (Kapasitas: {obj_meja.kapasitas} orang) -> {obj_meja.status}")
    print("-" * 45)

def tampilkan_katalog_menu(daftar_menu):
    if not daftar_menu:
        print("Belum ada menu yang terdaftar di sistem.")
        return

    print("🍽️  --- KATEGORI MAKANAN ---")
    ada_makanan = False
    for menu in daftar_menu:
        if isinstance(menu, FoodItem):
            print(menu.tampilkan_info())
            ada_makanan = True
    if not ada_makanan:
        print("- Belum ada makanan yang terdaftar -")

    print("\n🍹 --- KATEGORI MINUMAN ---")
    ada_minuman = False
    for menu in daftar_menu:
        if isinstance(menu, BeverageItem):
            print(menu.tampilkan_info())
            ada_minuman = True
    if not ada_minuman:
        print("- Belum ada minuman yang terdaftar -")
    print("-" * 45)