def _build_tab_riwayat(self, parent):
        tk.Label(parent, text="📜 RIWAYAT TRANSAKSI  (Linked List)",
            bg=self.BG_PANEL, fg=self.ACCENT,
            font=('Courier New', 12, 'bold')).pack(pady=(16, 8))

        frame = tk.Frame(parent, bg=self.BG_PANEL)
        frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))

        cols = ('Waktu', 'Aksi', 'Detail')
        self.tbl_riwayat = ttk.Treeview(frame, columns=cols,
            show='headings', style='Inventory.Treeview', height=18)
        self.tbl_riwayat.heading('Waktu',  text='Waktu')
        self.tbl_riwayat.heading('Aksi',   text='Aksi')
        self.tbl_riwayat.heading('Detail', text='Detail')
        self.tbl_riwayat.column('Waktu',  width=130, anchor='center')
        self.tbl_riwayat.column('Aksi',   width=80,  anchor='center')
        self.tbl_riwayat.column('Detail', width=500)

        sb = ttk.Scrollbar(frame, orient='vertical',
            command=self.tbl_riwayat.yview,
            style='Dark.Vertical.TScrollbar')
        self.tbl_riwayat.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        self.tbl_riwayat.pack(fill='both', expand=True)

        self.tbl_riwayat.tag_configure('TAMBAH', foreground=self.ACCENT2)
        self.tbl_riwayat.tag_configure('HAPUS',  foreground=self.DANGER)
        self.tbl_riwayat.tag_configure('UPDATE', foreground='#6B8CFF')
        self.tbl_riwayat.tag_configure('UNDO',   foreground=self.ACCENT)

        act = tk.Frame(parent, bg=self.BG_PANEL, pady=4)
        act.pack()
        self._btn(act, "🔄 Refresh", self._refresh_riwayat).pack(side='left', padx=4)
        self._btn(act, "🗑 Hapus Riwayat",
            lambda: (self.sistem.riwayat.hapus_semua(), self._refresh_riwayat()),
            color=self.DANGER, width=16).pack(side='left', padx=4)
