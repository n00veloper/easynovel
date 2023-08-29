import tempfile as tmp
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import os
import platform
import json

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

            history = json.loads(file.readlines()[0])

            # add widgets like it should.


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
    
    # if file exists, overwrite
    if os.path.isfile(selectedFile):
        if msg.askyesno(title="continue?", message=f"overwrite '{selectedFile}'?"):
            # write at temp folder
            with open(selectedFile,"w", encoding="UTF-8") as file:
                file.write(json.dumps(history))
    
    else:
        # write at file
        with open(selectedFile,"w", encoding="UTF-8") as file:
            file.write(json.dumps(history))

    return 0