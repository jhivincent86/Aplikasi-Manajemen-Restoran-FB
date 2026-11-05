from abc import ABC, abstractmethod

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