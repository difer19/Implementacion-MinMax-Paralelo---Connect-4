import math
import time
from DTO.settingsDTO import SettingsDTO



def desicion_minimax_max(state):
    settings = SettingsDTO()
    depht_value = settings.json_dict['depht']   
    print("depht_current :" + str(depht_value))

    start = time.time()
    maxv = -math.inf
    best_state = None
    for successor in state.generate_successors(state.next):
        value = min_value(successor, state.depht, depht_value)
        if value > maxv:
            maxv = value
            best_state = successor
    end = time.time()
    print(end-start)

    return best_state

def decision_minimax_min(estado):
    settings = SettingsDTO()
    depht_value = settings.json_dict['depht']   
    print("depht_current :" + str(depht_value))

    start = time.time()
    minv = math.inf
    best_state = None
    for successor in estado.generate_successors(estado.next):
        value = max_value(successor, estado.depht, depht_value)
        if value < minv:
            minv = value
            best_state = successor
    end = time.time()
    print(end-start)

    return best_state

def max_value(state, depht_current, depht_value):
    if state.isFinal() or state.depht > (depht_current + depht_value):
        return state.value
    maxv = -math.inf
    for successor in state.generate_successors("X"):
        maxv = max(maxv, min_value(successor, depht_current, depht_value))
    return maxv

def min_value(state, depht_current, depht_value):
    if state.isFinal() or state.depht > (depht_current + depht_value):
        return state.value
    minv = math.inf
    for successor in state.generate_successors("O"):
        minv = min(minv, max_value(successor, depht_current, depht_value))
    return minv

# def valor_estado_max(estado):
#     return max_valor(estado, estado.depht)

# def valor_estado_min(estado):
#     return min_valor(estado, estado.depht)