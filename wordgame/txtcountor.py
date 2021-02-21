### @JZU 03022021

import os;import shutil
import tkinter as tk
root = tk.Tk();root.withdraw()
from tkinter import filedialog
def txt2info():
    print("该剧情剧本文件路径：",end="\t")
    file=filedialog.askopenfilename()
    background=[];personnage=[]
    with open(file, 'r',encoding="UTF-8") as f:
        indice=0
        for line in f.readlines():
            if line.split(":")[0].split("：")[0].lower()[-2:]=="bg":
                bgname=line.split("\n")[0].split(":")[-1].split("：")[-1].replace(" ","").lower()
                if bgname not in background:
                    background.append(bgname)
                continue
            if indice:
                indice=0
            else:
                indice=1
                if line[0].lower() in "abcdefghijklmnopqrstuvwxyz?":
                    print(file,line)
                if "：" in line:
                    name=line.split("：")[0].split(" ")[-1]
                    if name!="？":
                        name=name.replace("？","Q")
                        if name not in personnage and name!="Moi":
                            personnage.append(name)
    print("背景：\t",background)
    print("人物：\t",personnage)
    print("图片文件夹路径：",end="\t")
    path=filedialog.askdirectory()
    print(path)
    files=[f.split(".")[0] for f in os.listdir(path)];todo=[]
    for i in background:
        if i not in files:
            todo.append(i)
    for i in personnage:
        if i not in files:
            todo.append(i)
    if len(todo)==0:
        print("素材已备齐，可以进行下一步转化啦！")
    else:
        print("代办：\t",todo)
    
def txts2info():
    print("剧本文件夹路径：",end="\t")
    path=filedialog.askdirectory()
    print(path)
    files= os.listdir(path)
    background=[];personnage=[]
    for file in files:
        with open(path+"/"+file, 'r',encoding="UTF-8") as f:
            indice=0
            for line in f.readlines():
                if line.split(":")[0].split("：")[0].lower()[-2:]=="bg":
                    bgname=line.split("\n")[0].split(":")[-1].split("：")[-1].replace(" ","").lower()
                    if bgname not in background:
                        background.append(bgname)
                    continue
                if indice:
                    indice=0
                else:
                    indice=1
                    if line[0].lower() in "abcdefghijklmnopqrstuvwxyz?":
                        print(file,line)
                    if "：" in line:
                        name=line.split("：")[0].split(" ")[-1]
                        if name!="？":
                            name=name.replace("？","Q")
                            if name not in personnage and name!="Moi":
                                personnage.append(name)
    print("背景：\t",background)
    print("人物：\t",personnage)
    print("图片文件夹路径：",end="\t")
    path=filedialog.askdirectory()
    print(path)
    files=[f.split(".")[0] for f in os.listdir(path)];todo=[]
    for i in background:
        if i not in files:
            todo.append(i)
    for i in personnage:
        if i not in files:
            todo.append(i)
    if len(todo)==0:
        print("素材已备齐，可以进行下一步转化啦！")
    else:
        print("代办：\t",todo)

if __name__=="__main__":
    ismulti=int(input("您是要处理单个剧本还是一套剧本（单个输入0，一套输入1）:\t"))
    if ismulti:
        txts2info() #For all videos
    else:
        txt2info() #For un video
