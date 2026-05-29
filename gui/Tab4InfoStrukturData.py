def _build_tab_info(self, parent):
        tk.Label(parent, text="🧮 STRUKTUR DATA YANG DIGUNAKAN",
            bg=self.BG_PANEL, fg=self.ACCENT,
            font=('Courier New', 13, 'bold')).pack(pady=(16, 12))

        info_list = [
            ("1. Hash Table",        "Penyimpanan utama inventaris.\nAkses O(1) dengan separate chaining untuk collision."),
            ("2. Linked List",       "Menyimpan riwayat transaksi.\nNode baru selalu ditambah di head — O(1)."),
            ("3. Stack (LIFO)",      "Operasi Undo.\nSetiap aksi di-push, undo men-pop operasi terakhir."),
            ("4. Queue (FIFO)",      "Notifikasi stok rendah.\nProduk dengan stok ≤ 10 masuk antrian notifikasi."),
            ("5. Binary Search Tree","Pencarian produk berdasarkan nama.\nSupport prefix search & inorder traversal."),
            ("6. Merge Sort",        "Mengurutkan daftar produk berdasarkan kolom.\nTime complexity O(n log n)."),
            ("7. Binary Search",     "Pencarian produk berdasarkan ID.\nBekerja pada array terurut — O(log n)."),
        ]

        canvas = tk.Canvas(parent, bg=self.BG_PANEL, highlightthickness=0)
        scroll = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        canvas.pack(fill='both', expand=True, padx=20)

        inner = tk.Frame(canvas, bg=self.BG_PANEL)
        canvas.create_window((0, 0), window=inner, anchor='nw')

        for judul, deskripsi in info_list:
            card = tk.Frame(inner, bg=self.BG_CARD,
                highlightthickness=1, highlightbackground=self.BORDER)
            card.pack(fill='x', pady=5, padx=4)
            tk.Label(card, text=judul, bg=self.BG_CARD, fg=self.ACCENT,
                font=('Courier New', 10, 'bold')).pack(anchor='w', padx=14, pady=(8, 2))
            tk.Label(card, text=deskripsi, bg=self.BG_CARD, fg=self.TEXT_MUTED,
                font=('Courier New', 9), justify='left').pack(anchor='w', padx=14, pady=(0, 8))

        inner.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
