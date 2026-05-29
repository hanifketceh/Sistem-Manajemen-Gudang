#models

class Barang:
    def __init__(self, sku, nama, stok, harga):
        self.sku = sku
        self.nama = nama
        self.stok = stok
        self.harga = harga

    def info(self):
        return f"[{self.sku}] {self.nama} | Stok: {self.stok} | Harga: Rp{self.harga}"

class BarangElektronik(Barang):
    def __init__(self, sku, nama, stok, harga, garansi_bulan):
        super().__init__(sku, nama, stok, harga)
        self.garansi_bulan = garansi_bulan

    def info(self):
        return f"[Elektronik] {super().info()} | Garansi: {self.garansi_bulan} Bulan"

class BarangPecahBelah(Barang):
    def __init__(self, sku, nama, stok, harga, proteksi):
        super().__init__(sku, nama, stok, harga)
        self.proteksi = proteksi

    def info(self):
        return f"[Pecah Belah] {super().info()} | Proteksi: {self.proteksi}"