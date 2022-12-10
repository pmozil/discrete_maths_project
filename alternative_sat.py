"""
2-SAT solution for the graph 3-colouring problem
"""

from typing import Callable, Dict, Tuple, List

def form_sats(
    graph: Dict[int, List[int]],
    nodes: List[bool]
) -> bool:
    """
    Perform a conjunctive normal formula on a graph and it's colour representation
    Args:
        graph: Dict[int, List[int]] - a dictionary.
            Basically an unsparsed adjacency matrix
        nodes: List[bool] - list of booleans.
            Those are triplets, that show colour.
            Only one of the triplets should be True.
            The list's length should be 3*n,
            where n is the number of vertices
            Example:
                [False, False, True, True, False, False] shows a graph,
                that has (0, 2) and (1, 0) (2nd number is the colour
    Returns:
        bool - whether the graph edge colouring is valid
    """
    # nodes = {node: [False, False, False] for node in graph}
    # print(nodes)
    for node, items in graph.items():
        node_col = nodes[(node*3):(node*3 + 3)].count(True) == 1
        # for y in items:
            # for i in range(3):
                # print(f"{(node*3 + i, y*3 + i)}: {not (nodes[node*3 + i] and nodes[y*3 + i])}")
        no_neighbours = all(
            not (nodes[node*3 + i] and nodes[y*3 + i])
                for y in items
                for i in range(3)
            )
        if not (node_col and no_neighbours):
            return False
    return return True
