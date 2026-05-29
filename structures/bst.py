#bst

class NodeBST:
    def __init__(self, barang):
        self.barang = barang
        self.left = None
        self.right = None

def insert_bst(root, barang):
    if root is None:
        return NodeBST(barang)
    if root.barang.sku == barang.sku:
        root.barang = barang 
        return root
    elif barang.sku < root.barang.sku:
        root.left = insert_bst(root.left, barang)
    else:
        root.right = insert_bst(root.right, barang)
    return root

def inorder_traversal_barang(root, hasil_list):
    if root is not None:
        inorder_traversal_barang(root.left, hasil_list)
        hasil_list.append(root.barang)
        inorder_traversal_barang(root.right, hasil_list)