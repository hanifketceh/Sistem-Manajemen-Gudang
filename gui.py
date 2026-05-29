"""
========================================
gui.py
Berisi semua kelas tampilan (Tkinter).
Menyimpan Windows, Frames, dan widget.

Kelas utama: GUIInventaris
  - Tab Inventaris  (tabel + toolbar)
  - Tab Tambah/Edit (form input)
  - Tab Riwayat     (linked list view)
  - Tab Struktur Data (info edukasi)
========================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

from logic import SistemInventaris
from structures import merge_sort


class GUIInventaris:
    # ── Palet warna Industrial / Warehouse ──────────────────
    BG_DARK      = '#1A1D23'
    BG_PANEL     = '#242830'
    BG_CARD      = '#2E333D'
    ACCENT       = '#F5A623'
    ACCENT2      = '#4CAF82'
    DANGER       = '#E05C5C'
    TEXT_PRIMARY = '#F0F2F5'
    TEXT_MUTED   = '#8B92A5'
    BORDER       = '#363C4A'

    def __init__(self, root):
        self.root     = root
        self.sistem   = SistemInventaris()
        self.sort_key = 'nama'
        self.sort_asc = True

        self.root.title("📦 Sistem Inventaris Gudang")
        self.root.geometry("1280x780")
        self.root.configure(bg=self.BG_DARK)
        self.root.resizable(True, True)

        self._setup_style()
        self._build_ui()
        self._refresh_tabel()
        self._update_badge_notif()

    # ── Style ────────────────────────────────────────────────
    def _setup_style(self):
        s = ttk.Style()
        s.theme_use('clam')

        s.configure('Inventory.Treeview',
            background=self.BG_CARD, foreground=self.TEXT_PRIMARY,
            fieldbackground=self.BG_CARD, rowheight=30,
            font=('Courier New', 9))
        s.configure('Inventory.Treeview.Heading',
            background=self.BG_PANEL, foreground=self.ACCENT,
            font=('Courier New', 9, 'bold'), relief='flat')
        s.map('Inventory.Treeview',
            background=[('selected', '#3A4055')],
            foreground=[('selected', self.ACCENT)])

        s.configure('Dark.TNotebook', background=self.BG_DARK)
        s.configure('Dark.TNotebook.Tab',
            background=self.BG_PANEL, foreground=self.TEXT_MUTED,
            font=('Courier New', 9, 'bold'), padding=[12, 6])
        s.map('Dark.TNotebook.Tab',
            background=[('selected', self.BG_CARD)],
            foreground=[('selected', self.ACCENT)])

        s.configure('Dark.Vertical.TScrollbar',
            background=self.BG_PANEL, troughcolor=self.BG_DARK,
            arrowcolor=self.TEXT_MUTED)

    # ── Widget helpers ───────────────────────────────────────
    def _btn(self, parent, text, cmd, color=None, width=12):
        c = color or self.ACCENT
        return tk.Button(parent, text=text, command=cmd,
            bg=c, fg=self.BG_DARK, font=('Courier New', 9, 'bold'),
            relief='flat', cursor='hand2', width=width,
            activebackground=self.TEXT_PRIMARY,
            activeforeground=self.BG_DARK,
            padx=8, pady=5)

    def _entry(self, parent, textvariable=None, width=28):
        return tk.Entry(parent, textvariable=textvariable,
            bg=self.BG_CARD, fg=self.TEXT_PRIMARY,
            insertbackground=self.TEXT_PRIMARY,
            font=('Courier New', 10), relief='flat',
            bd=0, highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.ACCENT,
            width=width)

    def _label(self, parent, text, bold=False, muted=False, color=None, bg=None):
        c  = color or (self.TEXT_MUTED if muted else self.TEXT_PRIMARY)
        f  = ('Courier New', 9, 'bold') if bold else ('Courier New', 9)
        bg = bg or self.BG_PANEL
        return tk.Label(parent, text=text, bg=bg, fg=c, font=f)

    # ── Build UI ─────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self.root, bg=self.BG_DARK, pady=12)
        header.pack(fill='x', padx=20)

        tk.Label(header, text="📦 SISTEM INVENTARIS GUDANG",
            bg=self.BG_DARK, fg=self.ACCENT,
            font=('Courier New', 20, 'bold')).pack(side='left')
        tk.Label(header, text="  |  Algoritma & Struktur Data  —  UAP",
            bg=self.BG_DARK, fg=self.TEXT_MUTED,
            font=('Courier New', 10)).pack(side='left', pady=6)

        # Badge notifikasi
        self.lbl_notif = tk.Label(header, text="",
            bg=self.DANGER, fg='white',
            font=('Courier New', 9, 'bold'),
            padx=8, pady=3, cursor='hand2')
        self.lbl_notif.pack(side='right', padx=4)
        self.lbl_notif.bind('<Button-1>', lambda e: self._show_notifikasi())

        # ── Notebook (tabs) ──
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

    # ── Tab 1: Inventaris ────────────────────────────────────
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
        self.tabel.tag_configure('ok',        foreground=self.TEXT_PRIMARY)

        # Action bar
        act = tk.Frame(parent, bg=self.BG_DARK, pady=6)
        act.pack(fill='x', padx=10)
        self._btn(act, "✏ Edit",    self._edit_selected,   color='#6B8CFF').pack(side='left', padx=3)
        self._btn(act, "🗑 Hapus",  self._hapus_selected,  color=self.DANGER).pack(side='left', padx=3)
        self._btn(act, "⟲ Undo",   self._undo,            color='#8B92A5').pack(side='left', padx=3)
        self._btn(act, "🔄 Refresh",self._refresh_tabel).pack(side='left', padx=3)
        self._btn(act, "📋 Detail", self._detail_selected, color=self.ACCENT2).pack(side='left', padx=3)

    # ── Tab 2: Form Tambah/Edit ──────────────────────────────
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

    # ── Tab 3: Riwayat ───────────────────────────────────────
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

    # ── Tab 4: Info Struktur Data ────────────────────────────
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

    # ── Actions ──────────────────────────────────────────────
    def _refresh_tabel(self, *args):
        keyword  = self.var_cari.get().strip()
        sort_map = {'Nama': 'nama', 'ID': 'id', 'Kategori': 'kategori',
                    'Stok': 'stok', 'Harga': 'harga'}
        self.sort_key = sort_map.get(self.var_sort.get(), 'nama')

        data = (self.sistem.cari_by_nama(keyword)
                if keyword else self.sistem.get_semua_terurut(self.sort_key))
        if keyword:
            data = merge_sort(data, self.sort_key)
        if not self.sort_asc:
            data = data[::-1]

        for row in self.tabel.get_children():
            self.tabel.delete(row)

        total_nilai = 0
        for p in data:
            tag = 'low_stock' if p['stok'] <= self.sistem.BATAS_STOK_RENDAH else 'ok'
            self.tabel.insert('', 'end', values=(
                p['id'], p['nama'], p['kategori'],
                p['stok'], f"Rp {p['harga']:,}", p['lokasi']
            ), tags=(tag,))
            total_nilai += p['stok'] * p['harga']

        self.lbl_stat.config(
            text=f"Total produk: {len(data)}  |  Nilai inventaris: Rp {total_nilai:,}")
        self._update_badge_notif()

    def _update_badge_notif(self):
        n = self.sistem.notifikasi_queue.size()
        if n > 0:
            self.lbl_notif.config(text=f"⚠ {n} Stok Rendah", bg=self.DANGER)
        else:
            self.lbl_notif.config(text="✓ Stok Aman", bg=self.ACCENT2)

    def _show_notifikasi(self):
        notifs = self.sistem.notifikasi_queue.get_semua()
        if not notifs:
            messagebox.showinfo("Notifikasi", "✓ Semua stok dalam kondisi aman!")
        else:
            pesan = "PERINGATAN STOK RENDAH (≤10 unit):\n\n" + "\n".join(notifs)
            messagebox.showwarning("⚠ Stok Rendah", pesan)

    def _get_selected_id(self):
        sel = self.tabel.selection()
        if not sel:
            messagebox.showwarning("Pilih Dulu",
                "Pilih produk dari tabel terlebih dahulu!")
            return None
        return self.tabel.item(sel[0])['values'][0]

    def _detail_selected(self):
        id_p = self._get_selected_id()
        if not id_p:
            return
        p = self.sistem.baca_produk(id_p)
        if not p:
            return
        messagebox.showinfo(f"Detail — {p['nama']}",
            f"ID          : {p['id']}\n"
            f"Nama        : {p['nama']}\n"
            f"Kategori    : {p['kategori']}\n"
            f"Stok        : {p['stok']} unit\n"
            f"Harga       : Rp {p['harga']:,}\n"
            f"Lokasi Rak  : {p['lokasi']}\n"
            f"Nilai Stok  : Rp {p['stok'] * p['harga']:,}")

    def _edit_selected(self):
        id_p = self._get_selected_id()
        if not id_p:
            return
        p = self.sistem.baca_produk(id_p)
        if not p:
            return
        self.edit_id = id_p
        self.form_vars['nama'].set(p['nama'])
        self.form_vars['kategori'].set(p['kategori'])
        self.form_vars['stok'].set(str(p['stok']))
        self.form_vars['harga'].set(str(p['harga']))
        self.form_vars['lokasi'].set(p['lokasi'])
        self.lbl_form_title.config(text=f"✏  EDIT PRODUK — {id_p}")
        self.btn_simpan.config(text="💾 UPDATE")
        self.lbl_form_status.config(
            text="Mode edit aktif. Ubah data lalu klik UPDATE.",
            fg=self.ACCENT)
        self.nb.select(1)   # pindah ke tab form

    def _hapus_selected(self):
        id_p = self._get_selected_id()
        if not id_p:
            return
        p = self.sistem.baca_produk(id_p)
        if messagebox.askyesno("Konfirmasi Hapus",
            f"Yakin hapus produk:\n{p['nama']} ({id_p})?\n\nOperasi ini bisa di-undo."):
            self.sistem.hapus_produk(id_p)
            self._refresh_tabel()
            self._refresh_riwayat()
            messagebox.showinfo("Berhasil",
                f"Produk '{p['nama']}' berhasil dihapus.\nGunakan Undo untuk membatalkan.")

    def _simpan_form(self):
        nama      = self.form_vars['nama'].get().strip()
        kategori  = self.form_vars['kategori'].get().strip()
        stok_str  = self.form_vars['stok'].get().strip()
        harga_str = self.form_vars['harga'].get().strip()
        lokasi    = self.form_vars['lokasi'].get().strip()

        if not all([nama, kategori, stok_str, harga_str, lokasi]):
            self.lbl_form_status.config(
                text="⚠ Semua field wajib diisi!", fg=self.DANGER)
            return
        try:
            stok  = int(stok_str)
            harga = int(harga_str)
            if stok < 0 or harga < 0:
                raise ValueError
        except ValueError:
            self.lbl_form_status.config(
                text="⚠ Stok & Harga harus angka positif!", fg=self.DANGER)
            return

        if self.edit_id:
            self.sistem.update_produk(self.edit_id, nama, kategori, stok, harga, lokasi)
            self.lbl_form_status.config(
                text=f"✓ Produk '{nama}' berhasil diupdate!", fg=self.ACCENT2)
        else:
            id_baru = self.sistem.tambah_produk(nama, kategori, stok, harga, lokasi)
            self.lbl_form_status.config(
                text=f"✓ Produk '{nama}' ditambah (ID: {id_baru})", fg=self.ACCENT2)

        self._reset_form()
        self._refresh_tabel()
        self._refresh_riwayat()

    def _reset_form(self):
        for v in self.form_vars.values():
            v.set('')
        self.edit_id = None
        self.lbl_form_title.config(text="➕  TAMBAH PRODUK BARU")
        self.btn_simpan.config(text="💾 SIMPAN")
        self.lbl_form_status.config(text="")

    def _undo(self):
        aksi = self.sistem.undo()
        if aksi:
            self._refresh_tabel()
            self._refresh_riwayat()
            messagebox.showinfo("Undo Berhasil",
                f"Operasi '{aksi}' berhasil dibatalkan!")
        else:
            messagebox.showinfo("Undo", "Tidak ada operasi yang bisa di-undo.")

    def _refresh_riwayat(self):
        for row in self.tbl_riwayat.get_children():
            self.tbl_riwayat.delete(row)
        for r in self.sistem.riwayat.get_semua():
            self.tbl_riwayat.insert('', 'end',
                values=(r['waktu'], r['aksi'], r['detail']),
                tags=(r['aksi'],))

    def _sort_by_col(self, col):
        map_col = {'ID': 'id', 'Nama': 'nama', 'Kategori': 'kategori',
                   'Stok': 'stok', 'Harga': 'harga', 'Lokasi': 'lokasi'}
        key = map_col.get(col, 'nama')
        if self.sort_key == key:
            self.sort_asc = not self.sort_asc
        else:
            self.sort_key = key
            self.sort_asc = True
        self.var_sort.set(col)
        self._refresh_tabel()

    def _set_sort(self, asc):
        self.sort_asc = asc
        self._refresh_tabel()