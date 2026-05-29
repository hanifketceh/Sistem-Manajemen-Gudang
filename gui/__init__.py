def __init__(self, root):
  self.root = root
  self.sistem = SistemInventaris()
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
