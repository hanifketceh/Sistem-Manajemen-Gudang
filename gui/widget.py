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
