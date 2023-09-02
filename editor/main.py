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

    # menu when clicking on the root window, it has a few commands who prompt on the screen. 
    menu = tix.Menu(cache.root)
    menu.add_command(label="Add frame", command=blocks.create_frame_at)
    menu.add_separator()
    menu.add_command(label="Save", command=lambda: save.saveHistory(cache.dic_el))
    menu.add_separator()
    menu.add_command(label="Load", command=lambda: save.loadHistory(cache.dic_el, cache.root))

    # manu del is cached because it is used globally, but is set here, used for frame manipulation on right click (mouse-3)
    cache.menu_del = tix.Menu(cache.root)
    cache.menu_del.add_command(label="Remove frame", command=blocks.delete_frame)

    # canvas is a fake "root window" so it does not open two menu on right click.
    cache.canvas.bind("<Button-3>", lambda event: blocks.show_menu(event, menu))

    cache.root.mainloop()

if __name__ == "__main__":
    main_window()