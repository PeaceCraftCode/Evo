from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QSlider, QLabel, QMessageBox, QLineEdit
import PyQt5
from json import load
import os.path
import time

def split_at_caps(string):
    out = []
    jnr = ''
    for i in string:
        if i.upper() == i and jnr != '':
            out.append(jnr)
            jnr = i
        else:
            jnr += i
    out.append(jnr)
    return out

class CONFIG:
    def check_quit(self): #check if all the options are valid
        if self.configDict['PercentHerbivore'] + self.configDict['PercentCarnivore'] + self.configDict['PercentOmnivore'] != 100:
            msg = QMessageBox(QMessageBox.Information,'Error!','Your herbivore, omnivore, and carnivore percentages must sum to 100.')
        elif self.configDict['SpeciesUpperCap'] <= self.configDict['SpeciesLowerCap']:
            msg = QMessageBox(QMessageBox.Information,'Error!','Your Species Upper Cap must be greater than your Species Lower Cap.')
        else:
            msg = QMessageBox.question(self.window, 'Confirm', "Are you sure you want to finish configuration? If the name you specified already exists, you will overwrite that save!", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if msg == QMessageBox.Yes:
                self.app.quit()
            return
        msg.show()
        msg.exec()
        


    def showFileDialog(self): #function to show file selector
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.window,"Evo Configuration - Select JSON Save File", "configs","JSON Files (*.json)", options=options)
        try:
            with open(fileName,'r') as fp:
                self.configDict = load(fp)
                self.check_quit()
        except OSError:
            pass

    def create_slider_func(self,name): #create dynamic function to connect to slider change event
        def _f():
            p = self.configSliderDict[name].sliderPosition()
            self.labelDict[name].setText(' '.join(split_at_caps(name)) + ' = ' + str(p))
            self.configDict[name] = p
        return _f

    def setWorldName(self,text):
        self.configDict['Name'] = text

    def __init__(self):
        self.configDict = { #set default values for config
            'SpeciesAmount':10,
            'PercentHerbivore':70,
            'PercentOmnivore':10,
            'PercentCarnivore':20,
            'SpeciesUpperCap':11,
            'SpeciesLowerCap':10,
            'PlantChanceCoefficient':100,
            'WaterPercent':50,
            'TreeMaxHeight':10
        }
        sliderSettings = { #set default values for config
            'SpeciesAmount':[2,50],
            'PercentHerbivore':[0,100],
            'PercentOmnivore':[0,100],
            'PercentCarnivore':[0,100],
            'SpeciesUpperCap':[4,70],
            'SpeciesLowerCap':[2,50],
            'PlantChanceCoefficient':[0,100],
            'WaterPercent':[0,100],
            'TreeMaxHeight':[2,7]
        }
        self.app = QApplication([]) #create application
        self.window = QWidget() #make a window
        self.window.setWindowTitle('Evo Configuration')
        self.window.setWindowIcon(PyQt5.QtGui.QIcon(os.path.join('Assets','Evo.png')))
        self.primLayout = QVBoxLayout() #General layout

        self.fileButton = QPushButton('Open saved config JSON') # Add load button
        self.fileButton.clicked.connect(self.showFileDialog) # Set callback
        self.primLayout.addWidget(self.fileButton) # Add to layout

        self.configSliderDict = {} #make dict of sliders
        self.labelDict = {} #make dict of slider labels
        for cfg in self.configDict.keys(): #loop thru all config opts
            self.configSliderDict[cfg] = QSlider(PyQt5.QtCore.Qt.Horizontal) #set a bunch of options VVV
            self.configSliderDict[cfg].setMaximum(sliderSettings[cfg][1])
            self.configSliderDict[cfg].setMinimum(sliderSettings[cfg][0])
            self.configSliderDict[cfg].setSliderPosition(self.configDict[cfg])
            self.configSliderDict[cfg].setTracking(True)
            self.configSliderDict[cfg].valueChanged.connect(self.create_slider_func(cfg)) #make dynamic callback
            self.labelDict[cfg] = QLabel(' '.join(split_at_caps(cfg)) + ' = ' + str(self.configDict[cfg]))
            self.primLayout.addWidget(self.labelDict[cfg]) # add the label
            self.primLayout.addWidget(self.configSliderDict[cfg]) # add the slider

        self.configDict['Name'] = time.strftime('%m-%d-%Y:%H:%M:%S') #Specify name
        self.primLayout.addWidget(QLabel('Save Name:'))
        self.enterName = QLineEdit()
        self.enterName.setPlaceholderText(time.strftime('%m-%d-%Y:%H:%M:%S'))
        self.enterName.textChanged.connect(self.setWorldName)
        self.primLayout.addWidget(self.enterName)

        self.finishButton = QPushButton('Finish Configuration') # Add finish button
        self.finishButton.clicked.connect(self.check_quit) # Quit if pressed
        self.primLayout.addWidget(self.finishButton) # Add to layout

        self.window.setLayout(self.primLayout) #set primLayout as the window's top layout
        self.window.show() #show the window
        self.app.exec_() #run the app