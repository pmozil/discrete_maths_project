"""
The two-satisfiability problem,
used in a graph 3-colouring problem
"""

from typing import Dict, Tuple, List, Set, Iterator


def read_csv(path: str) -> Tuple[Dict[int, List[int]], Dict[int, int]]:
    """
    Read a graph from file

    Args:
        path: str path to file

    Returns:
        Tuple[Dict[int, List[int]], Dict[int, int]]: - the graph, and its vertice colours
    """

    graph = dict()
    colors = dict()
    with open(path, 'r', encoding = 'utf-8') as file:
        lst = file.read().replace(',', '').split('\n')[:-1]
    for elem in lst:
        if int(elem[0]) not in graph:
            graph[int(elem[0])] = []
        if int(elem[1]) not in graph:
            graph[int(elem[1])] = []
        graph[int(elem[0])].append(int(elem[1]))
        graph[int(elem[1])].append(int(elem[0]))
        colors[int(elem[0])] = int(elem[2])
        colors[int(elem[1])] = int(elem[3])
    return graph, colors


def write_csv(
    path: str, graph: Dict[int, List[int]], colours: List[Tuple[int]]
) -> None:
    """
    Write a graph with its colours to a file

    Args:
        path: str - the path to file
        graph: Dict[int, List[int]] - the graph
        colours: List[Tuple[int]] - the vertice colours
    """
    colours = dict(colours)
    written = set()
    with open(path, "w", encoding="utf-8") as outfile:
        for vertice, adjacent_list in graph.items():
            for adjacent in adjacent_list:
                if (vertice, adjacent) not in written and (
                    adjacent,
                    vertice,
                ) not in written:
                    outfile.write(
                        f"{vertice},{adjacent},{colours[vertice]},{colours[adjacent]}\n"
                    )
                    written.add((vertice, adjacent))

# We should've taken the Catalan numbers
def make_impl_graph(edges: Tuple[int, int]) -> Dict[int, List[int]]:
    """
    Make a directed implication graph from an undirected graph
    Args:
        edges: Tuple[int, int] - a pair of vertice literals (could be 1 or -1).
            should be off-by-1, because there should be -0 and +0
    Returns:
        bool - whether the graph edge colouring is valid
    x v y = !x -> y & !y -> x
    """
    res = {}
    for v1, v2 in edges:
        if -v1 not in res:
            res[-v1] = [v2]
        else:
            res[-v1].append(v2)
        if -v2 not in res:
            res[-v2] = [v1]
        else:
            res[-v2].append(v1)

    return {v: list(set(e)) for v, e in res.items()}


def dfs(
    grp: Dict[int, List[int]], cur: int, visited: Set[int], path: List[int]
) -> List[int]:
    """
    Perform dfs on graph

    Args:
        graph: a directed graph

    Returns:
        List[int] - the order of the nodes
    """
    if cur in visited:
        return

    graph = {vertice: sorted(edges) for vertice, edges in grp.items()}
    result = []
    stack = [cur]

    while stack:
        s = stack[-1]
        visited.add(s)
        if s not in path:
            path.append(s)
        if s in graph:
            graph[s] = list(filter(lambda x: x not in visited, graph[s]))
            if graph[s] != []:
                stack.append(graph[s][0])
                continue
        stack.remove(s)

    return path


def invert_graph(graph: Dict[int, List[int]]) -> Dict[int, List[int]]:
    """
    Invert the edges in a graph

    Args:
        graph: Dict[int, Lisst[int]] - a graph to be inverted

    Returns:
        Dict[int, List[int]] - an inverted graph
    """
    new_graph = {}
    for node, items in graph.items():
        for item in items:
            if item not in new_graph:
                new_graph[item] = [node]
            else:
                new_graph[item].append(node)
    return new_graph


def scc(graph: Dict[int, List[int]]) -> List[Set[int]]:
    """
    Perform Kosaraju's algorith on graph

    Args:
        graph: a idrected graph

    Returns:
        List[Set[int]] - a list of strongly connected components
    """
    visited = set()
    base_path = []
    for i in graph.keys():
        if i not in visited:
            dfs(graph, i, visited, base_path)

    graph_inv = invert_graph(graph)
    visited.clear()
    paths = []
    while len(base_path):
        node = base_path.pop()
        if node not in visited:
            path = dfs(graph_inv, node, visited, [])
            yield path[:]
            path.clear()
    return


def colour_graph(
    graph: Dict[int, List[int]],
    colours: Dict[int, int]
) -> List[Tuple[int]]:
    """
    Colour a graph with 2-SAT

    Args:
        graph: Dict[int, List[int]] - the graph
        colours: Dict[int, int]] - starting colours of vertices
    Returns:
        List[Tuple[int]] - list of pairs: a vertice and it's colour
    """
    graph = {(vertice+1)*3 : [(v+1)*3 for v in graph[vertice]] for vertice in graph}
    colours = {(vertice+1)*3: col for vertice, col in colours.items()}
    clauses = []
    for vertice in graph:
        col = colours[vertice]
        lst = list(filter(lambda x: x!=col, range(3)))
        clauses.append((vertice+lst[0], vertice+lst[1]))
        clauses.append((-vertice-lst[0], -vertice-lst[1]))
        for adjacent in graph[vertice]:
            for i in lst:
                if colours[adjacent] != adjacent+i and (-adjacent-i, -vertice-i) not in clauses:
                    clauses.append((-vertice-i, -adjacent-i))
    impl_graph = make_impl_graph(clauses)
    res = list(scc(impl_graph))
    colouring = {}
    nots = {}
    j = len(res) - 1
    while j>=0 and len(colouring) != len(graph):
        last = res[j]
        if all(-x not in last for x in last):
            while last != []:
                col = last.pop()
                if col > 0:
                    if abs(col)//3 not in nots or abs(col)%3 not in nots[abs(col)//3]:
                        colouring[abs(col)//3] = abs(col)%3
                elif abs(col)//3 not in nots:
                    nots[abs(col)//3] = [abs(col)%3, colours[3*(abs(col)//3)]]
        else:
            print("A vertice cannot be coloured!")
        j -= 1
    return sorted([(v-1, col) for v, col in colouring.items()], key=lambda x: x[0])
