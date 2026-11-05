from models.menu_base import MenuItemBase
from models.table import Table
from exceptions.custom_exceptions import MenuItemNotFoundException

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