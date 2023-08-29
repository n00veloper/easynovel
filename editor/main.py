import tkinter as tk
import tkinter.tix as tix
import save
from dragndrop import *
import cache
import canvas
import blocks

def main_window():
    cache.root = DnDRoot()
    cache.canvas = tk.Canvas(cache.root)
    cache.canvas.pack(fill="both", expand=True)

    menu = tix.Menu(cache.root)
    menu.add_command(label="Add frame", command=blocks.create_frame_at)
    menu.add_separator()
    menu.add_command(label="Save", command=lambda: save.saveHistory(cache.dic_el))
    menu.add_separator()
    menu.add_command(label="Load", command=lambda: save.loadHistory(cache.dic_el, cache.root))

    cache.menu_del = tix.Menu(cache.root)
    cache.menu_del.add_command(label="Remove frame", command=blocks.delete_frame)

    cache.canvas.bind("<Button-3>", lambda event: blocks.show_menu(event, menu))
    #root.bind("<B2-Motion>", lambda event: drag_all(event, dic_el, root))

    cache.root.mainloop()

if __name__ == "__main__":
    main_window()