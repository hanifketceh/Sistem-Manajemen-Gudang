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
