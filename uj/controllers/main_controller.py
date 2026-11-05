from models.menu_items import FoodItem, BeverageItem
from models.table import Table
from models.order import Order
from exceptions.custom_exceptions import TableNotAvailableException
from services.kitchen import Kitchen
from views.main_menu import tampilkan_header, tampilkan_list_meja, tampilkan_katalog_menu, jeda_sebelum_kembali

def inisialisasi_data():
    daftar_menu = [
        FoodItem("Nasi Goreng", "Utama", 25000, 10),
        FoodItem("Ayam Bakar", "Utama", 30000, 5),
        BeverageItem("Es Teh", "Minuman", 5000, 20),
        BeverageItem("Kopi", "Minuman", 15000, 15)
    ]
    daftar_meja = {
        1: Table(nomor=1, kapasitas=4),
        2: Table(nomor=2, kapasitas=2),
        3: Table(nomor=3, kapasitas=6)
    }
    pesanan_aktif = {}
    return daftar_menu, daftar_meja, pesanan_aktif

def handle_registrasi_menu(daftar_menu):
    tampilkan_header("REGISTRASI MENU BARU")
    
    while True:
        jenis = input("Kategori (1. Makanan / 2. Minuman / 0. Batal): ")
        if jenis == '0':
            return
        if jenis in ['1', '2']:
            break
        print("❌ Kategori tidak valid! Harap pilih 1 atau 2.\n")
        
    while True:
        nama = input("Masukkan nama menu: ")
        if nama.strip():
            break
        print("❌ Nama menu tidak boleh kosong!\n")
        
    while True:
        try:
            harga = float(input("Masukkan harga (contoh: 15000): "))
            stok = int(input("Masukkan jumlah stok awal: "))
            
            if jenis == '1':
                menu_baru = FoodItem(nama, "Utama", harga, stok)
            else:
                menu_baru = BeverageItem(nama, "Minuman", harga, stok)
                
            daftar_menu.append(menu_baru)
            print(f"\n✅ Berhasil mendaftarkan {nama}")
            break
        except ValueError as e:
            if "could not convert" in str(e).lower() or "invalid literal" in str(e).lower():
                print("❌ GAGAL: Harga dan stok harus berupa angka!\n")
            else:
                print(f"❌ GAGAL: {e}\n")
                
    jeda_sebelum_kembali()

def handle_registrasi_meja(daftar_meja):
    tampilkan_header("REGISTRASI MEJA BARU")
    
    while True:
        input_nomor = input("Masukkan nomor meja baru (atau 0 untuk batal): ")
        if input_nomor == '0':
            return
            
        try:
            nomor = int(input_nomor)
            if nomor in daftar_meja:
                print(f"❌ Nomor meja {nomor} sudah ada di sistem!\n")
                continue
                
            kapasitas = int(input("Masukkan kapasitas maksimal orang: "))
            meja_baru = Table(nomor, kapasitas)
            daftar_meja[nomor] = meja_baru
            print(f"\n✅ Berhasil mendaftarkan Meja {nomor} dengan kapasitas {kapasitas} orang.")
            break
        except ValueError as e:
            if "invalid literal" in str(e).lower() or "could not convert" in str(e).lower():
                print("❌ GAGAL: Nomor meja dan kapasitas harus berupa angka!\n")
            else:
                print(f"❌ GAGAL: {e}\n")
                
    jeda_sebelum_kembali()

def handle_buka_meja(daftar_meja, pesanan_aktif):
    tampilkan_header("BUKA MEJA")
    tampilkan_list_meja(daftar_meja)

    while True:    
        input_nomor = input("Masukkan nomor meja yang dibuka (0 untuk batal): ")
        if input_nomor == '0':
            break
            
        try:
            nomor = int(input_nomor)
            if nomor not in daftar_meja:
                print("❌ Nomor meja tidak terdaftar di sistem!\n")
                continue
                
            jumlah_tamu = int(input("Masukkan jumlah tamu: "))
            meja = daftar_meja[nomor]
            
            meja.buka_meja(jumlah_tamu)
            pesanan_aktif[nomor] = Order(meja)
            
            jeda_sebelum_kembali()
            break
        except TableNotAvailableException as e:
            print(f"❌ GAGAL: {e}\n")
        except ValueError as e:
            if "invalid literal" in str(e).lower() or "could not convert" in str(e).lower():
                print("❌ GAGAL: Input harus berupa angka!\n")
            else:
                print(f"❌ GAGAL: {e}\n")

def handle_tambah_pesanan(pesanan_aktif, daftar_menu):
    while True:
        tampilkan_header("TAMBAH PESANAN")
        if not pesanan_aktif:
            print("❌ Belum ada meja yang dibuka! Silakan buka meja (Menu 5) terlebih dahulu.")
            jeda_sebelum_kembali()
            break
            
        print("Meja aktif saat ini:", ", ".join(map(str, pesanan_aktif.keys())))
        print("-" * 35)
        
        input_nomor = input("\nMasukkan nomor meja (0 untuk batal): ")
        if input_nomor == '0':
            break
            
        try:
            nomor = int(input_nomor)
            if nomor not in pesanan_aktif:
                print("❌ Meja ini belum dibuka atau tidak memiliki pesanan aktif!\n")
                continue
                
            order_meja = pesanan_aktif[nomor]
            
            while True:
                tampilkan_header(f"TAMBAH PESANAN - MEJA {nomor}")
                tampilkan_katalog_menu(daftar_menu)
                
                while True:
                    nama_item = input("\nMasukkan nama menu yang dipesan (0 selesai memesan): ")
                    if nama_item == '0':
                        break
                        
                    item_ditemukan = next((m for m in daftar_menu if m.nama.lower() == nama_item.lower()), None)
                    if item_ditemukan:
                        break 

                    print(f"❌ Menu '{nama_item}' tidak ditemukan! Silakan cek kembali penulisannya.\n")
                
                if nama_item == '0':
                    print(f"\n✅ Selesai mencatat pesanan untuk Meja {nomor}.")
                    break 
                
                while True:
                    qty_input = input(f"Masukkan jumlah pesanan untuk '{item_ditemukan.nama}': ")
                    if not qty_input.isdigit():
                        print("❌ Input jumlah (Qty) harus berupa angka bulat positif!\n")
                        continue
                    
                    qty = int(qty_input)
                    if qty <= 0:
                        print("❌ Qty harus lebih dari 0!\n")
                        continue
                    break
                    
                catatan = input("Masukkan catatan (opsional, enter jika kosong): ")
                
                try:
                    order_meja.tambah_item(daftar_menu, nama_item, qty, catatan)
                    input("\nTekan Enter untuk menambah pesanan lain...") 
                except ValueError as e: 
                    print(f"❌ GAGAL: {e}")
                    input("\nTekan Enter untuk mengulang pesanan item ini...") 
            
            jeda_sebelum_kembali()
            break 
            
        except ValueError:
            print("❌ Input nomor meja harus berupa angka!\n")

def handle_kirim_ke_dapur(pesanan_aktif):
    tampilkan_header("KIRIM ORDER KE DAPUR")
    
    meja_belum_dikirim = [
        no for no, order in pesanan_aktif.items() 
        if order.status == "DRAFT" and len(order.items) > 0
    ]
    
    if not meja_belum_dikirim:
        print("✅ Semua pesanan saat ini sudah terkirim ke dapur (atau belum ada pesanan baru).")
        jeda_sebelum_kembali()
        return
        
    print("Antrean meja yang belum dikirim (DRAFT):", ", ".join(map(str, meja_belum_dikirim)))
        
    while True:
        input_nomor = input("\nMasukkan nomor meja yang ingin dikirim (0 untuk batal): ")
        if input_nomor == '0':
            return
            
        try:
            nomor = int(input_nomor)
            if nomor not in pesanan_aktif:
                print("❌ Meja belum dibuka/tidak ada pesanan aktif!\n")
                continue
                
            order_meja = pesanan_aktif[nomor]
            
            if not order_meja.items:
                print("⚠️ Belum ada item yang dipesan untuk meja ini.\n")
                continue
            elif order_meja.status == "DIKONFIRMASI":
                print("⚠️ Pesanan meja ini sudah dikirim ke dapur sebelumnya.\n")
                continue
            else:
                print("\n--- Daftar Pesanan Meja", nomor, "---")
                for item in order_meja.items:
                    catatan = f" (Catatan: {item.catatan})" if item.catatan else ""
                    print(f"- {item.menu_item.nama} x{item.qty}{catatan} -> Status: {item.status}")
                print("---------------------------------")
                order_meja.kirim_ke_dapur() 
                break
        except ValueError:
            print("❌ Input harus berupa angka!\n")
            
    jeda_sebelum_kembali()

def handle_proses_dapur(pesanan_aktif):
    tampilkan_header("KITCHEN DISPLAY (SISTEM DAPUR)")
    meja_menunggu = [no for no, order in pesanan_aktif.items() if order.status == "DIKONFIRMASI"]
    
    if not meja_menunggu:
        print("✅ Tidak ada antrean pesanan di dapur saat ini.")
        jeda_sebelum_kembali()
        return

    print("Antrean Pesanan Masuk (Meja):", ", ".join(map(str, meja_menunggu)))
    
    while True:
        input_nomor = input("\nPilih nomor meja yang ingin diproses masakannya (0 untuk batal): ")
        if input_nomor == '0':
            return
            
        try:
            nomor = int(input_nomor)
            if nomor not in meja_menunggu:
                print("❌ Meja tersebut tidak ada dalam antrean dapur!\n")
                continue
                
            order_meja = pesanan_aktif[nomor]
            print("\n--- Memproses Masakan ---")
            semua_siap = True
            
            for item in order_meja.items:
                if item.status == "SIAP":
                    continue
                    
                print(f"\nItem: {item.menu_item.nama} (Qty: {item.qty}) - Catatan: {item.catatan}")
                print("Status saat ini:", item.status)
                
                while True:
                    aksi = input("Pilih aksi (1. Set DIMASAK / 2. Set SIAP / 0. Lewati): ")
                    if aksi in ['1', '2', '0']:
                        break
                    print("❌ Pilihan tidak valid! Harap ketik 1, 2, atau 0.\n")
                    
                if aksi == '1':
                    Kitchen.update_status_item(item, "DIMASAK")
                    semua_siap = False
                elif aksi == '2':
                    Kitchen.update_status_item(item, "SIAP")
                else:
                    semua_siap = False
            
            if semua_siap:
                print(f"\n✅ Semua makanan untuk Meja {nomor} telah SIAP disajikan!")
            break
            
        except ValueError:
            print("❌ Input harus berupa angka!\n")
            
    jeda_sebelum_kembali()

def handle_cetak_tagihan(pesanan_aktif):
    tampilkan_header("CETAK TAGIHAN")
    
    if not pesanan_aktif:
        print("❌ Tidak ada meja yang memiliki pesanan aktif saat ini.")
        jeda_sebelum_kembali()
        return

    print("Meja dengan pesanan aktif:", ", ".join(map(str, pesanan_aktif.keys())))
    print("-" * 35)
    
    while True:
        input_nomor = input("\nMasukkan nomor meja untuk dicetak tagihannya (0 untuk batal): ")
        if input_nomor == '0':
            return
            
        try:
            nomor = int(input_nomor)
            if nomor not in pesanan_aktif:
                print("❌ Tidak ada pesanan aktif di meja ini!\n")
                continue
                
            order_meja = pesanan_aktif[nomor]
            total = order_meja.hitung_total()
            
            print("\n" + "="*35)
            print(f"🧾 STRUK TAGIHAN - MEJA {nomor}")
            print("=" * 35)
            for item in order_meja.items:
                subtotal = item.qty * item.menu_item.harga
                print(f"{item.menu_item.nama} x{item.qty} : Rp{subtotal:,.0f}")
                if item.catatan:
                    print(f"  *Catatan: {item.catatan}")
            print("-" * 35)
            print(f"TOTAL TAGIHAN : Rp{total:,.0f}")
            print("=" * 35)
            break
            
        except ValueError:
            print("❌ Input harus berupa angka!\n")
            
    jeda_sebelum_kembali()