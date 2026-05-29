def _build_tab_inventaris(self, parent):
    # Toolbar
    toolbar = tk.Frame(parent, bg=self.BG_DARK, pady=8)
    toolbar.pack(fill='x', padx=10)

    self._label(toolbar, "Cari:", bg=self.BG_DARK).pack(side='left', padx=(0, 4))
    self.var_cari = tk.StringVar()
    self.var_cari.trace('w', lambda *a: self._refresh_tabel())
    self._entry(toolbar, self.var_cari, width=25).pack(side='left', padx=(0, 10))

    self._label(toolbar, "Urut:", bg=self.BG_DARK).pack(side='left', padx=(0, 4))
    self.var_sort = tk.StringVar(value='Nama')
    combo = ttk.Combobox(toolbar, textvariable=self.var_sort,
        values=['Nama', 'ID', 'Kategori', 'Stok', 'Harga'],
        width=10, state='readonly', font=('Courier New', 9))
    combo.pack(side='left')
    combo.bind('<<ComboboxSelected>>', lambda e: self._refresh_tabel())

    self._btn(toolbar, "↑ ASC",  lambda: self._set_sort(True),  width=7).pack(side='left', padx=2)
    self._btn(toolbar, "↓ DESC", lambda: self._set_sort(False), color='#6B8CFF', width=7).pack(side='left', padx=2)

    # Stat bar
    stat = tk.Frame(parent, bg=self.BG_PANEL, pady=4)
    stat.pack(fill='x', padx=10)
    self.lbl_stat = tk.Label(stat, text="",
        bg=self.BG_PANEL, fg=self.TEXT_MUTED,
        font=('Courier New', 9))
    self.lbl_stat.pack(side='left', padx=8)

    # Tabel
    frame_tabel = tk.Frame(parent, bg=self.BG_DARK)
    frame_tabel.pack(fill='both', expand=True, padx=10, pady=4)

    cols   = ('ID', 'Nama', 'Kategori', 'Stok', 'Harga', 'Lokasi')
    widths = {'ID': 90, 'Nama': 240, 'Kategori': 110,
                  'Stok': 65, 'Harga': 120, 'Lokasi': 90}

    self.tabel = ttk.Treeview(frame_tabel, columns=cols,
        show='headings', style='Inventory.Treeview', selectmode='browse')
    for c in cols:
        self.tabel.heading(c, text=c,
            command=lambda col=c: self._sort_by_col(col))
        anchor = 'w' if c in ('Nama',) else 'center'
        self.tabel.column(c, width=widths[c], anchor=anchor)

    sb = ttk.Scrollbar(frame_tabel, orient='vertical',
        command=self.tabel.yview, style='Dark.Vertical.TScrollbar')
    self.tabel.configure(yscrollcommand=sb.set)
    sb.pack(side='right', fill='y')
    self.tabel.pack(fill='both', expand=True)
    self.tabel.tag_configure('low_stock', foreground=self.DANGER)
    self.tabel.tag_configure('ok', foreground=self.TEXT_PRIMARY)

    # Action bar
    act = tk.Frame(parent, bg=self.BG_DARK, pady=6)
    act.pack(fill='x', padx=10)
    self._btn(act, "✏ Edit",    self._edit_selected,   color='#6B8CFF').pack(side='left', padx=3)
    self._btn(act, "🗑 Hapus",  self._hapus_selected,  color=self.DANGER).pack(side='left', padx=3)
    self._btn(act, "⟲ Undo",   self._undo,            color='#8B92A5').pack(side='left', padx=3)
    self._btn(act, "🔄 Refresh",self._refresh_tabel).pack(side='left', padx=3)
    self._btn(act, "📋 Detail", self._detail_selected, color=self.ACCENT2).pack(side='left', padx=3)
