from models.menu_base import MenuItemBase

class FoodItem(MenuItemBase):
    def tampilkan_info(self) -> str:
        return f"[Makanan] {self.nama} - Rp{self.harga:,.0f} (Stok: {self.stok})"

class BeverageItem(MenuItemBase):
    def tampilkan_info(self) -> str:
        return f"[Minuman] {self.nama} - Rp{self.harga:,.0f} (Stok: {self.stok})"