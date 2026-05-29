#binary_tree

class NodeTree:
    def __init__(self, teks):
        self.teks = teks
        self.Left = None
        self.Right = None

def buat_pohon_keputusan():
    root = NodeTree("Apakah jenis barang Elektronik?")
    
    root.Left = NodeTree("Apakah barang bernilai tinggi?")
    root.Left.Left = NodeTree("Rekomendasi: Taruh di Area AC / Kering")
    root.Left.Right = NodeTree("Rekomendasi: Taruh di Rak Standar Samping")
    
    root.Right = NodeTree("Apakah barang termasuk kategori rapuh?")
    root.Right.Left = NodeTree("Rekomendasi: Taruh di Rak Atas (Bebas Guncangan)")
    root.Right.Right = NodeTree("Rekomendasi: Taruh di Pallet Lantai Bawah (Berat)")
    
    return root