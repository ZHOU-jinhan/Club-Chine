### @JZU 17022021

# pip install pypinyin
from pypinyin import pinyin
import re
# pip/conda install googletrans==4.0.0-rc1
from googletrans import Translator
import tkinter as tk
root = tk.Tk();root.withdraw()
from tkinter import filedialog
try:
    translator = Translator(service_urls=['translate.google.com',])
except:
    translator = Translator(service_urls=['translate.google.cn',])

class Change:
    def __init__(self):
        self.pinyin = []
        
    def write_file(self):
        address_txt=filedialog.askopenfilename()
        with open(address_txt, encoding='utf-8') as f:
            txt=f.readlines()
        print("")
        d=1
        for w in txt[0]+txt[1]+txt[2]:
            if ord(w)>11903 and w not in "，！？：“”【】":
                d=0;break
        if d:
            src_="fr";dest_="zh-cn"
        else:
            src_="zh-cn";dest_="fr"
        with open('%s_translated.txt' % address_txt.split(".")[0], 'w', encoding='utf-8') as f:
            for line in txt:
                if line.strip() == '':
                    continue
                if dest_=="fr":
                    _new_line = re.sub(r'\s', '', line)
                    _pinyin = ''.join(map(lambda x: x[0].ljust(6), pinyin(_new_line)))
                    _lyric = self.split_words(_new_line)
                    _trans = translator.translate(_new_line,src=src_,dest=dest_).text
                    f.write('%s\n%s\n%s\n\n' % (_pinyin, _lyric,_trans))
                else:
                    _new_line = re.sub(r'\n', '', line)
                    _trans = translator.translate(_new_line,src=src_,dest=dest_).text
                    f.write('%s\n%s\n\n' % (_new_line,_trans))

    @staticmethod
    def split_words(words):
        word_list = ""
        tmp = ""
        for string in words:
            if len(bytes(string, 'utf-8')) == 3 and len(string) == 1:
                if tmp != '':
                    word_list += tmp.ljust(6)
                    tmp = ""
                word_list += string.ljust(5)
            else:
                tmp += string
        return word_list


if __name__ == '__main__':
    Main = Change()
    Main.write_file()
