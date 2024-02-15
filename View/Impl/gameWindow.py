# libs
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from DTO.estadoDTO import stateDTO
from DTO.settingsDTO import SettingsDTO
from MinMax.minmax_original import *
from MinMax.parallel_minmax_ver1 import *
from MinMax.parallel_minmax_ver2 import *
from Sounds.repr.sounds import *
import copy


class GameWindow(QWidget):
    def __init__(self, parent = None):
        super(GameWindow, self).__init__(parent)
        self.startGui()

        
    def startGui(self):
        uic.loadUi(r'View/UI/Game.ui', self)
        self.results_list = []

        self.charge_game_params()

        self.wid = self.findChild(QWidget, 'wid')
        self.grid = self.wid.findChild(QGridLayout, 'tablero')
        self.startButton = self.findChild(QPushButton, 'pushButton_2')
        self.restartButton = self.findChild(QPushButton, 'pushButton')

        self.board = [[None for _ in range(7)] for _ in range(7)]
        self.buttons = []

        for row in range(7):
            for col in range(7):
                if row == 0:
                    button = QPushButton()
                    button.setText(" ↓ ")
                    button.setStyleSheet("""
                                            QPushButton:Pressed
                                            {
                                                background-color: white;
                                            }
                                         """)
                    self.grid.addWidget(button, row, col)
                    self.buttons.append(button)
                else:
                    widget = QLabel(self)
                    self.grid.addWidget(widget, row, col)
                    self.board[row-1][col] = widget
                    self.charge_ficha(1, row-1, col)
        
        self.buttons[0].clicked.connect(lambda: self.human_movement(0, self.current_state.next))
        self.buttons[1].clicked.connect(lambda: self.human_movement(1, self.current_state.next))
        self.buttons[2].clicked.connect(lambda: self.human_movement(2, self.current_state.next))
        self.buttons[3].clicked.connect(lambda: self.human_movement(3, self.current_state.next))
        self.buttons[4].clicked.connect(lambda: self.human_movement(4, self.current_state.next))
        self.buttons[5].clicked.connect(lambda: self.human_movement(5, self.current_state.next))
        self.buttons[6].clicked.connect(lambda: self.human_movement(6, self.current_state.next))

        self.startButton.clicked.connect(self.start)
        self.restartButton.clicked.connect(self.restart)

        self.show()
    
    def charge_game_params(self):
        self.human_turn = -1
        self.status_game = 0
        self.current_state = stateDTO([
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."]
        ], "X", 0)
        

    def start(self):
        self.status_game = 1
        settings = SettingsDTO()
        if settings.json_dict['initial'] == "M":
            # Movimiento maquina
            self.human_turn = 0
            self.machine_movement(self.current_state.next)
        elif settings.json_dict['initial'] == "H":
            # Movimiento Humano
            self.human_turn = 1
        
        self.startButton.setEnabled(False)

    def restart(self):
        self.charge_game_params()
        self.charge_board(self.current_state)
        self.startButton.setEnabled(True)

    def charge_board(self, state):
        #play_mp3_move()
        for row in range (6):
            for col in range(7):
                if state.position[row][col] == "X":
                    self.charge_ficha(2, row, col)
                elif state.position[row][col] == "O":
                    self.charge_ficha(3, row, col)
                elif state.position[row][col] == ".":
                    self.charge_ficha(1, row, col)
    
    def charge_ficha(self, type, row, col):
        if type == 1: #Void
            image_path = r"View\Images\void_tab.png"
            pixmap = QPixmap(image_path)
            self.board[row][col].setPixmap(pixmap)
            self.board[row][col].setAlignment(Qt.AlignmentFlag.AlignCenter)
        if type == 2: # Amarillo
            image_path = r"View\Images\yellow_tab.png"
            pixmap = QPixmap(image_path)
            self.board[row][col].setPixmap(pixmap)
            self.board[row][col].setAlignment(Qt.AlignmentFlag.AlignCenter)
        if type == 3: # Rojo
            image_path = r"View\Images\red_tab.png"
            pixmap = QPixmap(image_path)
            self.board[row][col].setPixmap(pixmap)
            self.board[row][col].setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def human_movement(self, button_number, turn):
        if self.human_turn == 0 or self.status_game == 0: return

        new_position = copy.deepcopy(self.current_state.position)
        for fila in range(5, -1, -1):
            if new_position[fila][button_number] == ".":
                new_position[fila][button_number] = turn
                break
        
        self.current_state = stateDTO(new_position, "O" if turn == "X" else "X", self.current_state.depht + 1)
        
        self.charge_board(self.current_state)

        if self.current_state.isWin(turn):
            print("Winner : Human")
            self.show_win_message("H")
            self.status_game = 0
        elif self.current_state.isTie():
            self.show_win_message("E")
            self.status_game = 0
        else:
            self.human_turn = 0
            self.machine_movement(self.current_state.next)
    
    def machine_movement(self, turn):
        if self.status_game == 1 and self.human_turn == 0:
            settings = SettingsDTO()
            if settings.json_dict['initial'] == "M":
                if settings.json_dict['algorithm'] == "Original MinMax":
                    self.current_state = desicion_minimax_max(self.current_state)
                elif settings.json_dict['algorithm'] == "Parallel MinMax Ver 1":
                    self.current_state = parallel_MinMax(self.current_state, "max")
                elif settings.json_dict['algorithm'] == "Parallel MinMax Ver 2":
                    self.current_state = parallel_MinMax2(self.current_state, "max")
                    
            elif settings.json_dict['initial'] == "H":
                if settings.json_dict['algorithm'] == "Original MinMax":
                    self.current_state = decision_minimax_min(self.current_state)
                elif settings.json_dict['algorithm'] == "Parallel MinMax Ver 1":
                    self.current_state = parallel_MinMax(self.current_state, "min")
                elif settings.json_dict['algorithm'] == "Parallel MinMax Ver 2":
                    self.current_state = parallel_MinMax2(self.current_state, "min")
            
            self.charge_board(self.current_state)
            play_mp3_move()
            
            if self.current_state.isWin(turn):
                print("Winner : Machine")
                self.show_win_message("M")
                self.status_game = 0
                self.startButton.setEnabled(False)
            elif self.current_state.isTie():
                self.show_win_message("E")
                self.status_game = 0
                self.startButton.setEnabled(False)
            else:
                self.human_turn = 1
     
    
    def show_win_message(self, winner):
        success = QMessageBox()
        success.setIcon(QMessageBox.Icon.NoIcon)
        success.setWindowTitle("Finish game")

        message = ""
        if winner == "M":
            message = "The machine has won"
        elif winner == "H":
            message = "The human has won"
        elif winner == "E":
            message = "Tie"

        success.setText(message)

        success.setStandardButtons(QMessageBox.StandardButton.Ok)

        success.setStyleSheet("""
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

        success.exec()
    
    