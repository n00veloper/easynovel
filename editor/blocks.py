import cache
from dragndrop import *
import tkinter as tk

def show_menu(event, menu):
        global frame_at
        x = cache.root.winfo_x() + event.x
        y = cache.root.winfo_y() + event.y
        frame_at = [event.x,event.y]
        menu.tk_popup(x, y)

def frame_del(event, menu_del):
        cache.frame_right_click = event.widget

        global frame_at
        x = cache.frame_right_click.winfo_rootx() + event.x
        y = cache.frame_right_click.winfo_rooty() + event.y
        menu_del.tk_popup(x, y)

def delete_frame():
        delete = cache.dic_el["movable"].index(cache.frame_right_click)
        del cache.dic_el["movable"][delete]
        del cache.dic_el["ID"][delete]
        cache.frame_right_click.place_forget()

        print(cache.dic_el)

def create_frame_at():
        frame = DnDFrame(cache.root, bd=10, bg="grey")
        frame.place(x=frame_at[0], y=frame_at[1], width=200, height=300)

        # full form for history
        i_label = tk.Label(master=frame, text = "comment")
        comment = tk.Text(master=frame, height = 5, width = 10)
        i_label.grid(column=0, row=0)
        comment.grid(column=1, row=0)

        p_label = tk.Label(master=frame, text = "awnser")
        prompt = tk.Text(master=frame, height = 5, width = 10)
        p_label.grid(column=0, row=1)
        prompt.grid(column=1, row=1)

        ID_label = tk.Label(master=frame, text = "ID connection")
        ID_prompt = tk.Text(master=frame, height = 1, width = 10)
        ID_label.grid(column=0, row=2)
        ID_prompt.grid(column=1, row=2)

        OR_label = tk.Label(master=frame, text = "ID order")
        OR_prompt = tk.Text(master=frame, height = 1, width = 10)
        OR_label.grid(column=0, row=3)
        OR_prompt.grid(column=1, row=3)

        cache.dic_el["movable"].append(frame)
        cache.dic_el["ID"].append([ID_prompt, OR_prompt, frame, comment, prompt])
        canvas.connector()

        frame.bind("<Button-3>", lambda event: frame_del(event, cache.menu_del))