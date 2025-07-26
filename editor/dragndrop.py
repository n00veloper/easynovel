import tkinter as tk
import cache
import canvas

def make_all_draggable(widget):
    # same as make_draggable, but for scrolling the whole screen
    widget.bind("<Button-2>", on_drag_start)
    widget.bind("<B2-Motion>", drag_all)

def drag_all(event):
    # drag everything to the opposite direction, like if the background was scrolled somewhere else.
    # note the cache.sensibility, it can be changed for better or worst controll
    widget = event.widget
    x = (widget._drag_start_x - event.x)
    y = (widget._drag_start_y - event.y)
    for item in cache.dic_el["movable"]:
        item.place(x=item.winfo_x()-x, y=item.winfo_y()-y)
    on_drag_start(event)
    canvas.connector()

def make_draggable(widget):
    # get every drag event on track
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    # on start of drag, get event position, so it goes smoother.
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    # do a drag and drop movment on a early on called event
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)
    canvas.connector()

class DragDropMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        make_draggable(self)

class DragDropMixinRoot:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        make_all_draggable(self)

# As always when it comes to mixins, make sure to
# inherit from DragDropMixin FIRST!
class DnDFrame(DragDropMixin, tk.Frame):
    pass

class DnDRoot(DragDropMixinRoot, tk.Tk):
    pass

# This wouldn't work:
# class DnDFrame(tk.Frame, DragDropMixin):
#     pass