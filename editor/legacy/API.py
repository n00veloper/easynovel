import sys
import os
import json
import platform
import copy

def historydata(gather):
    pass

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

def no_gui():

    while True:
        # check save
        savestage = '0' # stage of progress
        if os.path.isfile(f"{file_path}save.save"): # static save file
            with open(f"{file_path}save.save", "r", encoding="utf-8") as file:
                for line in file:
                    # if save.save has save data...
                    if "[savastage] = " in line:
                        savestage = line.replace("[savastage] = ", "").replace("\n", "")
                    if "[awnsers] = " in line:
                        awnsers = line.replace("[awnsers] = ", "").replace("\n", "").split("-")
        # get data from history
        with open(f"{file_path}history.ezn", "r", encoding="utf-8") as file:
            data = json.loads(file.readlines()[0])
            compatible = [] # compatible options of history
            needs_s, stage_s, comment_s =  stagefy(savestage)
            i = 1000000000 # up to 1 bilion jumps
            while i > 0:
                for line in data.keys():
                    # compare to continue
                    needs_e, stage_e, comment_e = stagefy(line)
                    # if same point and needs...
                    if stage_e == stage_s and (set(needs_e) == set(needs_s) or set(needs_e) == set(awnsers)):
                        compatible.append(line)
                i -= 1
                if len(compatible) <= 0:
                    stage_s = str(int(stage_s)+1)
                if len(compatible) > 0:
                    break
            first = True # first prompt
            compatible.sort() # order comments
            comments = [] # options
            kill = False # kill if needed
            # prompt everything on the screen
            while True:
                for c in compatible:
                    needs_e, stage_e, comment_e = stagefy(c)
                    if first:
                        first = False
                        print(data[c]["comment"])
                    comment = data[c]["prompt"]
                    print(f"{comment_e[0]}. {comment}")
                    comments.append(comment_e[0])
                    if comment_e[0] == "0":
                        kill = True
                comment = input("awnser... ")

                # if awnsered... break
                if comment in comments:
                    break
            
            awnsers.append(comment) # add awnser
            savestage = f"{str(int(stage_s)+1)}"
            with open(f"{file_path}save.save", "r", encoding="utf-8") as file:
                fill = file.readlines()
            with open(f"{file_path}save.save", "w", encoding="utf-8") as file:
                for line in fill:
                    if "[awnsers] = " in line:
                        awns = ""
                        for a in awnsers:
                            if a != "":
                                awns += f"{a}-"
                        awns = awns[:-1]
                        line = f"[awnsers] = {awns}\n"
                    if "[savastage] = " in line:
                        line = f"[savastage] = {savestage}\n"
                    file.write(line)
            if kill:
                quit(0)
            


if __name__ == "__main__":
    file_path = os.path.realpath(__file__)
    # get os for path
    if platform.system() == "Windows":
        file_path = file_path.split("\\")
        del file_path[-1]
        file_path = ''.join(f"{x}\\" for x in file_path)
    else:
        file_path = file_path.split("/")
        del file_path[-1]
        file_path = ''.join(f"{x}/" for x in file_path)
    # API function
    i = 0
    while i < len(sys.argv):
        if "--api" in sys.argv[i].lower(): # check for /api arg, then return history
            print(historydata(sys.argv[i+1]))
        i += 1
    if not os.path.isfile(f"{file_path}save.save"):
        with open(f"{file_path}save.save", "w", encoding="utf-8") as file:
            file.write("[savastage] = 0\n")
            file.write("[awnsers] = \n")
    # else... run on prompt
    if os.path.isfile(f"{file_path}history.ezn"):
            no_gui()
            

