# UI ***************************************************************************
# content = assignment
#
# date    = 2022-01-01
# email   = contact@alexanderrichtertd.com
# *******************************************************************************


import os
import sys
import webbrowser

from Qt import QtWidgets, QtCompat


# *******************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
PATH_UI = ("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])


# *******************************************************************
# CLASS
class SimpleUI:
    def __init__(self):
        # LOAD ui with absolute path
        self.wgUtil = QtCompat.loadUi(PATH_UI)

        # BUTTON
        self.wgUtil.btnAccept.clicked.connect(self.press_accept)
        self.wgUtil.btnHelp.clicked.connect(self.press_help)

        # SHOW the UI
        self.wgUtil.show()

    # ************************************************************
    # PRESS
    def press_accept(self):
        print("You accepted this process!")

    def press_help(self):
        webbrowser.open("https://www.alexanderrichtertd.com")


# *******************************************************************
# START
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    classVar = SimpleUI()
    app.exec_()
