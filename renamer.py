import Ui_renamer
import setstyle
import sys
import os
import fnmatch
import yaml

if getattr(sys, 'frozen', False):  # Do a check if running from frozen application or .py script
    from PySide2 import QtWidgets, QtCore, QtGui
else:
    try:
        from PyQt5 import QtWidgets, QtCore, QtGui
    except:
        print("PyQt5 not found, trying PySide2...")
        from Qt import QtWidgets, QtCore, QtGui

appversion = '0.1'
available_configs = {}

class MainWindow(QtWidgets.QMainWindow, Ui_renamer.Ui_MainWindow):
    def __init__(self):
        '''Construct MainWindow'''
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Overmind Studios Renamer " + appversion)
        self.statusbar.setSizeGripEnabled(False)
        self.setFixedSize(self.size())
        self.show()
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.parseConfigs()

    def parseConfigs(self):
        '''parse config files and populate fields'''
        global available_configs
        config_index = 0
        configlist = os.listdir('templates')
        for config in configlist:
            if fnmatch.fnmatch(config, '*.yml'):
                with open(os.path.join('templates', config), 'r') as stream:
                    try:
                        data = yaml.load(stream)
                        available_configs[config_index] = config
                        config_index += 1
                        self.comboBox.addItem(str('{0:03d}'.format(config_index)) + " - " + str(data.get('date')) + " - " + data.get('client') + " - " + data.get('project') + " - " + data.get('version'))
                        print(available_configs)
                    except yaml.YAMLError as exc:
                        print(exc)
    
    def on_combobox_changed(self, value):
        '''update settings according to config selection'''
        global available_configs
        with open(os.path.join('templates', available_configs[value]), 'r') as stream:
                    try:
                        data = yaml.load(stream)
                        self.statusbar.showMessage("Naming scheme: " + data.get('naming_scheme'))
                    except yaml.YAMLError as exc:
                        print(exc)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(setstyle.setPalette())
    window = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
