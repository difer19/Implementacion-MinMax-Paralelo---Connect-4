import math
import multiprocessing
import time
from DTO.settingsDTO import SettingsDTO

settings = SettingsDTO()
depht_value = settings.json_dict['depht']

def max_value(state, depht_current, max_depht):
    if state.isFinal() or state.depht > (depht_current + depht_value):
        return state.value
    best = -math.inf
    for successor in state.generate_successors("X"):
        best = max(best, min_value(successor, depht_current, max_depht))
    return best

def min_value(state, depht_current, max_depht):
    if state.isFinal() or state.depht > (depht_current + depht_value):
        return state.value
    best = math.inf
    for successor in state.generate_successors("O"):
        best = min(best, max_value(successor, depht_current, max_depht))
    return best

def parallel_MinMax(state, type):
    start = time.time()

    settings = SettingsDTO()
    depht_value = settings.json_dict['depht']
    print("depht_current :" + str(depht_value))

    pool = multiprocessing.Pool()
    successors = state.generate_successors(state.next)

    results = []
    for successor in successors:
        if type == "max":
            results.append(pool.apply_async(min_value, (successor, state.depht, depht_value, )))
        elif type == "min":
            results.append(pool.apply_async(max_value, (successor, state.depht, depht_value, )))
        
    pool.close()
    pool.join()

    if type == "max":
        best_value = -math.inf
        best_state = None
        for i, result in enumerate(results):
            value = result.get()
            if value > best_value:
                best_value = value
                best_state = successors[i]
        fin = time.time()
        print(fin-start)
        return best_state

    elif type == "min":
        worst_value = math.inf
        worst_state = None
        for i, result in enumerate(results):
            value = result.get()
            if value < worst_value:
                worst_value = value
                worst_state = successors[i]
        fin = time.time()
        print(fin-start)
        return worst_state