import math
import multiprocessing
import time
from DTO.settingsDTO import *

depht_current = 0

def parallel_MinMax2(state, type):
    start = time.time()

    settings = SettingsDTO()
    depht_value = settings.json_dict['depht']
    max_depth = depht_value
    print("depht_current :" + str(depht_value))

    if type == "max":
        max_val = -math.inf
        for successor in state.generate_successors(state.next):
            val = min_value(successor, 1, max_depth)
            if val > max_val:
                max_val = val
                x = successor
    else:
        min_val = math.inf
        for successor in state.generate_successors(state.next):
            val = max_value(successor, 1, max_depth)
            if val < min_val:
                min_val = val
                x = successor

    end = time.time()
    print(end - start)
    return x

def max_value(state, depth, max_depth):
    if depth == max_depth or state.isFinal():
        return state.value
    
    max_val = -math.inf
    successors = state.generate_successors("X")
    
    if len(successors) < multiprocessing.cpu_count():
        results = [min_value(s, depth + 1, max_depth) for s in successors]
    else:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.starmap(min_value, [(s, depth + 1, max_depth) for s in successors])

    max_val = max(results)
    return max_val

def min_value(state, depth, max_depth):
    if depth == max_depth or state.isFinal():
        return state.value
    
    min_val = math.inf
    successors = state.generate_successors("O")
    
    if len(successors) < multiprocessing.cpu_count():
        results = [max_value(s, depth + 1, max_depth) for s in successors]
    else:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.starmap(max, [(s, depth + 1, max_depth) for s in successors])

    min_val = min(results)
    return min_val