import tkinter as tk
import sys
from ui import create_main_window

def on_closing():
    sys.exit()  # Terminates the script

if __name__ == "__main__":
    root = tk.Tk()
    create_main_window(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window close event
    root.mainloop()
