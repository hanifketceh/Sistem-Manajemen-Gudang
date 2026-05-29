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
