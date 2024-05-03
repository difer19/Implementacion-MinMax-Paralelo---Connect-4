import copy
import math
import time
from DTO.estadoDTO import stateDTO
from MinMax.minmax_original import *
from MinMax.parallel_minmax_ver1 import *
from MinMax.parallel_minmax_ver2 import *
from DTO.settingsDTO import SettingsDTO

class Game:
    def __init__(self, start_machine, player):
        self.state = stateDTO([
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."], 
            [".", ".", ".", ".", ".", ".", "."]
        ], "X", 0)

        if start_machine:
            self.start_game("M", player)
        else:
            self.start_game("H", player)
    
    def start_game(self, initial, player):
        turn = player
        if turn == "X": 
            turn_2 = "O"
        else: 
            turn_2 = "X"

        settings = SettingsDTO()

        if initial == "M":
            while not self.state.isFinal():
                self.state.print_board()
                print("------------------")
                if turn == player:
                    if settings.json_dict['algorithm'] == "Original MinMax":
                        self.state = desicion_minimax_max(self.state)
                    elif settings.json_dict['algorithm'] == "Parallel MinMax Ver 1":
                        self.state = parallel_MinMax(self.state, "max")
                    elif settings.json_dict['algorithm'] == "Parallel MinMax Ver 2":
                        self.state = parallel_MinMax2(self.state, "max")
                    turn = turn_2
                else:
                    self.state = self.human_player(turn_2)
                    turn = player

            print("------------------")
            self.state.print_board()

            if self.state.isWin(player):
                print("------------------")
                print("Machine Win: " + player)
            elif self.state.isWin(turn_2):
                print("Human Win : " + turn_2)
            else:
                print("Tie")
        else:
            while not self.state.isFinal():
                self.state.print_board()
                print("------------------")
                if turn == player:
                    self.state = self.human_player(player)
                    turn = turn_2
                else:
                    if settings.json_dict['algorithm'] == "Original MinMax":
                        self.state = decision_minimax_min(self.state)
                    elif settings.json_dict['algorithm'] == "Parallel MinMax Ver 1":
                        self.state = parallel_MinMax(self.state, "min")
                    elif settings.json_dict['algorithm'] == "Parallel MinMax Ver 2":
                        self.state = parallel_MinMax2(self.state, "min")
                    turn = player

            print("------------------")
            self.state.print_board()
            print("------------------")

            if self.state.isWin(player):
                print("Humano Win: " + player)
            elif self.state.isWin(turn_2):
                print("Machine Win: " + turn_2)
            else:
                print("Tie")
    
    def human_player(self, turn):
        column = -1
        while column < 0 or column >= 7 or self.state.position[0][column] != ".":
            column = int(input("Enter the column (1-7): ")) - 1
        
        new_position = copy.deepcopy(self.state.position)
        for row in range(5, -1, -1):
            if new_position[row][column] == ".":
                new_position[row][column] = turn
                break
        
        return stateDTO(new_position, "O" if turn == "X" else "X", self.state.depht + 1)
      
if __name__ == "__main__":
    option = 0
    while option != 3:
        print("_______Game_________")
        print("1. The maquina start")
        print("2. The human start")
        print("3. Exit")
        print("---------------------")
        option = int(input("Option: "))
        if option == 1:
            game = Game(True, "X")
        elif option == 2:
            game = Game(False, "X")
        elif option == 3:
            print("Thanks for play")


