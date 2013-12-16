#-------------------------------------------------------------------------------
# Name:       CexControl
# Purpose:    Automatically add mined coins on Cex.IO to GHS pool
#
# Author:     Eloque
#
# Created:    19-11-2013
# Copyright:  (c) Eloque 2013
# Licence:    Free to use, copy and distribute as long as I'm credited
#             Provided as is, use at your own risk and for your own benefit
# Donate BTC: 17w7oe38d8Rm3pHYLwNZLn8TFSBVEaogJA
#-------------------------------------------------------------------------------

import CexControl

from Tkinter import *
from Tkinter import Button
from Tkinter import Entry
from Tkinter import Frame
from Tkinter import Label
from Tkinter import Tk

import threading
## import Queue

def main():
    master.title(title)  # @UndefinedVariable
    frame = Frame(master, bd=2, relief=SUNKEN)  # @UndefinedVariable


# The main application class
class CexControlGui:
    def __init__(self, master):

        self.balanceBTC = StringVar()
        self.balanceNMC = StringVar()
        self.balanceGHS = StringVar()

        # Gui Creation Block
        frame = Frame(master, bd=2, relief=SUNKEN)
        self.master = master
        self.CreateGui(frame)

        ## Take logging into the GUI app
        CexControl.log.SetOutput(False)
        CexControl.log.LogText = CexControl.log.LogText = self.display

        ## Try to get the configuration settings in the settings object
        self.settings = CexControl.Settings()
        self.settings.LoadSettings()

        self.MakeConnection()

    def Center(self):
        root.withdraw()
        root.update_idletasks()  # Update "requested size" from geometry manager

        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.geometry("+%d+%d" % (x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        root.deiconify()

    # Create the overal gui of the application
    def CreateGui(self, frame):

        # Select File Location
        ##self.FileLocation = Entry(frame, width=30 )
        ##self.FileLocation.insert(0, self.sLogLocation )
        #3self.FileLocation.grid(row=3, column=1)

        # Creat buttons to the right
        self.frmButtons = Frame(frame, bd=2, relief=SUNKEN)
        self.frmButtons.grid( row=0, column=0, sticky=N )

        # Creat buttons to the right
        self.frmLabels = Frame(frame, bd=2, relief=SUNKEN)
        self.frmLabels.grid( row=1, column=0, sticky=N )

        self.button = Button(self.frmButtons, text="Get balance", command=self.RetrieveBalance )
        self.button.grid(row=1, column=1 )

        self.button = Button(self.frmButtons, text="Trade Loop", command=self.DoTradeLoop )
        self.button.grid(row=2, column=1 )

        self.label = Label(self.frmLabels, text = "BTC")
        self.label.grid(row=2, column=1 )

        self.labelBTC = Label(self.frmLabels, width=20, textvariable = self.balanceBTC )
        self.labelBTC.grid(row=2, column=2 )

        self.label = Label(self.frmLabels, text = "NMC")
        self.label.grid(row=3, column=1 )

        self.labelNMC = Label(self.frmLabels, width=20, textvariable = self.balanceNMC )
        self.labelNMC.grid(row=3, column=2 )

        self.label = Label(self.frmLabels, text = "GHS")
        self.label.grid(row=4, column=1 )

        self.labelGHS = Label(self.frmLabels, width=20, textvariable = self.balanceGHS )
        self.labelGHS.grid(row=4, column=2 )

        self.display = Text(frame,height = 12, width=60) ## ,font=("Times", 12)
        self.display.grid(row=0, column=1 )

        ## self.frmButtons.pack()
        frame.pack()

        self.Center()

    def MakeConnection(self):
        self.Context = self.settings.GetContext()

    # PlaceHolder null operation
    def PlaceHolder(self):
        pass
        return

    # Retrieve BTC, NMC and GHS Balace
    def RetrieveBalance(self):

        self.balanceBTC.set("%.8f" % CexControl.GetBalance(self.Context, "BTC"))
        self.balanceNMC.set("%.8f" % CexControl.GetBalance(self.Context, "NMC"))
        self.balanceGHS.set("%.8f" % CexControl.GetBalance(self.Context, "GHS"))

        ## Make sure that the labels are there as well
        ## t = threading.Timer(2, lambda: self.balanceBTC.set("%.8f" % CexControl.GetBalance(self.Context, "BTC")) )
        ## t.start()

        ## t = threading.Timer(2, lambda: self.balanceNMC.set("%.8f" % CexControl.GetBalance(self.Context, "NMC")) )
        ## t.start()

        ## t = threading.Timer(2, lambda: self.balanceGHS.set("%.8f" % CexControl.GetBalance(self.Context, "GHS")) )
        ##t.start()

        return

    ## Execute tradeloop
    def DoTradeLoop(self):

        CexControl.TradeLoop(self.Context, self.settings)
        return


##if __name__ == '__main__':
##    main()
# Run the programs

root = Tk()
app = CexControlGui(root)

title = "CexControl version %s" % CexControl.version

app.master.title(title)

## root.resizable(0,0)
## root.minsize(280,60)

root.mainloop()

