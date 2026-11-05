from exceptions.custom_exceptions import TableNotAvailableException

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