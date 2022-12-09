from typing import Callable, Dict, Tuple, List

def form_sats(
    graph: Dict[int, List[int]]
) -> List[Callable[Dict[int, List[bool]]]]:
    # nodes = {node: [False, False, False] for node in graph}
    forms = []
    for node, items in graph.items():
        node_col = lambda nodes: len(filter(lambda x: x, nodes[node])) == 1
        no_neighbours = [
            lambda nodes: all(not (nodes[node][i] and nodes[y][i]))
                for i in range(3)
                for y in graph[node]
            ]
        forms.append(lambda nodes: node_col(nodes) and no_neighbours(nodes))
    return forms

def process_nodes(
    forms: List[Callable[Dict[int, List[bool]]]],
    nodes: Dict[int, [List[bool]]]
) -> bool:
    return all(form(nodes) for form in forms)
