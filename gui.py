from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
import PyQt5
from json import load

class CONFIG:
    def showFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.window,"Select JSON Save File", "","JSON Files (*.json)", options=options)
        with open(fileName,'r') as fp:
            self.configDict = load(fp)
        print(self.configDict)

    def __init__(self):
        self.configDict = {}
        self.app = QApplication([]) #create application
        self.window = QWidget() #make a window
        self.window.setWindowTitle('Evo Configuration')
        self.primLayout = QVBoxLayout() #General layout
        self.fileButton = QPushButton('Open saved config JSON')
        self.fileButton.clicked.connect(self.showFileDialog)
        self.primLayout.addWidget(self.fileButton)
        self.window.setLayout(self.primLayout) #set primLayout as the window's top layout
        self.window.show() #show the window
        self.app.exec_() #run the app
        
        print(self.configDict)
    
CONFIG()