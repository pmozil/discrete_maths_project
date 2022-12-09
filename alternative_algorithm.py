import random as r
from typing import Dict, Tuple, List
from io import StringIO

def rg(path):
    gr = {}
    with open(path, 'r') as infile:
        quints = map(lambda x: tuple(map(int, x)), [line.split(',') for line in infile.readlines()])
        for obj in quints:
            if (obj[0], obj[2]) in gr:
                gr[(obj[0], obj[2])].add((obj[1], obj[3]))
            else:
                gr[(obj[0], obj[2])] = {(obj[1], obj[3])}
            if (obj[1], obj[3]) in gr:
                gr[(obj[1], obj[3])].add((obj[0], obj[2]))
            else:
                gr[(obj[1], obj[3])] = {(obj[0], obj[2])}
    return gr

def _least_colour(
        colours: List[int]
) -> int:
    """
    Get the smallest int (colour) thaat is not adjacent to given vertice

    Args:
        graph: Dict[Tuple[int], List[Tuple[int]] - the graph
        vertice: Tuple[int] - thr vertice

    Returns:
        int - the smallest colour
    """
    col = 0
    while col in colours:
        col += 1
    return col
    

def _colouring(
    graph: Dict[int, List[int]],
    colours: Dict[int, int],
    numbering: List[int]
) -> Tuple[Dict[Tuple[int], List[Tuple[int]]], int]:
    """
    Greedy colouring of a given graph

    Args:
        graph: Dict[Tuple[int], int] - a weighted adjacency list
        path: List[int] - a sequence of vertices
        slow: bool - whether to use 2^32 as a fallback length or 2^64

    Returns:
        int - the length of a path
    """
    max_col = 0
    for node in numbering:
        cols = [colours[nd] for nd in graph[node]] + [colours[node]]
        colours[node] = _least_colour(cols)
        max_col = max(max_col, colours[node])
    return {
        (node, colours[node]):
            [
                (el, colours[el]) for el in graph[node]
            ] for node in numbering
        }, max_col



def _mutate_genome(path: List[int], mutations: int = 1) -> List[int]:
    """
    Mutate a genome, in our case a path

    Args:
        path: List[int] - a path
        mutations: int - the number of mutations

    Returns:
        List[int] - a new path
    """
    length = len(path) - 1
    for _ in range(mutations):
        coord1 = r.randint(0, length)
        while (coord2 := r.randint(0, length)) == coord1:
            pass
        path[coord1], path[coord2] = path[coord2], path[coord1]
    return path


def _gen_rand_numbering(length: int) -> List[int]:
    """
    Generate a random path for _TSP_genetic_memo and _TSP_genetic

    Args:
        n: int - number of vertices

    Returns:
        List[int] - a random path
    """
    return r.sample(list(range(0, length)), length)


def _colouring_genetic_with_memo(
    graph: Dict[Tuple[int], List[Tuple[int]]]
) -> List[Tuple[Dict[Tuple[int], List[Tuple[int]]], int]]:
    """
    Perform a genetic graph colouring optimisation algorithm on a given graph, with memoisation

    Args:
        graph: Dict[Tuple[int], List[Tuple[int]] - a coloured graph

    Returns:
        Tuple[Tuple[List[int], int]] - a (somewhat) optimised colouring of a graph
    """
    base_graph = {}
    colours = {}
    for node, els in graph.items():
        base_graph[node[0]] = [el[0] for el in els]
        colours[node[0]] = node[1]
    length = len(colours)
    colourings = {}

    iters = 0
    while iters < 32:
        numbering = tuple(_gen_rand_numbering(length))
        # Tuples here, gotta have sets
        colourings[numbering] = _colouring(base_graph, colours, numbering)
        iters += 1
    
    for _ in range(16):
        new_colourings = {}
        for numbering in colourings:
            new_numbering = tuple(_mutate_genome(list(numbering)))
            if new_numbering not in colourings:
                new_colourings[new_numbering] = _colouring(base_graph, colours, new_numbering)

        for cols, el in new_colourings.items():
            colourings[cols] = el

    return list(sorted(colourings.items(), key=lambda x: x[1][1]))[:5]

def _colouring_genetic(
    graph: Dict[Tuple[int], List[Tuple[int]]]
) -> List[Tuple[Dict[Tuple[int], List[Tuple[int]]], int]]:
    """
    Perform a genetic graph colouring optimisation algorithm on a given graph

    Args:
        graph: Dict[Tuple[int], List[Tuple[int]] - a coloured graph

    Returns:
        Tuple[Tuple[List[int], int]] - a (somewhat) optimised colouring of a graph
    """
    base_graph = {}
    colours = {}
    for node, els in graph.items():
        base_graph[node[0]] = [el[0] for el in els]
        colours[node[0]] = node[1]
    length = len(colours)
    colourings = []

    iters = 0
    while iters < 32:
        numbering = tuple(_gen_rand_numbering(length))
        col_graph, max_cols = _colouring(base_graph, colours, numbering)
        for ind, struct in enumerate(colourings):
            if max_cols < struct[1][1]:
                colourings.insert(ind, (numbering, (col_graph, max_cols)))
                break
        else:
            colourings.append((numbering, (col_graph, max_cols)))
        iters += 1
    
    for _ in range(32):
        new_colourings = []
        for numbering in colourings:
            new_numbering = tuple(_mutate_genome(list(numbering)))
            for ind, struct in enumerate(colourings):
                if max_cols < struct[1][1]:
                    colourings.insert(ind, (numbering, (col_graph, max_cols)))
                    break
        else:
            colourings.append((numbering, (col_graph, max_cols)))

        for cols, el in new_colourings:
            for ind, struct in enumerate(colourings):
                if el[1] < struct[1][1]:
                    colourings.insert(ind, (cols, el))
                    break
        colourings = colourings[:32]

    return list(sorted(colourings, key=lambda x: x[1][1]))[0]
