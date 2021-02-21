### @JZU 03022021

import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from time import time
import os;import shutil
class background:
    backgroundserie=[];backgroundname=[]
    def __init__(self,adress:str):
        self.name=str(adress).split("/")[-1].split("\\")[-1].split(".")[0]
        pic=cv2.imread(adress);pic=cv2.resize(pic,(1920,1080),interpolation=cv2.INTER_LANCZOS4)
        self.adress=str(adress).split(".")[0]+"_resize.png"
        cv2.imwrite(self.adress,pic)
        if self.name.lower() not in background.backgroundname:
            background.backgroundserie.append(self)
            background.backgroundname.append(self.name.lower())

    def add_text(self,text:str,adress_stock="./"):
        pic=cv2.imread(self.adress)
        width,heigh=np.shape(pic)[:2]
        if "：" in text:
            nom=text.split("：")[0];dialog=text[len(nom)+1:];n=nom.split(" ")[-1]
            if n!="Moi" and n!="？":
                n=n.replace("？","Q").replace("é","e").replace("è","e").replace("à","a")
                pers=cv2.imread(self.adress[:-len(str(self.adress).split("/")[-1].split("\\")[-1])]+n+".png")
                try:
                    p_width,p_heigh=np.shape(pers)[:2]
                except:
                    try:
                        pers=cv2.imread(self.adress[:-len(str(self.adress).split("/")[-1].split("\\")[-1])]+n+".PNG")
                        p_width,p_heigh=np.shape(pers)[:2]
                    except:
                        try:
                            pers=cv2.imread(self.adress[:-len(str(self.adress).split("/")[-1].split("\\")[-1])]+n+".jpg")
                            p_width,p_heigh=np.shape(pers)[:2]
                        except:
                            try:
                                pers=cv2.imread(self.adress[:-len(str(self.adress).split("/")[-1].split("\\")[-1])]+n+".JPG")
                                p_width,p_heigh=np.shape(pers)[:2]
                            except:
                                print(self.adress[:-len(str(self.adress).split("/")[-1].split("\\")[-1])]+n)
                pers=cv2.resize(pers,(1920,1080),fx=1000/p_heigh,fy=1000/p_heigh)
                overlay=np.where((pers[:,:,0]<250)+(pers[:,:,1]<250)+(pers[:,:,2]<250))
                pic[overlay]=pers[overlay]
            cv2.rectangle(pic, (130,int(1080/7*4)-100), (500, int(1080/7*4)-40),(230,200,200), -1)
            pic_o=pic.copy()
            cv2.rectangle(pic, (130,int(1080/7*4)-40), (1820, 1080-130),(250,255,255), -1)
            pic=cv2.addWeighted(pic_o, 0.3,pic,0.7,0)
            pic=Image.fromarray(cv2.cvtColor(pic,cv2.COLOR_BGR2RGB))
            draw=ImageDraw.Draw(pic)
            draw.text((150,int(1080/7*4)-90),str(nom.split("_")[0]),font=ImageFont.truetype('simhei.ttf', 40),fill=(0,0,0))
            draw.text((200,int(1080/7*4)),str(dialog),font=ImageFont.truetype('simhei.ttf', 25),fill=(0,0,0))
            pic = cv2.cvtColor(np.asarray(pic),cv2.COLOR_RGB2BGR)
        else:
            pic_o=pic.copy()
            cv2.rectangle(pic,(130,130),(1820, 1080-130),(250,255,255), -1)
            pic=cv2.addWeighted(pic_o,0.3,pic,0.7,0)
            pic=Image.fromarray(cv2.cvtColor(pic,cv2.COLOR_BGR2RGB))
            draw=ImageDraw.Draw(pic)
            draw.text((150,300),str(text),font=ImageFont.truetype('simhei.ttf', 25),fill=(0,0,0))
            pic = cv2.cvtColor(np.asarray(pic),cv2.COLOR_RGB2BGR)
        address_stock=str(adress_stock)+self.name+"_"+str(time())+".png"
        cv2.imwrite(address_stock,pic)
        scene(address_stock,max(int(len(text)/30),5))

class scene:
    sceneserie=[]
    def __init__(self,address:str,sec:int):
        self.address=str(address)
        self.frame=max(int(sec),2)
        scene.sceneserie.append(self)

import tkinter as tk
root = tk.Tk();root.withdraw()
from tkinter import filedialog
def txt2avi(fps:int=1):
    print("该剧情剧本文件路径：",end="\t")
    address_str=filedialog.askopenfilename()
    print(address_str)
    print("图片素材文件夹路径：",end="\t")
    address_img=filedialog.askdirectory()
    print(address_img)
    print("视频保存文件夹路径：",end="\t")
    address_avi=filedialog.askdirectory()
    print(address_avi)
    file=address_avi.split(".")[0]+"_roaming"
    background.backgroundserie=[]
    scene.sceneserie=[]
    try:
        os.makedirs(file)
    except:
        pass
    indice=0;text_actuel=""
    with open(address_str, 'r',encoding="UTF-8") as f:
        for line in f.readlines():
            if line.split(":")[0].split("：")[0].lower()[-2:]=="bg":
                bgname=line.split("\n")[0].split(":")[-1].split("：")[-1].replace(" ","").replace("é","e").replace("è","e").replace("à","a").lower()
                if bgname in background.backgroundname:
                    bg=background.backgroundserie[background.backgroundname.index(bgname)]
                else:
                    try:
                        f=address_img+"/"+bgname+".png"
                        bg=background(f)
                    except:
                        f=address_img+"/"+bgname+".jpg"
                        bg=background(f)
                scene(bg.adress,3)
                continue
            if indice:
                for i in range(int(len(line)/120+1)):
                    text_actuel+=line[i*120:(i+1)*120]+"\n"
                bg.add_text(text_actuel[:-1],adress_stock=directory+"/")
                text_actuel="";indice=0
            else:
                indice=1
                for i in range(int(len(line)/60+1)):
                    text_actuel+=line[i*60:(i+1)/60]+"\n"
                text_actuel=text_actuel[:-1]
    videoWriter=cv2.VideoWriter(address_avi+"/"+address_avi.split("/")[-1].split("\\")[-1]+".avi",cv2.VideoWriter_fourcc(*'XVID'),int(fps),(1920,1080))
    for scene_actuel in scene.sceneserie:
        address,sec=scene_actuel.address,scene_actuel.frame
        frame=cv2.imread(address)
        for j in range(sec*int(fps)):
            videoWriter.write(frame)
    videoWriter.release();shutil.rmtree(file)

def txts2avi(fps:int=1):
    print("剧情剧本文件夹路径：",end="\t")
    address_str=filedialog.askdirectory()
    print(address_str)
    print("图片素材文件夹路径：",end="\t")
    address_img=filedialog.askdirectory()
    print(address_img)
    print("视频保存文件夹路径：",end="\t")
    address_avi=filedialog.askdirectory()
    print(address_avi)
    background.backgroundserie=[]
    files= os.listdir(address_str);i=0
    for file in files:
        if ".txt" not in file:
            continue
        scene.sceneserie=[]
        try:
            directory=address_avi.split(".")[0]+"_roaming"+str(i)
            os.makedirs(directory)
        except:
            pass
        indice=0;text_actuel="";print(str(i+1)+"/"+str(len(files)),address_str+"/"+file)
        with open(address_str+"/"+file, 'r',encoding="UTF-8") as f:
            for line in f.readlines():
                if line.split(":")[0].split("：")[0].lower()[-2:]=="bg":
                    bgname=line.split("\n")[0].split(":")[-1].split("：")[-1].replace(" ","").replace("é","e").replace("è","e").replace("à","a").lower()
                    if bgname in background.backgroundname:
                        bg=background.backgroundserie[background.backgroundname.index(bgname)]
                    else:
                        try:
                            f=address_img+"/"+bgname+".png"
                            bg=background(f)
                        except:
                            try:
                                f=address_img+"/"+bgname+".jpg"
                                bg=background(f)
                            except:
                                try:
                                    f=address_img+"/"+bgname+".PNG"
                                    bg=background(f)
                                except:
                                    try:
                                        f=address_img+"/"+bgname+".JPG"
                                        bg=background(f)
                                    except:
                                        print(address_img+"/"+bgname)
                    scene(bg.adress,2)
                    continue
                if indice:
                    for j in range(int(len(line)/120+1)):
                        text_actuel+=line[j*120:(j+1)*120]+"\n"
                    bg.add_text(text_actuel[:-1].replace("î","i").replace("ï","i").replace("û","u").replace("â","a").replace("À","A").replace("ê","e").replace("ô","o").replace("ç","c"),adress_stock=directory+"/")
                    text_actuel="";indice=0
                else:
                    indice=1
                    for j in range(int(len(line)/60+1)):
                        text_actuel+=line[j*60:(j+1)*60]+"\n"
                    text_actuel=text_actuel[:-1]
        videoWriter=cv2.VideoWriter(address_avi+"/"+address_avi.split("/")[-1].split("\\")[-1]+"_"+str(i)+".avi",cv2.VideoWriter_fourcc(*'XVID'),int(fps),(1920,1080))
        for scene_actuel in scene.sceneserie:
            address,sec=scene_actuel.address,scene_actuel.frame
            frame=cv2.imread(address)
            for j in range(sec):
                videoWriter.write(frame)
        videoWriter.release();i+=1;shutil.rmtree(directory)

if __name__=="__main__":
    ismulti=int(input("您是要处理单个剧本还是一套剧本（单个输入0，一套输入1）:\t"))
    if ismulti:
        txts2avi(fps=1) #For all videos
    else:
        txt2avi(fps=1) #For un video
    print("\n转化完毕，谢谢您的使用！")
