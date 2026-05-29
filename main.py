# main.py

from structures.models import BarangElektronik, BarangPecahBelah
from structures.bst import insert_bst, inorder_traversal_barang
from structures.stack_queue import Stack, Queue
from structures.linked_list import DoublyLinkedList
from structures.sort_search import selection_sort_barang, linear_search_barang, binary_search_barang
from structures.binary_tree import buat_pohon_keputusan

class AppController:
    def __init__(self):
        self.master_list = []  
        self.bst_root = None    
        self.undo_stack = Stack()
        self.truk_queue = Queue()
        self.log_list = DoublyLinkedList()
        self.decision_tree = buat_pohon_keputusan()

    def tambah_atau_update_barang(self, kategori, sku, nama, stok, harga, atribut_unik):
        if kategori == "Elektronik":
            baru = BarangElektronik(sku, nama, int(stok), int(harga), atribut_unik)
        else:
            baru = BarangPecahBelah(sku, nama, int(stok), int(harga), atribut_unik)
        
        existing = [b for b in self.master_list if b.sku == sku]
        if existing:
            self.master_list.remove(existing[0])
            self.log_list.insertAtEnd(f"UPDATE: Barang {sku} diperbarui.")
        else:
            self.log_list.insertAtEnd(f"CREATE: Barang {sku} ditambahkan.")
            
        self.master_list.append(baru)
        self.undo_stack.push(("TAMBAH", baru))
        self.rebuild_bst()

    def dapatkan_semua_barang(self):
        hasil_terurut = []
        inorder_traversal_barang(self.bst_root, hasil_terurut)
        return hasil_terurut

    def hapus_barang(self, sku):
        target = [b for b in self.master_list if b.sku == sku]
        if target:
            self.master_list.remove(target[0])
            self.undo_stack.push(("HAPUS", target[0]))
            self.log_list.insertAtEnd(f"DELETE: Barang {sku} dihapus.")
            self.rebuild_bst()
            return True
        return False

    def rebuild_bst(self):
        self.bst_root = None
        for b in self.master_list:
            self.bst_root = insert_bst(self.bst_root, b)

    def urutkan_barang(self, berdasarkan="stok"):
        daftar = list(self.master_list)
        selection_sort_barang(daftar, berdasarkan)
        return daftar

if __name__ == "__main__":
    app = AppController()
    
    app.tambah_atau_update_barang("Elektronik", "BRG01", "Laptop Hore", 10, 5000000, "12")
    app.tambah_atau_update_barang("Pecah Belah", "BRG02", "Gelas Kaca", 50, 15000, "Bubble Wrap")
    
    print("=== HASIL DATA MASUK ===")
    for b in app.dapatkan_semua_barang():
        print(b.info())
        
    print("\n=== LOG RIWAYAT ===")
    for log in app.log_list.get_all_logs():
        print(log)
import tkinter as tk
from gui import GUIInventaris


def main():
    root = tk.Tk()
    app  = GUIInventaris(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()

