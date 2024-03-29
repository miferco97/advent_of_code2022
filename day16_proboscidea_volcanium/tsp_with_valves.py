import os
import sys
import itertools
from typing import List, Tuple, Union, Any, Dict

REMAINING_TIME = 30

class Node():
    def __init__(self, name, valve_value, connections, graph, parent=None):
        self.name = name
        self.value = valve_value
        self.valve_is_opened = False
        self.parent = parent
        self.connections = connections

    def __repr__(self) -> str:
        opened = 'opened' if self.valve_is_opened else 'closed'
        return f'{self.name}: valve  with values {self.value} is {opened} -> connects to {self.connections}\n'

    def get_value_expected(self, remaining_time):
        # print(f'{remaining_time=}')
        return self.value*(remaining_time)

    def get_name(self):
        return self.name


def parse_graph(filename) -> Dict:
    graph = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            valve, tunnels = line.split(';')
            name = valve[6:8]
            valve_rate = int(valve[valve.find('=')+1:])
            tunnels = [x[:-1] if x[-1] ==
                       ',' else x for x in tunnels.strip().split(' ')[4:]]
            graph[name] = Node(name, valve_rate, tunnels, graph)

    return graph

def find_best_path(origin: str, dest: str, graph: Dict[str, Node]):
    visited = {}
    to_visit = [graph[origin]]
    costs = {origin: 0}
    node = None
    while to_visit:
        node = to_visit.pop(0)
        if node.name == dest:
            break
        for connection in graph[node.name].connections:
            if costs.get(connection) is None and visited.get(connection) is None:
                costs[connection] = costs[node.name] + 1
                to_visit.append(graph[connection])
                to_visit[-1].parent = graph[node.name]
        to_visit.sort(key=lambda x: costs[x.name])
    parent = node.parent
    path = [node.name]
    while parent is not None:
        path.append(parent.name)
        parent = parent.parent
    return path[::-1]


# def compute_expected_presure_release(final_path, orig, elaped_time: int, elapsed_valves: List, graph):
#     if len(elapsed_valves) == 1:
#         return graph[elapsed_valves[0]]
#     for valve in elapsed_valves:
#         pass

RECUR_END=0
def find_best_combination(starting_node:str, _elapsed_time:int,accum_preasure_released:int, graph:Dict[str,Node], _open_valves:List[str],came_from=None,has_opened=False)->int:
    childs=graph[starting_node].connections.copy()
    elapsed_time = _elapsed_time+1
    open_valves=_open_valves.copy()
    max_value = accum_preasure_released
    if elapsed_time >= REMAINING_TIME or len(graph.keys()) == len(_open_valves):
        global RECUR_END
        RECUR_END+=1
        print(f'break time {RECUR_END}')
        return 0
    if starting_node not in open_valves and graph[starting_node].value != 0:
        childs.append('open')
    if not has_opened and came_from is not None:
        childs.remove(came_from)
    for possibility in childs:
        preasure_released = accum_preasure_released
        if possibility == 'open':
            open_valves.append(starting_node)
            preasure_released += graph[starting_node].get_value_expected(REMAINING_TIME-elapsed_time) 
            preasure_released += find_best_combination(starting_node,elapsed_time,preasure_released,graph,open_valves,has_opened=True)
        else:
            preasure_released += find_best_combination(possibility,elapsed_time,preasure_released,graph,open_valves,came_from=starting_node,has_opened=False)
        if preasure_released > max_value:
            max_value = preasure_released
            # print(starting_node)
    return max_value


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    visualize = False
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)
    graph = parse_graph(input_file)
    print(graph)
    closed_valves = []
    for key, value in graph.items():
        if value.value != 0:
            closed_valves.append(key)
    # return pressure
    # for depth in range(len(closed_valves)):
    #     path = find_best_path(orig, depth[closed_valves])
    # possibilities = itertools.permutations(closed_valves, 5)
    # print([x for x in possibilities])
    max_value = find_best_combination('AA',0,0,graph,[])
    print(max_value)
