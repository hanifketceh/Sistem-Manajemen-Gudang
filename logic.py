import random
import string
from datetime import datetime

from structures import (
    HashTableInventaris,
    LinkedListTransaksi,
    Stack,
    Queue,
    BinarySearchTree,
    merge_sort,
    binary_search,
)


class SistemInventaris:
    BATAS_STOK_RENDAH = 10

    def __init__(self):
        # Inisialisasi semua struktur data
        self.inventaris       = HashTableInventaris()
        self.riwayat          = LinkedListTransaksi()
        self.undo_stack       = Stack()
        self.notifikasi_queue = Queue()
        self.bst              = BinarySearchTree()

        self._isi_data_awal()

    # --------------------------------------------------------
    # Helper
    # --------------------------------------------------------
    def _generate_id(self):
        return 'PRD-' + ''.join(random.choices(string.digits, k=5))

    def _isi_data_awal(self):
        data_awal = [
            {'id': 'PRD-00001', 'nama': 'Laptop ASUS VivoBook',   'kategori': 'Elektronik', 'stok': 15, 'harga': 7500000, 'lokasi': 'Rak A1'},
            {'id': 'PRD-00002', 'nama': 'Monitor LG 24"',         'kategori': 'Elektronik', 'stok': 8,  'harga': 2200000, 'lokasi': 'Rak A2'},
            {'id': 'PRD-00003', 'nama': 'Keyboard Mechanical',    'kategori': 'Aksesoris',  'stok': 25, 'harga': 450000,  'lokasi': 'Rak B1'},
            {'id': 'PRD-00004', 'nama': 'Mouse Wireless',         'kategori': 'Aksesoris',  'stok': 5,  'harga': 180000,  'lokasi': 'Rak B2'},
            {'id': 'PRD-00005', 'nama': 'Kabel HDMI 2m',          'kategori': 'Kabel',      'stok': 50, 'harga': 75000,   'lokasi': 'Rak C1'},
            {'id': 'PRD-00006', 'nama': 'Hard Disk Eksternal 1TB','kategori': 'Storage',    'stok': 3,  'harga': 850000,  'lokasi': 'Rak A3'},
            {'id': 'PRD-00007', 'nama': 'RAM DDR4 8GB',           'kategori': 'Komponen',   'stok': 20, 'harga': 320000,  'lokasi': 'Rak D1'},
            {'id': 'PRD-00008', 'nama': 'SSD 512GB',              'kategori': 'Storage',    'stok': 12, 'harga': 650000,  'lokasi': 'Rak D2'},
        ]
        for p in data_awal:
            self.inventaris.insert(p['id'], p)
            self.bst.insert(p['nama'], p)
        self._cek_stok_rendah()

    def _catat_riwayat(self, aksi, detail):
        self.riwayat.tambah({
            'waktu': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'aksi' : aksi,
            'detail': detail,
        })

    def _cek_stok_rendah(self):
        """Rebuild antrian notifikasi stok rendah (Queue)"""
        self.notifikasi_queue.hapus_semua()
        for p in self.inventaris.get_semua():
            if p['stok'] <= self.BATAS_STOK_RENDAH:
                self.notifikasi_queue.enqueue(
                    f"⚠ Stok rendah: {p['nama']} ({p['stok']} unit)"
                )

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------
    def tambah_produk(self, nama, kategori, stok, harga, lokasi):
        """Tambah produk baru ke Hash Table & BST"""
        id_baru = self._generate_id()
        while self.inventaris.exists(id_baru):
            id_baru = self._generate_id()

        produk = {
            'id'      : id_baru,
            'nama'    : nama,
            'kategori': kategori,
            'stok'    : int(stok),
            'harga'   : int(harga),
            'lokasi'  : lokasi,
        }
        self.inventaris.insert(id_baru, produk)
        self.bst.insert(nama, produk)
        self.undo_stack.push({'aksi': 'tambah', 'produk': produk})
        self._catat_riwayat('TAMBAH', f"Produk baru: {nama} (ID: {id_baru})")
        self._cek_stok_rendah()
        return id_baru

    # --------------------------------------------------------
    # READ
    # --------------------------------------------------------
    def baca_produk(self, id_produk):
        """Ambil satu produk dari Hash Table by ID"""
        return self.inventaris.get(id_produk)

    def get_semua_terurut(self, key='nama'):
        """Ambil semua produk, urutkan dengan Merge Sort"""
        return merge_sort(self.inventaris.get_semua(), key)

    def cari_by_nama(self, keyword):
        """Cari produk menggunakan BST (prefix search)"""
        return self.bst.search_prefix(keyword)

    def cari_by_id(self, id_produk):
        """Cari produk menggunakan Binary Search pada array terurut"""
        semua = merge_sort(self.inventaris.get_semua(), 'id')
        idx   = binary_search(semua, id_produk)
        return semua[idx] if idx >= 0 else None

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------
    def update_produk(self, id_produk, nama=None, kategori=None,
                      stok=None, harga=None, lokasi=None):
        """Update data produk di Hash Table & BST"""
        produk = self.inventaris.get(id_produk)
        if not produk:
            return False

        # Simpan state lama ke Stack untuk undo
        self.undo_stack.push({
            'aksi'      : 'update',
            'produk_lama': dict(produk),
            'id'        : id_produk,
        })

        # Hapus key lama dari BST sebelum rename
        self.bst.delete(produk['nama'])

        if nama     is not None: produk['nama']     = nama
        if kategori is not None: produk['kategori'] = kategori
        if stok     is not None: produk['stok']     = int(stok)
        if harga    is not None: produk['harga']    = int(harga)
        if lokasi   is not None: produk['lokasi']   = lokasi

        self.inventaris.insert(id_produk, produk)
        self.bst.insert(produk['nama'], produk)
        self._catat_riwayat('UPDATE', f"Edit produk: {produk['nama']} (ID: {id_produk})")
        self._cek_stok_rendah()
        return True

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------
    def hapus_produk(self, id_produk):
        """Hapus produk dari Hash Table & BST"""
        produk = self.inventaris.get(id_produk)
        if not produk:
            return False

        self.undo_stack.push({'aksi': 'hapus', 'produk': dict(produk)})
        self.bst.delete(produk['nama'])
        self.inventaris.delete(id_produk)
        self._catat_riwayat('HAPUS', f"Hapus produk: {produk['nama']} (ID: {id_produk})")
        self._cek_stok_rendah()
        return True

    # --------------------------------------------------------
    # UNDO (Stack)
    # --------------------------------------------------------
    def undo(self):
        """Batalkan operasi terakhir menggunakan Stack"""
        op = self.undo_stack.pop()
        if not op:
            return None

        if op['aksi'] == 'tambah':
            p = op['produk']
            self.bst.delete(p['nama'])
            self.inventaris.delete(p['id'])
            self._catat_riwayat('UNDO', f"Undo tambah: {p['nama']}")

        elif op['aksi'] == 'hapus':
            p = op['produk']
            self.inventaris.insert(p['id'], p)
            self.bst.insert(p['nama'], p)
            self._catat_riwayat('UNDO', f"Undo hapus: {p['nama']}")

        elif op['aksi'] == 'update':
            p_lama = op['produk_lama']
            sekarang = self.inventaris.get(op['id'])
            if sekarang:
                self.bst.delete(sekarang['nama'])
            self.inventaris.insert(op['id'], p_lama)
            self.bst.insert(p_lama['nama'], p_lama)
            self._catat_riwayat('UNDO', f"Undo update: {p_lama['nama']}")

        self._cek_stok_rendah()
        return op['aksi']