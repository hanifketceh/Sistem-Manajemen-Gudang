def _build_ui(self):
    #Header
    header = tk.Frame(self.root, bg=self.BG_DARK, pady=12)
    header.pack(fill='x', padx=20)

    tk.Label(header, text="📦 SISTEM INVENTARIS GUDANG",
        bg=self.BG_DARK, fg=self.ACCENT,
        font=('Courier New', 20, 'bold')).pack(side='left')
    tk.Label(header, text="  |  Algoritma & Struktur Data  —  UAP",
        bg=self.BG_DARK, fg=self.TEXT_MUTED,
        font=('Courier New', 10)).pack(side='left', pady=6)
    
    #Badge Notifikasi
    self.lbl_notif = tk.Label(header, text="",
        bg=self.DANGER, fg='white',
        font=('Courier New', 9, 'bold'),
        padx=8, pady=3, cursor='hand2')
    self.lbl_notif.pack(side='right', padx=4)
    self.lbl_notif.bind('<Button-1>', lambda e: self._show_notifikasi())

    #Notebook
    self.nb = ttk.Notebook(self.root, style='Dark.TNotebook')
    self.nb.pack(fill='both', expand=True, padx=20, pady=(0, 10))

    tab1 = tk.Frame(self.nb, bg=self.BG_DARK)
    self.nb.add(tab1, text='  📋 Inventaris  ')
    self._build_tab_inventaris(tab1)

    tab2 = tk.Frame(self.nb, bg=self.BG_PANEL)
    self.nb.add(tab2, text='  ➕ Tambah / Edit  ')
    self._build_tab_form(tab2)

    tab3 = tk.Frame(self.nb, bg=self.BG_PANEL)
    self.nb.add(tab3, text='  📜 Riwayat  ')
    self._build_tab_riwayat(tab3)

    tab4 = tk.Frame(self.nb, bg=self.BG_PANEL)
    self.nb.add(tab4, text='  🧮 Struktur Data  ')
    self._build_tab_info(tab4)
