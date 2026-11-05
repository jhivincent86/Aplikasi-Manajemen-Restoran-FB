from controllers.main_controller import (
    inisialisasi_data, handle_registrasi_menu, handle_registrasi_meja,
    handle_buka_meja, handle_tambah_pesanan, handle_kirim_ke_dapur,
    handle_proses_dapur, handle_cetak_tagihan
)
from views.main_menu import tampilkan_menu_utama, jeda_sebelum_kembali

daftar_menu, daftar_meja, pesanan_aktif = inisialisasi_data()

while True:
    tampilkan_menu_utama()
    pilihan = input("Pilih menu (0-7): ")

    if pilihan == '0':
        print("\n👋 Terima kasih telah menggunakan aplikasi ini!")
        break
    elif pilihan == '1':
        handle_registrasi_menu(daftar_menu)
    elif pilihan == '2':
        handle_registrasi_meja(daftar_meja)
    elif pilihan == '3':
        handle_buka_meja(daftar_meja, pesanan_aktif)
    elif pilihan == '4':
        handle_tambah_pesanan(pesanan_aktif, daftar_menu)
    elif pilihan == '5':
        handle_kirim_ke_dapur(pesanan_aktif)
    elif pilihan == '6':
        handle_proses_dapur(pesanan_aktif)
    elif pilihan == '7':
        handle_cetak_tagihan(pesanan_aktif)
    else:
        print("❌ Pilihan tidak valid, silakan coba lagi.")
        jeda_sebelum_kembali()