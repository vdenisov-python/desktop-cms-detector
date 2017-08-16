from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

import os
from appManager import mainManager

#########################################################################

class graphicalInterface:

    #***************************************************************
    def __init__(self, main):

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.color_area_1 = "#FF9696"
        self.area_1 = Frame(main, bg=self.color_area_1)
        self.area_1.pack(side=TOP, fill=X)

        self.label_pathToFile = Label(self.area_1, text="Path to file:",
                                      font="helvetica 11", bg=self.color_area_1)
        self.entry_pathToFile = Entry(self.area_1, width=33, font="helvetica 11")
        self.button_pathToFile = Button(self.area_1, text="Browse",
                                        font="helvetica 11", bg="#FCFF88")
        self.button_pathToFile.bind(
            "<Button-1>",
            lambda event: self.entry_pathToFile.insert(END, askopenfilename())
        )

        self.label_pathToSave = Label(self.area_1, text="Path to save:",
                                      font="helvetica 11", bg=self.color_area_1)
        self.entry_pathToSave = Entry(self.area_1, width=33, font="helvetica 11")
        self.button_pathToSave = Button(self.area_1, text="Browse",
                           font="helvetica 11", bg="#FCFF88")
        self.button_pathToSave.bind(
            "<Button-1>",
            lambda event: self.entry_pathToSave.insert(END, askdirectory())
        )

        self.label_pathToFile.grid(row=0, column=0, padx=(10,0), pady=(15,5), sticky=E)
        self.entry_pathToFile.grid(row=0, column=1, pady=(15,5))
        self.button_pathToFile.grid(row=0, column=2, padx=(5,0), pady=(15,5))

        self.label_pathToSave.grid(row=1, column=0, padx=(10,0), pady=(5,15), sticky=E)
        self.entry_pathToSave.grid(row=1, column=1, pady=(5,15))
        self.button_pathToSave.grid(row=1, column=2, padx=(5,0), pady=(5,15))

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.color_area_2 = "#96FF96"
        self.area_2 = Frame(main, bg=self.color_area_2)
        self.area_2.pack(side=TOP, fill=X)

        self.label_saveOptions = Label(self.area_2, text="Save options:",
                                       font="helvetica 11", bg=self.color_area_2)

        self.chooseExt = StringVar()
        self.radioButton_1 = Radiobutton(self.area_2, text="Save as '*.txt'", variable=self.chooseExt,
                                         value="txt", font="helvetica 11", bg="#FFFFFF")
        self.radioButton_2 = Radiobutton(self.area_2, text="Save as '*.xls'", variable=self.chooseExt,
                                         value="xls", font="helvetica 11", bg="#FFFFFF")
        self.genLogs = BooleanVar()
        self.buttonGenLogs = Checkbutton(self.area_2, text="Create configuration file 'Logs.txt'",
                                         variable=self.genLogs, font="helvetica 11", bg="#FFFFFF")

        self.label_saveOptions.grid(row=0, columnspan=2, padx=(40,0),pady=(10,5))
        self.radioButton_1.grid(row=1, column=0, padx=(80,10))
        self.radioButton_2.grid(row=1, column=1, padx=(10,40))
        self.buttonGenLogs.grid(row=2, padx=(40,0), columnspan=2, pady=(5,15))

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.color_area_3 = "#99CCFF"
        self.area_3 = Frame(main, bg=self.color_area_3)
        self.area_3.pack(side=TOP, fill=X)

        self.buttonRun = Button(self.area_3, text="Begin analysis",
                                font="helvetica 11", bg="#FCFF88")
        self.buttonRun.bind("<Button-1>", self.startAnalysis)
        self.label_statusExecution = Label(self.area_3, text="Status of execution:",
                                           font="helvetica 11", bg=self.color_area_3)
        self.label_statusOutput = Label(self.area_3, text="waiting input valid data".upper(),
                                        font="helvetica 11", bg=self.color_area_3)

        self.buttonRun.grid(row=0, padx=(160,160), pady=(10,10))
        self.label_statusExecution.grid(row=1)
        self.label_statusOutput.grid(row=2, pady=(10,15))

    #***************************************************************

    def startAnalysis(self, event):

        pathToFile = self.entry_pathToFile.get()
        status_File = os.path.exists(pathToFile)

        pathToSave = self.entry_pathToSave.get()
        status_Save = os.path.exists(pathToSave)

        extension = self.chooseExt.get()
        fileLogs = self.genLogs.get()

        if status_File == True and status_Save == True and extension != "":

            userSelect = {
                "pathToFile": pathToFile,
                "pathToSave": pathToSave,
                "extension": extension,
                "genLogs": fileLogs
            }
            print(userSelect)
            print("#"*50)

            ############################################
            finalStatus = mainManager(userSelect).status
            ############################################

            print("#" * 50)
            if finalStatus == True:
                print("Information about sites is stored")
                self.label_statusOutput["text"] = "analysis completed successfully".upper()
            else:
                print("Error when saving data")
                self.label_statusOutput["text"] = "errors in process of analyzing".upper()

        else:
            if status_File == False:
                showerror("ShowError", "Path to file is incorrect")
            elif status_Save == False:
                showerror("ShowError", "Path to save is incorrect")
            elif extension == "":
                showwarning("ShowWarning", "Extension is not selected")

#########################################################################

root = Tk()
root.title("DiscoverCMS - recognizer CMS of web-sites")

x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 3
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 3
root.wm_geometry("+%d+%d" % (x, y))

root.geometry("444x333")
root.minsize(width=444, height=333)
root.maxsize(width=444, height=333)

root.bind("<Escape>", lambda event: root.quit())

GUI = graphicalInterface(root)

root.mainloop()

#========================================================================
