import tempfile as tmp
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import os
import json
import blocks
import cache
import copy

def loadHistory(history, root):
    # will ask to open a .ezn file (eazynovel)
    filetypes = (
        ('easynovel files', '*.ezn'),
        ('All files', '*.*')
    )
    selectedFile = fd.askopenfilename(title="load your file", initialdir="./", filetypes=filetypes)

    # check file...
    if os.path.isfile(selectedFile):
        
        # read temp folder
        with open(selectedFile,"r", encoding="UTF-8") as file:
            
            # remove everything already in
            while len(history["movable"]) > 0:
                cache.frame_right_click = history["movable"][0]
                blocks.delete_frame()
            
            # load save
            history = json.loads(file.readlines()[0])

            # add widgets like it should.
            for widget in history["load"]:
                if widget["type"] == "frame":
                    cache.frame_at = widget["pos"]
                    blocks.create_frame_at(widget["args"][0], widget["args"][1] , widget["args"][2], widget["args"][3])


def saveHistory(history):
    # will ask to save a .ezn file (eazynovel)
    filetypes = (
        ('easynovel files', '*.ezn'),
        ('All files', '*.*')
    )
    selectedFile = fd.asksaveasfilename(title="save your file", initialdir="./", filetypes=filetypes)
    
    #if does not have extension
    if not "." in selectedFile:
        selectedFile += ".ezn"
    
    # convert var to dictionary
    tmporarydic = {"load": [], "ID": copy.copy(history["ID"])}
    while len(tmporarydic["ID"]) > 0:
        # if is block id add root first, then...
        if tmporarydic["ID"][0][-1] == "frame":
            tmporarydic["load"].append({
                                "type": "frame",
                                "pos": [tmporarydic["ID"][0][2].winfo_rootx(), tmporarydic["ID"][0][2].winfo_rooty()],
                                "args": [tmporarydic["ID"][0][3].get("1.0",'end-1c'), tmporarydic["ID"][0][4].get("1.0",'end-1c'), tmporarydic["ID"][0][0].get("1.0",'end-1c'), tmporarydic["ID"][0][1].get("1.0",'end-1c')]
                               })
        del tmporarydic["ID"][0]
    del tmporarydic["ID"]

    # if file exists, overwrite
    if os.path.isfile(selectedFile):
        if msg.askyesno(title="continue?", message=f"overwrite '{selectedFile}'?"):
            # write at temp folder
            with open(selectedFile,"w", encoding="UTF-8") as file:
                file.write(json.dumps(tmporarydic))
    
    else:
        # write at file
        with open(selectedFile,"w", encoding="UTF-8") as file:
            file.write(json.dumps(tmporarydic))

    return 0