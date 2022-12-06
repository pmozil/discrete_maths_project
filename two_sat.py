"""
The two-satisfiability problem,
used in a graph 3-colouring problem
"""

from itertools import Dict, Tuple, List

def read_csv(file_path: str) -> Dict[Tuple[int], List[Tuple[int]]]:
    """
    Reads a csv file and returns a graph, represented by
    a dictionary with a coloured vertice as key and a list of coloured vertices
    as objects

    Args:
        file_path: str - path to csv

    Returns:
        Dict[Tuple[int], List[Tuple[int]]] - a graph model
    """
    pass

def write_csv(file_path: str, graph: Dict[Tuple[int], List[Tuple[int]]]) -> None:
    """
    Writes dictionary with a coloured vertice as key and
    a list of coloured vertices as objects to a csv file

    Args:
        file_path: str - path to csv
        graph: Dict[Tuple[int], List[Tuple[int]]] - a graph model
    """
    pass

def colour_graph(
        graph: Dict[Tuple[int], List[Tuple[int]]]
        ) -> Dict[Tuple[int], List[Tuple[int]]]:
    """
    Parses a graph and returns either a proper coloured graph or nothing

    Args:
        graph: Dict[Tuple[int], List[Tuple[int]]] - a coloured graph

    Returns:
        Dict[Tuple[int], List[Tuple[int]]] - a coloured graph
    """
    pass
    pass
