#sort_search

def selection_sort_barang(arr, berdasarkan="stok"):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if berdasarkan == "stok":
                if arr[j].stok < arr[min_idx].stok:
                    min_idx = j
            elif berdasarkan == "harga":
                if arr[j].harga < arr[min_idx].harga:
                    min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def linear_search_barang(arr, target_nama):
    hasil = []
    for index in range(len(arr)):
        if target_nama.lower() in arr[index].nama.lower():
            hasil.append(arr[index])
    return hasil

def binary_search_barang(arr_sorted_by_sku, target_sku):
    low = 0
    high = len(arr_sorted_by_sku) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr_sorted_by_sku[mid].sku == target_sku:
            return arr_sorted_by_sku[mid]
        elif arr_sorted_by_sku[mid].sku < target_sku:
            low = mid + 1
        else:
            high = mid - 1
    return None