import os
import msvcrt
from abc import ABC, abstractmethod

class MenuItemNotFoundException(Exception):
    pass

class TableNotAvailableException(Exception):
    pass

class MenuItemBase(ABC):
    def __init__(self, nama: str, kategori: str, harga: float, stok: int):
        self.nama = nama
        self.kategori = kategori
        self.harga = harga
        self.stok = stok

    @property
    def harga(self) -> float:
        return self._harga

    @harga.setter
    def harga(self, value: float):
        if value < 0:
            raise ValueError("Harga tidak boleh bernilai negatif!")
        self._harga = value

    @property
    def stok(self) -> int:
        return self._stok

    @stok.setter
    def stok(self, value: int):
        if value < 0:
            raise ValueError("Stok tidak boleh bernilai negatif!")
        self._stok = value

    @abstractmethod
    def tampilkan_info(self) -> str:
        pass

class FoodItem(MenuItemBase):
    def tampilkan_info(self) -> str:
        return f"[Makanan] {self.nama} - Rp{self.harga:,.0f} (Stok: {self.stok})"

class BeverageItem(MenuItemBase):
    def tampilkan_info(self) -> str:
        return f"[Minuman] {self.nama} - Rp{self.harga:,.0f} (Stok: {self.stok})"

class Table:
    def __init__(self, nomor: int, kapasitas: int):
        self.nomor = nomor
        self.kapasitas = kapasitas
        self.__status = "KOSONG"

    @property
    def nomor(self) -> int:
        return self._nomor

    @nomor.setter
    def nomor(self, value: int):
        if value <= 0:
            raise ValueError("Nomor meja tidak boleh nol atau negatif!")
        self._nomor = value

    @property
    def kapasitas(self) -> int:
        return self._kapasitas

    @kapasitas.setter
    def kapasitas(self, value: int):
        if value <= 0:
            raise ValueError("Kapasitas meja harus lebih dari 0!")
        self._kapasitas = value

    @property
    def status(self) -> str:
        return self.__status

    def buka_meja(self, jumlah_tamu: int):
        if jumlah_tamu <= 0:
            raise ValueError("Jumlah tamu harus lebih dari 0!")
        
        if self.__status == "TERISI":
            raise TableNotAvailableException(f"Meja {self.nomor} sedang terisi!")
            
        if jumlah_tamu > self.kapasitas:
            raise ValueError(f"Jumlah tamu ({jumlah_tamu}) melebihi kapasitas meja ({self.kapasitas}).")
        
        self.__status = "TERISI"
        print(f"✅ Meja {self.nomor} berhasil dibuka untuk {jumlah_tamu} tamu.")

class OrderItem:
    def __init__(self, menu_item: MenuItemBase, qty: int, catatan: str = ""):
        self.menu_item = menu_item
        self.qty = qty
        self.catatan = catatan
        self.status = "PENDING"

class Order:
    def __init__(self, table: Table):
        self.table = table
        self.items = []
        self.status = "DRAFT"

    def tambah_item(self, daftar_menu: list, nama_item: str, qty: int, catatan: str = ""):
        item_ditemukan = next((m for m in daftar_menu if m.nama.lower() == nama_item.lower()), None)
        
        if not item_ditemukan:
            raise MenuItemNotFoundException(f"Menu '{nama_item}' tidak ditemukan di sistem!")
        if item_ditemukan.stok < qty:
            raise ValueError(f"Stok '{nama_item}' tidak mencukupi! Sisa stok: {item_ditemukan.stok}")
        
        item_ditemukan.stok -= qty
        pesanan_baru = OrderItem(item_ditemukan, qty, catatan)
        self.items.append(pesanan_baru)
        
        self.status = "DRAFT"
        print(f"➕ Berhasil menambahkan {qty}x {item_ditemukan.nama} ke pesanan Meja {self.table.nomor}.")

    def kirim_ke_dapur(self):
        self.status = "DIKONFIRMASI"
        print(f"✅ Pesanan Meja {self.table.nomor} berhasil dikirim ke dapur.")

    def hitung_total(self) -> float:
        total = sum(item.qty * item.menu_item.harga for item in self.items)
        return total

class Kitchen:
    @staticmethod
    def update_status_item(order_item: OrderItem, status_baru: str):
        order_item.status = status_baru
        print(f"👨‍🍳 Dapur: Status '{order_item.menu_item.nama}' (Qty: {order_item.qty}) diupdate menjadi -> {status_baru}")

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
    print("3. Lihat Daftar Menu")
    print("4. Lihat Status Meja")
    print("5. Buka Meja (Terima Tamu)")
    print("6. Tambah Pesanan")
    print("7. [Pelayan] Kirim Order ke Dapur")
    print("8. [Dapur] Update Status Masakan")
    print("9. Cetak Tagihan (Billing)")
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
    
    while True:
        input_nomor = input("Masukkan nomor meja untuk dicetak tagihannya (0 untuk batal): ")
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

def main():
    daftar_menu, daftar_meja, pesanan_aktif = inisialisasi_data()

    while True:
        tampilkan_menu_utama()
        pilihan = input("Pilih menu (0-9): ")

        if pilihan == '0':
            print("\n👋 Terima kasih telah menggunakan aplikasi ini!")
            break
        elif pilihan == '1':
            handle_registrasi_menu(daftar_menu)
        elif pilihan == '2':
            handle_registrasi_meja(daftar_meja)
        elif pilihan == '3':
            tampilkan_header("DAFTAR MENU TERSEDIA")
            tampilkan_katalog_menu(daftar_menu)
            jeda_sebelum_kembali()
        elif pilihan == '4':
            tampilkan_header("STATUS MEJA")
            tampilkan_list_meja(daftar_meja)
            jeda_sebelum_kembali()
        elif pilihan == '5':
            handle_buka_meja(daftar_meja, pesanan_aktif)
        elif pilihan == '6':
            handle_tambah_pesanan(pesanan_aktif, daftar_menu)
        elif pilihan == '7':
            handle_kirim_ke_dapur(pesanan_aktif)
        elif pilihan == '8':
            handle_proses_dapur(pesanan_aktif)
        elif pilihan == '9':
            handle_cetak_tagihan(pesanan_aktif)
        else:
            print("❌ Pilihan tidak valid, silakan coba lagi.")
            jeda_sebelum_kembali()

if __name__ == "__main__":
    main()