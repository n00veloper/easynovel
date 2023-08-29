import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import tempfile as tmp
import os
import json
import platform
import shutil
import _thread
import pygame

def stagefy(savestage):
    # get stage progress
    savestage = savestage.replace("\n", "")
    stage = savestage.split(".")
    if len(stage) <= 1:
        stage.append("1")
    # stage so far: ["(X,y)1", "1"]
        
    # if has branches
    if "(" in stage[0]:
        spl = stage[0].split(")") # so far ["(x,y", "1"]
        tmp_stage = spl[1] # stage result = "1"
        spl = spl[0].replace("(", "") # so far "x,y"
        needs = spl.split(",") # needs result = "["x", "y"]"
    # if not
    else:
        tmp_stage = stage[0]
        needs = []
    del stage[0]
    return needs, tmp_stage, stage # list, str, list = needs, comment, 

def removeHistory(remove, listbox):
    global data
    """
    remove is the tkinter object where points to what to be removed
    listbox is the listbox itself
    """
    # get os for path
    if platform.system() == "Windows":
        path = f"{tmpfolder}\\futuresave.ezn"
    else:
        path = f"{tmpfolder}/futuresave.ezn"
    
    # load data to change, or ignores
    if os.path.exists(path):
        with open(path,"r", encoding="UTF-8") as file:
            data = json.loads(file.readlines()[0])

        # change data
        data.pop(remove.get("1.0",tk.END), None)

        # write at temp folder
        with open(path,"w", encoding="UTF-8") as file:
            file.write(json.dumps(data))
        
        # delete all recourses on history list
        listbox.delete(0,tk.END)

        # add stuff to listbox, but sort out first
        ordered = sorted(data.keys())
        for order in ordered:
            comment = data[order]["comment"][0:10]
            prompt = data[order]["prompt"][0:10]
            listbox.insert(tk.END,f"{order} - c:{comment} - a:{prompt}")
        
        return 0 # return success
    return 1

def addHistory(add, listbox):
    global data
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

    # add stuff to listbox, but sort out first
    ordered = sorted(data.keys())
    for order in ordered:
        comment = data[order]["comment"][0:10]
        prompt = data[order]["prompt"][0:10]
        listbox.insert(tk.END,f"{order} - c:{comment} - a:{prompt}")
    
    return 0 # return success


def loadHistory(listbox):
    global data
    # will ask to open a .ezn file (eazynovel)
    filetypes = (
        ('easynovel files', '*.ezn'),
        ('All files', '*.*')
    )
    selectedFile = fd.askopenfilename(title="load your file", initialdir="./", filetypes=filetypes)

    # get os for path
    if platform.system() == "Windows":
        path = f"{tmpfolder}\\futuresave.ezn"
    else:
        path = f"{tmpfolder}/futuresave.ezn"

    # check file...
    if os.path.isfile(selectedFile):
        # copy save to temp
        shutil.copyfile(selectedFile, path)
        
        # read temp folder
        with open(path,"r", encoding="UTF-8") as file:
            data = json.loads(file.readlines()[0])
        
        # delete all recourses on history list
        listbox.delete(0,tk.END)

        # add stuff to listbox, but sort out first
        ordered = sorted(data.keys())
        for order in ordered:
            comment = data[order]["comment"][0:10]
            prompt = data[order]["prompt"][0:10]
            listbox.insert(tk.END,f"{order} - c:{comment} - a:{prompt}")

def saveHistory():
    # will ask to save a .ezn file (eazynovel)
    filetypes = (
        ('easynovel files', '*.ezn'),
        ('All files', '*.*')
    )
    selectedFile = fd.asksaveasfilename(title="save your file", initialdir="./", filetypes=filetypes)
    # get os for path
    if platform.system() == "Windows":
        path = f"{tmpfolder}\\futuresave.ezn"
    else:
        path = f"{tmpfolder}/futuresave.ezn"
    
    #if does not have extension
    if not "." in selectedFile:
        selectedFile += ".ezn"

    # if file does not exists, but temp exists, copy to path
    if not os.path.isfile(selectedFile) and os.path.isfile(path):
        shutil.copyfile(path, selectedFile)

    # if temp does not exists (user did not made changes), make lazyerror
    elif not os.path.isfile(path):
        msg.showerror(title="too lazy error code", message="create something first!!!")
    
    # if file exists, and temp too, overwrite
    elif os.path.isfile(selectedFile) and os.path.isfile(path):
        if msg.askyesno(title="continue?", message=f"overwrite '{selectedFile}'?"):
            shutil.copyfile(path, selectedFile)
    
    return 0

def newHistory(listbox):
    global tmpfolder
    tmpfolder = tmp.mkdtemp() # new temporary folder, modified save data
    
    # delete all recourses on history list
    listbox.delete(0,tk.END)
    
    return 0

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
    load_button = tk.Button(master=row_1, text='load', command= lambda: loadHistory(listBoxHistory))
    load_button.grid(column=0, row=0)

    new_button = tk.Button(master=row_1, text='new', command= lambda: newHistory(listBoxHistory))
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

def visualGUI():
    global data
    pygame.init()
    screen = pygame.display.set_mode((400, 400), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    camera = [0,0]
    camera_speed = 2 # speed
    camera_tick = 2 # sleep

    def visualLoad():
        returned = []
        for d in data.keys():
            #fonts from system
            identifier = pygame.font.SysFont('Arial', 25)
            comment = pygame.font.SysFont('Arial', 20)
            awnser = pygame.font.SysFont('Arial', 15)

            # render text
            size = [identifier.size(d), comment.size(data[d]["comment"]), awnser.size(data[d]["prompt"])] 
            identifier = identifier.render(d, True, (0,0,0))
            comment = comment.render(data[d]["comment"], True, (0,0,0))
            awnser = awnser.render(data[d]["prompt"], True, (0,0,0))
            needs_e, stage_e, comment_e = stagefy(d)
            pos = [int(stage_e), int(comment_e[0])+1, len(needs_e)]
            # to return text
            returned.append([identifier, comment, awnser, pos, size])
        return returned

    # update ui every... (open file)
    update_history_ticks = 100
    update_history = 100
    visualdata = visualLoad()
    while True:
        # check if quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # check if pressed, moves every X ticks
        move_ticker = 0
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if move_ticker == 0:
                move_ticker = camera_tick
                camera[0] -= camera_speed
        if keys[pygame.K_RIGHT]:
            if move_ticker == 0:   
                move_ticker = camera_tick     
                camera[0] += camera_speed
        if keys[pygame.K_DOWN]:
            if move_ticker == 0:
                move_ticker = camera_tick
                camera[1] += camera_speed
        if keys[pygame.K_UP]:
            if move_ticker == 0:   
                move_ticker = camera_tick     
                camera[1] -= camera_speed
            
        screen.fill((255, 255, 255))
        
        # placeholder
        #screen.blit(dialogue, (40-camera[0],40-camera[1]))
        #screen.blit(name, (40-camera[0],140-camera[1]))
        #screen.blit(game_over, (40-camera[0],240-camera[1]))
        
        # reset ticks
        if move_ticker > 0:
            move_ticker -= 1
        if update_history == 0:
            visualdata = visualLoad()
            update_history = update_history_ticks 
        if update_history > 0:
            update_history -= 1

        # loop for data...
        sz, szy = (0, 0)
        inf = {}
        oydt = 0
        for dt in visualdata:
            # dt = [identifier, comment, awnser, pos, size]
            szy = 0
            # if has same history path, get older size
            if str(dt[3][0]) in inf:
                szy = inf[str(dt[3][0])]
                print(dt[3][0], szy)
            if str(dt[3][0])+" "+str(dt[3][1]) in inf:
                szy = inf[str(dt[3][0])+" "+str(dt[3][1])]

            # do some math to show the text
            screen.blit(dt[0], ((dt[3][0]*150)-camera[0],((dt[3][1]*oydt)/3)+szy-camera[1]))
            szy += dt[4][0][1]
            screen.blit(dt[1], ((dt[3][0]*150)-camera[0],((dt[3][1]*oydt)/3)+szy-camera[1]))
            szy += dt[4][1][1]
            screen.blit(dt[2], ((dt[3][0]*150)-camera[0],((dt[3][1]*oydt)/3)+szy-camera[1]))
            szy += dt[4][2][1]
            oydt = dt[4][1][1]+dt[4][2][1]+dt[4][0][1]

            #save every id, and size used, for spacing
            if str(dt[3][0]) in inf:
                if inf[str(dt[3][0])] > szy:
                    inf[str(dt[3][0])] = szy+oydt
                else:
                    inf[str(dt[3][0])] = szy+oydt
            else:
                inf[str(dt[3][0])] = szy+oydt
            if str(dt[3][0])+" "+str(dt[3][1]) in inf:
                if inf[str(dt[3][0])+" "+str(dt[3][1])] > szy:
                    inf[str(dt[3][0])+" "+str(dt[3][1])] = szy+oydt
                    print(szy)
                else:
                    inf[str(dt[3][0])+" "+str(dt[3][1])] = szy+oydt
            else:
                inf[str(dt[3][0])+" "+str(dt[3][1])] = szy+oydt


        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    tmpfolder = tmp.mkdtemp() #temporary folder, modified save data
    data = {} # info of the history itself
    _thread.start_new_thread(visualGUI, ())
    GUI()