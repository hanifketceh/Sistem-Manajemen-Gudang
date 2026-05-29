def _build_tab_form(self, parent):
    self.edit_id = None

    wrapper = tk.Frame(parent, bg=self.BG_PANEL)
    wrapper.pack(expand=True, fill='both')

    card = tk.Frame(wrapper, bg=self.BG_CARD,
        highlightthickness=1, highlightbackground=self.BORDER)
    card.place(relx=0.5, rely=0.5, anchor='center', width=520, height=460)

    self.lbl_form_title = tk.Label(card, text="➕  TAMBAH PRODUK BARU",
        bg=self.BG_CARD, fg=self.ACCENT,
        font=('Courier New', 14, 'bold'))
    self.lbl_form_title.pack(pady=(20, 16))

    fields = tk.Frame(card, bg=self.BG_CARD)
    fields.pack(padx=30, fill='x')

    self.form_vars = {}
    field_list = [
        ("Nama Produk *",  'nama',     False),
        ("Kategori *",     'kategori', True),
        ("Stok *",         'stok',     False),
        ("Harga (Rp) *",   'harga',    False),
        ("Lokasi Rak *",   'lokasi',   False),
    ]
    for lbl_text, key, is_combo in field_list:
        row = tk.Frame(fields, bg=self.BG_CARD)
        row.pack(fill='x', pady=4)
        tk.Label(row, text=lbl_text, bg=self.BG_CARD,
            fg=self.TEXT_MUTED, font=('Courier New', 9),
            width=16, anchor='w').pack(side='left')
        var = tk.StringVar()
        if is_combo:
            cb = ttk.Combobox(row, textvariable=var,
                values=['Elektronik','Aksesoris','Kabel',
                        'Storage','Komponen','Furnitur','Lainnya'],
                width=26, font=('Courier New', 10))
            cb.pack(side='left', fill='x', expand=True)
        else:
            self._entry(row, var).pack(side='left', fill='x', expand=True)
        self.form_vars[key] = var

    btn_frame = tk.Frame(card, bg=self.BG_CARD)
    btn_frame.pack(pady=20)
    self.btn_simpan = self._btn(btn_frame, "💾 SIMPAN", self._simpan_form, width=14)
    self.btn_simpan.pack(side='left', padx=6)
    self._btn(btn_frame, "🔄 RESET", self._reset_form,
        color='#6B8CFF', width=10).pack(side='left', padx=6)

    self.lbl_form_status = tk.Label(card, text="",
        bg=self.BG_CARD, fg=self.ACCENT2,
        font=('Courier New', 9))
    self.lbl_form_status.pack()
