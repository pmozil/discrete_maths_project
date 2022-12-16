"""
2-SAT solution for the graph 3-colouring problem
"""

from typing import Dict, Tuple, List, Set, Iterator

# The function is redundant now, but it has sentimental value for me
# Should someone delete this, I'll remove their kneecaps with an ice cream scoop
def form_sats(graph: Dict[int, List[int]], nodes: List[bool]) -> bool:
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
        node_col = nodes[(node * 3) : (node * 3 + 3)].count(True) == 1
        # for y in items:
        # for i in range(3):
        # print(f"{(node*3 + i, y*3 + i)}: {not (nodes[node*3 + i] and nodes[y*3 + i])}")
        no_neighbours = all(
            not (nodes[node * 3 + i] and nodes[y * 3 + i])
            for y in items
            for i in range(3)
        )
        if not (node_col and no_neighbours):
            return False
    return True


# We should've taken the Catalan numbers
# This dfs is gonna get a hernia, the way it carries this algorithm
def dfs(
    grp: Dict[int, List[int]],
    cur: int,
    visited: Set[int],
    path: List[int],
    *_,
    cycles: List[List[int]] = None,
    colours: Dict[int, int] = None,
    back_edges: List[Tuple[int]] = None
) -> Tuple[List[int], List[List[int]], Dict[int, int], Dict[int, int]]:
    """
    Perform dfs on graph

    Args:
        grp: Dict[int, List[int]] - a directed graph
        cur: int - node to strt with
        visited: Set[int] - visitd edges
        path: List[int] - the path
        cycles: List[List[int]] - cycles array
        colours: List[Tuple[int]] - array of colours
        back_edges: List[Tuple[int]] - array of back edges

    Returns:
        Tuple[List[int], List[List[int]], Dict[int, int], Dict[int, int]] - ... yeah.
    """
    if cur in visited:
        return

    graph = {vertice: sorted(edges) for vertice, edges in grp.items()}
    result = []
    stack = [cur]
    base = 1

    while stack:
        s = stack[-1]
        visited.add(s)

        if s not in path:
            path.append(s)

        if isinstance(colours, dict) and s not in colours:
            base = 0 if base else 1
            colours[s] = base

        for node in graph.get(s):
            if node in path and isinstance(cycles, list):
                cycle = path[path.index(node) : path.index(s) + 1]
                if cycle not in cycles:
                    cycles.append(cycle)
            if neigh in visited:
                back_edges.append((s, neigh))
            if node not in visited:
                stack.append(node)

        stack.remove(s)

    return (path, cycles, colours, back_edges)


def get_cycle_intersections(
    odd_cycles: List[List[int]], even_cycles: List[List[int]]
) -> Iterator[List[int]]:
    """
    Get intersections in lists of cycles

    Args:
        odd_cycles: List[List[int]]
        even_cycles: List[List[int]]

    Returns:
        Iterator[List[int]] - a list of intersections
    """
    for ec in even_cycles:
        for oc in odd_cycles:
            for el in ec:
                if el in oc:
                    yield ec
                    break


def get_back_edges(
    cycles: List[List[int]], back_edges: List[Tuple[int]]
) -> Iterator[Tuple[int]]:
    """
    Get back edges for odd cycles

    Args:
        odd_cycles: List[List[int]] - the odd cycles
        back_edges: List[Tuple[int]] - the back edges

    Returns:
        Iterator[Tuple[int]] - a generator of back edges
    """
    for v1, v2 in back_edges.items():
        if any(v2 in x for x in cycles):
            yield (v1, v2)


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

    return res


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
            _ = dfs(graph, i, visited, base_path)

    graph_inv = invert_graph(graph)
    visited.clear()
    path = []
    while len(base_path):
        node = base_path.pop()
        if node not in visited:
            path, *_ = dfs(graph_inv, node, visited, [])
            yield path[:]
            path.clear()
    return


def colour_graph(graph: Dict[int, List[int]]) -> List[Tuple[int]]:
    """
    We're finally at the final step of solving the colouring problem.
    I started off really hating this problem, but it's growing on me.
    Maybe it's not that bad? Nah, it's probably stockholm syndrome.
    Anything related to graphs is just pure abomination algoritmified.
    Well, at least I won't have to suffer for long now. Cheers!

    Args:
        graph: Dict[int, List[int]] - the graph

    Returns:
        List[Tuple[int]] - list of pairs: a vertice and it's colour
    """
    path, cycles, dfs_tree_colours, back_edges = dfs(
        graph, 0, set(), [], colours={}, back_edges=[], cycles=[]
    )
    odd_cycles, even_cycles = []
    for cycles in cycles:
        if len(cycle) % 2:
            odd_cycles.append(cycle)
        else:
            even_cycles.append(cycle)
   inters = get_cycle_intersections(odd_cycles, even_cycles)
   back_edges = list(get_back_edges(odd_cycles, back_edges))
   # TODO: finish the function
   clauses = []
   return
