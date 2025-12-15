"""
This script will basically act as the launcher for the application.

The purpose of this application is to be able to manage the user's computer and automate tasks.
"""
# Importing libraries
from PyQt5 import QtCore, QtWidgets, QtGui
import yaml, sys, requests, subprocess, os

# Import scripts
from src import main as maingui
from src import commons

# Paths
realpath = os.path.realpath(__file__)
dir_path = os.path.dirname(realpath)

# Variables
init_functions = [
    
]

# Starting up
def main():
    # Initialize pre-launch functions
    for fnc in init_functions:
        fnc = fnc()
        
        if fnc.check_init():
            fnc.run() # Will return any potential errors
        else:
            continue
    
    app = QtWidgets.QApplication.instance()

    # check apps
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    else:
        msg = QtWidgets.QMessageBox()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        msg.setWindowIcon(icon)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Another instance of the application is running!")
        msg.setWindowTitle("Error!") 
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes)
    
    # Startup the application
    app.setQuitOnLastWindowClosed(False)
    window = maingui.App(app)
    sys.exit(app.exec_())
    
# Functions
def getVerFromTag(tag):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    
    version = ""
    for character in tag:
        if numbers.__contains__(character):
            version += character
        if character == "c" or character == "s":
            break
            
    return float(version)

def getUpdateWithVersion(version, updates_array):
    for update in updates_array:
        up_version = getVerFromTag(update[0])
        
        if up_version == version:
            return update

def getLastestVersion(array):
    """
    This function basically finds the highest number in an array
    """
    
    latest = 0
    for version, release in array:
        version = getVerFromTag(version)
        
        if version > latest:
            latest = version
            
    return latest
    

if __name__ == "__main__":
    main()