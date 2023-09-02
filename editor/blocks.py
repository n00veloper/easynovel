import cache
from dragndrop import *
import tkinter as tk

def show_menu(event, menu):
        # used to get the menu to show in the right position
        global frame_at
        x = cache.root.winfo_x() + event.x
        y = cache.root.winfo_y() + event.y
        cache.frame_at = [event.x,event.y]
        menu.tk_popup(x, y)

def frame_del(event, menu_del):
        # show options to delete or condigure the frame.
        cache.frame_right_click = event.widget

        global frame_at
        x = cache.frame_right_click.winfo_rootx() + event.x
        y = cache.frame_right_click.winfo_rooty() + event.y
        menu_del.tk_popup(x, y)

def delete_frame():
        # delete any frame who was right clicked.

        delete = cache.dic_el["movable"].index(cache.frame_right_click)
        del cache.dic_el["movable"][delete]
        del cache.dic_el["ID"][delete]
        cache.frame_right_click.place_forget()

def create_frame_at(comment_v = False, prompt_v = False, ID_prompt_v = False, OR_prompt_v = False):
        #creates frames.
        # it uses a function call to customize the frame, from dragndrop.
        frame = DnDFrame(cache.root, bd=10, bg="grey")
        frame.place(x=cache.frame_at[0], y=cache.frame_at[1], width=200, height=300)

        # full form for history, dont need to comment much
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

        # in the case it got loaded from file
        for val in [[comment_v, comment], [prompt_v, prompt], [ID_prompt_v, ID_prompt], [OR_prompt_v, OR_prompt]]:
                if val[0]:
                        val[1].delete(1.0, "end")
                        val[1].insert("end", val[0])

        # also adds the frame to these paths, note the "frame" at the end to identify later on.
        cache.dic_el["movable"].append(frame)
        cache.dic_el["ID"].append([ID_prompt, OR_prompt, frame, comment, prompt, "frame"])
        canvas.connector()
        
        # on mouse-3 (right) click, do frame_del (show menu options)
        frame.bind("<Button-3>", lambda event: frame_del(event, cache.menu_del))