import tkinter as tk
from gui import GUIInventaris


def main():
    root = tk.Tk()
    app  = GUIInventaris(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
