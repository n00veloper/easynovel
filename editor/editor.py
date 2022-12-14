import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import tempfile as tmp
import os
import json
import platform

def removeHistory():
    pass

def addHistory(add, listbox):
    """
    add is a list of:
    [0] comment
    [1] prompt
    [2] log
    all on tkinter text object, needs to be extracted.
    listbox is a listbox tkinter object
    """
    # get os for path
    if platform.system() == "Windows":
        path = f"{tmpfolder}\\futuresave.ezn"
    else:
        path = f"{tmpfolder}/futuresave.ezn"
    
    # if blank, ignores
    if add[0].get("1.0",tk.END) == "" or add[1].get("1.0",tk.END) == "" or add[2].get("1.0",tk.END) == "":
        return 1
    
    # load data to change, or ignores
    if os.path.exists(path):
        with open(path,"r", encoding="UTF-8") as file:
            data = json.loads(file.readlines()[0])
    else:
        data = {}
    # change data
    data[add[2].get("1.0",tk.END)] = {"comment": add[0].get("1.0",tk.END), "prompt": add[1].get("1.0",tk.END)}
    
    # write at temp folder
    with open(path,"w", encoding="UTF-8") as file:
        file.write(json.dumps(data))
    
    # delete all recourses on history list
    listbox.delete(0,tk.END)

    # add stuff to listbox, but short out first
    ordered = sorted(data.keys(), key = lambda x:float(x))
    for order in ordered:
        comment = data[order]["comment"][0:10]
        prompt = data[order]["prompt"][0:10]
        listbox.insert(tk.END,f"{order} - c:{comment} - a:{prompt}")
    
    return 0 # return success


def loadHistory():
    # will ask to open a .ezn file (eazynovel)
    filetypes = (
        ('easynovel files', '*.ezn'),
        ('All files', '*.*')
    )
    selectedFile = fd.askopenfilename(title="load your file", initialdir="./", filetypes=filetypes)

def saveHistory():
    # will ask to save a .ezn file (eazynovel)
    filetypes = (
        ('easynovel files', '*.ezn'),
        ('All files', '*.*')
    )
    selectedFile = fd.asksaveasfilename(title="save your file", initialdir="./", filetypes=filetypes)

def newHistory():
    # will make everything blank, to create a new history.
    pass

def GUI():
    master = tk.Tk()
    master.geometry("600x300")
    master.resizable(True, True)

    # they see me scrooling, the hating...
    frame=tk.Frame(master=master)
    frame.pack(expand=True, fill=tk.BOTH)
    
    canvas=tk.Canvas(frame,bg='gray')
    
    hbar=tk.Scrollbar(frame,orient=tk.HORIZONTAL)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)
    hbar.config(command = canvas.xview)
    
    vbar = tk.Scrollbar(frame,orient = tk.VERTICAL)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    vbar.config(command = canvas.yview)
    
    canvas.config(width=300,height=300)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.bind('<Configure>', lambda e: canvas.config(scrollregion=canvas.bbox('all')))
    canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    #main canvas frame
    w = tk.Frame(master=canvas)
    canvas.create_window((0,0), window=w, anchor=tk.CENTER)

    # container for better design
    row_1 = tk.Frame(master=w)
    row_1.grid(column=0, row=0)

    # save, load or new at 1st row
    load_button = tk.Button(master=row_1, text='load', command= lambda: loadHistory())
    load_button.grid(column=0, row=0)

    new_button = tk.Button(master=row_1, text='new', command= lambda: newHistory())
    new_button.grid(column=1, row=0)

    new_button = tk.Button(master=row_1, text='save', command= lambda: saveHistory())
    new_button.grid(column=2, row=0)

    # container for better design
    row_2 = tk.Frame(master=w)
    row_2.grid(column=0, row=1)

    # will list every history entry at 2nd row
    i_label = tk.Label(master=row_2, text = "history log")
    i_label.grid(column=0, row=0)
    listBoxHistory = tk.Listbox(master=row_2, height=5, width=60)
    listBoxHistory.grid(column=1, row=0)

    # container for better design
    row_3 = tk.Frame(master=w)
    row_3.grid(column=0, row=2)

    # full form at 3th row
    i_label = tk.Label(master=row_3, text = "comment")
    comment = tk.Text(master=row_3, height = 5, width = 25)
    i_label.grid(column=0, row=0)
    comment.grid(column=1, row=0)

    p_label = tk.Label(master=row_3, text = "awnser")
    prompt = tk.Text(master=row_3, height = 5, width = 25)
    p_label.grid(column=2, row=0)
    prompt.grid(column=3, row=0)

    l_label = tk.Label(master=row_3, text = "history log number")
    log = tk.Text(master=row_3, height = 1, width = 25)
    l_label.grid(column=0, row=1)
    log.grid(column=1, row=1)

    # container for better design
    row_4 = tk.Frame(master=w)
    row_4.grid(column=0, row=3)

    # will remove/add history at 4th row
    remove_button = tk.Button(master=row_4, text='remove', command=lambda: removeHistory(log, listBoxHistory))
    remove_button.grid(column=0, row=0)

    add_button = tk.Button(master=row_4, text='add', command=lambda: addHistory([comment, prompt, log], listBoxHistory))
    add_button.grid(column=1, row=0)

    master.mainloop()
    return 0

if __name__ == "__main__":
    tmpfolder = tmp.mkdtemp() #temporary folder, modified save data
    GUI()