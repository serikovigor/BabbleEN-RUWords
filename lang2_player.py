import os
import time
import tempfile

from gtts import gTTS
import pygame as pg
from utils import *
import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as tkFileDialog


class BabbleApp:

    def __init__(self, root, loader: AbstractLang2Loader):
        self.root = root
        self.loader = loader

        # ------
        self.root.title("Lang2 files audio-Player")
        self.large_font = tkFont.Font(family="Arial", size=18, weight="bold")
        # ---------------------
        self.search_results_txt = tk.Text(width=50, height=10, font=self.large_font)
        # self.search_results_txt.grid(row=1, column=0)
        self.search_results_txt.pack(side=tk.TOP, fill=tk.X)
        # --
        self.statusbar = tk.Label(text="on the way…", bd=1, relief=tk.SUNKEN,
                                  anchor=tk.W, font=self.large_font)

        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        # --
        self.mainmenu = tk.Menu(root)
        self.root.config(menu=self.mainmenu)

        self.filemenu = tk.Menu(self.mainmenu, tearoff=0, font=self.large_font)
        self.filemenu.add_command(label="Open lang2", font=self.large_font,
                                  command=self.open_file)

        self.playmenu = tk.Menu(self.mainmenu, tearoff=0)
        self.playmenu.add_command(label="PLAY | STOP", command=self.play_stop,
                                  font=self.large_font)
        # self.playmenu.add_command(label="Stop", command=self.play_stop,
        #                          font=self.large_font)

        self.mainmenu.add_cascade(label="File",
                                  menu=self.filemenu, font=self.large_font)
        self.mainmenu.add_cascade(label="PLAY/STOP",
                                  menu=self.playmenu, font=self.large_font)
        # --------------

        self.ttsBusy = False
        self.updateUIFlag = True

        self.wordPos: int = 0  # played word position
        self.sentPos = -1

        self.wordsPlayFlag: bool = False
        self.currentSentence: str = None
        self.resetBusyCounter: int = 0
        # --
        self.store = self.loader.words_store
        self.updateUI()

    def open_file(self):
        filename = tkFileDialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                                filetypes=(("lang2 files", "*.lang2"), ("all files", "*.*")))
        print(filename)
        self.loader.load(filename)
        self.store = self.loader.words_store
        self.newWord(0)



    def play_stop(self):
        self.wordsPlayFlag = not self.wordsPlayFlag
        if not self.wordsPlayFlag:
            pg.mixer.music.stop()
        self.updateUI()

    def newWord(self, pos: int):
        self.sentPos = -1
        self.wordPos = pos

    def ttxBusy(self) -> bool:
        return pg.mixer.music.get_busy()

    def updateUI(self):
        if self.wordsPlayFlag:
            self.statusbar.config(text="PLAING")
        else:
            self.statusbar.config(text="STOPPED")
        self.search_results_txt.delete('1.0', tk.END)
        for x in reversed(self.store.words_array[self.wordPos]):
            self.search_results_txt.insert(1.0, x + '\n')

    def play_text(self, text, gts_lang):
        temp = tempfile.NamedTemporaryFile()
        var = gTTS(text=text, lang=gts_lang, slow=False)
        var.save(temp.name)
        #
        pg.mixer.music.load(temp.name)
        pg.mixer.music.play()

    def setNextWord(self):

        self.sentPos += 1
        if self.sentPos >= len(self.store.words_array[self.wordPos]):
            self.updateUIFlag = True
            self.sentPos = 0
            self.wordPos += 1
            # if self.wordPos >= len(self.wordsArray):
            if self.wordPos >= self.store.words_array_size:
                self.wordPos = 0

        if self.sentPos == 0:
            self.updateUI()

        return self.store.words_array[self.wordPos][self.sentPos]

    def getCurrentWord(self):
        return self.store.words_array[self.wordPos][self.sentPos]

    def tick(self):
        if self.updateUIFlag:
            self.updateUI()
        if not self.wordsPlayFlag:
            return
        if self.ttxBusy():
            return
        # --
        word = self.setNextWord()

        if (self.sentPos % 2) == 0:
            self.play_text(word, 'en')
        else:
            self.play_text(word, 'ru')


if __name__ == '__main__':

    pg.init()
    pg.mixer.init()

    file = "lang2/first.lang2"
    l2_loader = Lang2FileWordsLoader(file)

    root = tk.Tk()
    root.geometry('640x480+100+100')
    main_dialog = tk.Frame(root)
    app = BabbleApp(root, l2_loader)

    while 1:
        try:
            root.update()
        except:
            print("dialog error!!!")
        # --
        time.sleep(0.1)
        app.tick()

    print('BY!')
