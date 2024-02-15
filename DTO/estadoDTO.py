import copy


class stateDTO:
    def __init__(self, position, next, depht):
            self.position = position
            self.next = next
            self.depht = depht
            self.value = self.evaluation()
        
    def print_board(self):
        guide = ["1", "2", "3", "4", "5", "6", "7"]
        print(guide)
        print("")
        for row in self.position:
            print(row)
    
    def isWin(self, turn):
        for horizontal in self.position:
            counter = 0
            for i in horizontal:
                if i == turn:
                    counter += 1
                else:
                    counter = 0
                
                if counter == 4:
                    return True
        
        for column in range(7):
            counter = 0
            for row in range(6):
                if self.position[row][column] == turn:
                    counter += 1
                else:
                    counter = 0
                
                if counter == 4:
                    return True
        
        for diagonal in self.get_diagonals():
            if diagonal == ["O", "O", "O", "O"] and turn == "O":
                return True
            elif diagonal == ["X", "X", "X", "X"] and turn == "X":
                return True
        
        return False 
        
    def isTie(self):
        for row in self.position:
            for data in row:
                if data == ".":
                    return False
        return True

    def isFinal(self):
        return self.isTie() or self.isWin("X") or self.isWin("O")
    
    def get_verticals(self):
        verticals = []
        for column in range(7):
            vertical = [self.position[row][column] for row in range(6)]
            verticals.append(vertical)
        return verticals

    def get_diagonals(self):
        diagonals = []
        for row in range(len(self.position) - 3):
            for column in range(len(self.position[0]) - 3):
                diagonal = [self.position[row + i][column + i] for i in range(4)]
                diagonals.append(diagonal)

        for row in range(len(self.position) - 3):
            for column in range(3, len(self.position[0])):
                diagonal = [self.position[row + i][column - i] for i in range(4)]
                diagonals.append(diagonal)

        return diagonals
    
    def evaluation(self):
        state_value = 0

        # horizontals
        for horizontal in self.position:
            for i in range(0, 3):
                valid_row = [horizontal[i], horizontal[i+1], horizontal[i+2], horizontal[i+3]]
                state_value += self.count_groups(valid_row, "X") - 2*self.count_groups(valid_row, "O")

        # Verticals
        for vertical in self.get_verticals():
            for i in range(0, 2):
                valid_row = [vertical[i], vertical[i+1], vertical[i+2], vertical[i+3]]
                state_value += self.count_groups(valid_row, "X") - 2*self.count_groups(valid_row, "O")

        # Diagonales
        for diagonal in self.get_diagonals():
            state_value += self.count_groups(diagonal, "X") - 2*self.count_groups(diagonal, "O")

        # Nuevas opciones de mejora
        # valor_estado += self.evaluar_centro()  # Mejora 1: Evaluar el control del centro del tablero
        # valor_estado += self.evaluar_fichas_cercanas()  # Mejora 2: Evaluar la formación de fichas cercanas
        # valor_estado += self.evaluar_patrones_estrategicos()  # Mejora 3: Evaluar patrones estratégicos

        state_value += self.evaluar_centro()

        if self.isWin("O"):
            state_value -= 1000
        elif self.isWin("X"):
            state_value += 500 

        return state_value

    def count_groups(self, row, player):
        counter = 0
        group = 0
        for i in range(len(row)):
            if row[i] == player:
                group += 1
            else:
                counter += group // 4
                group = 0
        counter += group // 4
        return counter
    
    def evaluar_centro(self):
        center_control_X = 0
        center_control_O = 0
        for col in range(7):
            for row in range(2, 5):
                if self.position[row][col] == "X":
                    center_control_X += 1
                elif self.position[row][col] == "O":
                    center_control_O += 1

        return (center_control_X - center_control_O)

    
    def generate_successors(self, turn):
        successors = []
        for column in range(7):
            if self.position[0][column] == ".":
                new_position = copy.deepcopy(self.position)
                for row in range(5, -1, -1):
                    if new_position[row][column] == ".":
                        new_position[row][column] = turn
                        break
                successor = stateDTO(new_position, "O" if turn == "X" else "X", self.depht + 1)
                successors.append(successor)
        return successors  