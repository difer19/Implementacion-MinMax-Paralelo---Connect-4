from PyQt6.QtWidgets import *
from PyQt6 import uic
from DTO.settingsDTO import SettingsDTO

class SettingsWindow(QWidget):
    def __init__(self, parent = None):
        super(SettingsWindow, self).__init__(parent)
        self.startGUI()
        
    def startGUI(self):
        uic.loadUi(r'View/UI/Settings.ui', self)

        self.HumanRB = self.findChild(QRadioButton, 'human')
        self.MachineRB = self.findChild(QRadioButton, 'machine')
        self.minmaxOr = self.findChild(QRadioButton, 'mm_original')
        self.mm_parallel1 = self.findChild(QRadioButton, 'mm_parallel1')
        self.mm_parallel2 = self.findChild(QRadioButton, 'mm_parallel2')
        self.depth_le = self.findChild(QLineEdit, 'dephtLe')
        self.save = self.findChild(QPushButton, 'save')

        self.charge_current_settings()

        self.save.clicked.connect(self.save_settings)

        self.show()
    
    def charge_current_settings(self):
        settings = SettingsDTO()

        print(settings.json_dict['initial'])

        if settings.json_dict['initial'] == 'H':
            self.HumanRB.setChecked(True)
        else:
            self.MachineRB.setChecked(True)

        if settings.json_dict['algorithm'] == 'Original MinMax':
            self.minmaxOr.setChecked(True)
        elif settings.json_dict['algorithm'] == 'Parallel MinMax Ver 1':
            self.mm_parallel1.setChecked(True)
        elif settings.json_dict['algorithm'] == 'Parallel MinMax Ver 2':
            self.mm_parallel2.setChecked(True)

        self.depth_le.setText(str(settings.json_dict['depht']))

    def save_settings(self):
        try:
            initial = ""
            algorithm = ""
            depht = ""

            if self.HumanRB.isChecked() == True:
                initial = "H"
            else:
                initial = "M"
            
            if self.minmaxOr.isChecked() == True:
                algorithm = "Original MinMax"
            elif self.mm_parallel1.isChecked() == True: 
                algorithm = "Parallel MinMax Ver 1"
            elif self.mm_parallel2.isChecked() == True: 
                algorithm = "Parallel MinMax Ver 2"
            
            depht = int(self.depth_le.text())

            settings = SettingsDTO()
            settings.modified_json(initial, algorithm, depht)

            exito = QMessageBox()
            exito.setIcon(QMessageBox.Icon.Information)
            exito.setWindowTitle("Success")
            exito.setText("Settings Saved")
            exito.setStandardButtons(QMessageBox.StandardButton.Ok)

            exito.setStyleSheet("""
                                    QMessageBox {
                                        background-color: white;
                                        font-size: 18px;
                                    }
                                    
                                    QPushButton{
                                        color: white;
                                        background-color: #1A4A8B;
                                        border-radius: 15px;
                                        font: 14pt;
                                        padding: 10px;
                                    }
                                    
                                    QPushButton:hover {
                                        background-color: darkblue;
                                    }
                                """)

            exito.exec()

        except ValueError:
            alerta = QMessageBox()
            alerta.setIcon(QMessageBox.Icon.Warning)
            alerta.setWindowTitle("Fail")
            alerta.setText("Invalid Data Type")
            alerta.setStandardButtons(QMessageBox.StandardButton.Ok)

            alerta.setStyleSheet("""
                                    QMessageBox {
                                        background-color: white;
                                        font-size: 18px;
                                    }
                                    
                                    QPushButton{
                                        color: white;
                                        background-color: #1A4A8B;
                                        border-radius: 15px;
                                        font: 14pt;
                                        padding: 10px;
                                    }
                                    
                                    QPushButton:hover {
                                        background-color: darkblue;
                                    }
                                """)
            
            alerta.exec()
        

