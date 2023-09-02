import cache
import tkinter as tk

def connector():
    i = 0
    # delete old arrows
    cache.canvas.delete("all")

    # make shortest path for arrow by ID
    tmp_list = []
    for item in cache.dic_el["ID"]:
        v1 = item[0].get("1.0",'end-1c')
        v2 = item[1].get("1.0",'end-1c')
        if v1 == "":
            v1 = 1
        if v2 == "":
            v2 = 1
        
        tmp_list.append([int(v1), int(v2), item[2]])

    tmp_list.sort(key = lambda row: (row[1]))

    # add arrows from tmp_list order.
    dic_keys = {}
    for equal in tmp_list:
        for item in tmp_list:
            if equal[0] == item[0]:
                if not equal[0] in dic_keys.keys():
                    dic_keys[equal[0]] = equal
                elif dic_keys[equal[0]][1] <= item[1]:
                    cache.canvas.create_line(dic_keys[equal[0]][2].winfo_x(), dic_keys[equal[0]][2].winfo_y(), item[2].winfo_x(), item[2].winfo_y(), arrow=tk.LAST)
                    dic_keys[equal[0]] = item
    