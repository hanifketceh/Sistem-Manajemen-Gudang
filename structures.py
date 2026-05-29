# ============================================================
# 1. LINKED LIST - Riwayat Transaksi
# ============================================================
class NodeTransaksi:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListTransaksi:
    def __init__(self):
        self.head = None
        self.size = 0

    def tambah(self, data):
        """Tambah node baru di head — O(1)"""
        node_baru = NodeTransaksi(data)
        node_baru.next = self.head
        self.head = node_baru
        self.size += 1

    def get_semua(self):
        """Traverse dari head ke tail — O(n)"""
        hasil = []
        current = self.head
        while current:
            hasil.append(current.data)
            current = current.next
        return hasil

    def hapus_semua(self):
        self.head = None
        self.size = 0


# ============================================================
# 2. STACK (LIFO) - Undo Operasi
# ============================================================
class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        """Tambah item ke atas stack"""
        self.data.append(item)

    def pop(self):
        """Ambil & hapus item teratas"""
        if not self.is_empty():
            return self.data.pop()
        return None

    def peek(self):
        """Lihat item teratas tanpa menghapus"""
        if not self.is_empty():
            return self.data[-1]
        return None

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)


# ============================================================
# 3. QUEUE (FIFO) - Notifikasi Stok Rendah
# ============================================================
class Queue:
    def __init__(self):
        self.data = []

    def enqueue(self, item):
        """Tambah ke belakang antrian"""
        self.data.append(item)

    def dequeue(self):
        """Ambil dari depan antrian"""
        if not self.is_empty():
            return self.data.pop(0)
        return None

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def get_semua(self):
        return list(self.data)

    def hapus_semua(self):
        self.data = []


# ============================================================
# 4. BINARY SEARCH TREE - Pencarian Produk by Nama
# ============================================================
class NodeBST:
    def __init__(self, key, data):
        self.key  = key    # nama produk lowercase
        self.data = data   # dict produk
        self.left  = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        self.root = self._insert(self.root, key.lower(), data)

    def _insert(self, node, key, data):
        if node is None:
            return NodeBST(key, data)
        if key < node.key:
            node.left  = self._insert(node.left,  key, data)
        elif key > node.key:
            node.right = self._insert(node.right, key, data)
        else:
            node.data = data   # update jika sudah ada
        return node

    def search(self, key):
        return self._search(self.root, key.lower())

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.data
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def search_prefix(self, prefix):
        """Cari semua produk yang namanya mengandung prefix — inorder"""
        hasil = []
        self._inorder_search(self.root, prefix.lower(), hasil)
        return hasil

    def _inorder_search(self, node, prefix, hasil):
        if node is None:
            return
        self._inorder_search(node.left, prefix, hasil)
        if prefix in node.key:
            hasil.append(node.data)
        self._inorder_search(node.right, prefix, hasil)

    def delete(self, key):
        self.root = self._delete(self.root, key.lower())

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left  = self._delete(node.left,  key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            successor  = self._min_node(node.right)
            node.key   = successor.key
            node.data  = successor.data
            node.right = self._delete(node.right, successor.key)
        return node

    def _min_node(self, node):
        while node.left:
            node = node.left
        return node

    def inorder(self):
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, node, hasil):
        if node:
            self._inorder(node.left, hasil)
            hasil.append(node.data)
            self._inorder(node.right, hasil)

    def rebuild(self, semua_produk):
        """Rebuild seluruh BST dari list produk"""
        self.root = None
        for p in semua_produk:
            self.insert(p['nama'], p)


# ============================================================
# 5. HASH TABLE - Penyimpanan Utama Inventaris
#    Menggunakan Separate Chaining untuk collision handling
# ============================================================
class HashTableInventaris:
    def __init__(self, kapasitas=100):
        self.kapasitas   = kapasitas
        self.table       = [[] for _ in range(kapasitas)]
        self.jumlah_item = 0

    def _hash(self, key):
        """Hash function: sum of ASCII * position"""
        total = 0
        for i, ch in enumerate(str(key)):
            total += ord(ch) * (i + 1)
        return total % self.kapasitas

    def insert(self, key, value):
        idx    = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)   # update
                return
        bucket.append((key, value))
        self.jumlah_item += 1

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx    = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.jumlah_item -= 1
                return True
        return False

    def get_semua(self):
        hasil = []
        for bucket in self.table:
            for k, v in bucket:
                hasil.append(v)
        return hasil

    def exists(self, key):
        return self.get(key) is not None


# ============================================================
# 6. MERGE SORT - Mengurutkan List Produk
# ============================================================
def merge_sort(arr, key='nama'):
    if len(arr) <= 1:
        return arr
    mid   = len(arr) // 2
    kiri  = merge_sort(arr[:mid],  key)
    kanan = merge_sort(arr[mid:], key)
    return _merge(kiri, kanan, key)


def _merge(kiri, kanan, key):
    hasil = []
    i = j = 0
    while i < len(kiri) and j < len(kanan):
        vk = kiri[i][key]
        vn = kanan[j][key]
        if isinstance(vk, str):
            vk, vn = vk.lower(), vn.lower()
        if vk <= vn:
            hasil.append(kiri[i]);  i += 1
        else:
            hasil.append(kanan[j]); j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil


# ============================================================
# 7. BINARY SEARCH - Pencarian Cepat berdasarkan ID
# ============================================================
def binary_search(arr, target_id):
    """Cari produk di array yang sudah diurutkan by ID — O(log n)"""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid]['id'] == target_id:
            return mid
        elif arr[mid]['id'] < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return -1