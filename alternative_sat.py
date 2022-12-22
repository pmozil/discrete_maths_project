"""
2-SAT solution for the graph 3-colouring problem
"""

from typing import Dict, Tuple, List, Set, Iterator


def read_graph(path: str) -> Tuple[Dict[int, List[int]], Dict[int, int]]:
    """
    Read a graph from file

    Args:
        path: str path to file

    Returns:
        Tuple[Dict[int, List[int]], Dict[int, int]]: - the graph, and its vertice colours
    """

    gr = {}
    cols = {}
    with open(path, "r", encoding="utf-8") as infile:
        quints = map(
            lambda x: tuple(map(int, x)),
            [line.split(",") for line in infile.readlines()],
        )
        for obj in quints:
            if obj[0] in gr:
                gr[obj[0]].add(obj[1])
            else:
                gr[obj[0]] = {obj[1]}
            if obj[1] in gr:
                gr[obj[1]].add(obj[0])
            else:
                gr[obj[1]] = {obj[0]}
            cols[obj[0]] = obj[2]
            cols[obj[1]] = obj[3]
    return {v: list(gr[v]) for v in gr}, cols


def write_graph(
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
    colours: Dict[int, int] = None,
    back_edges: List[Tuple[int]] = None,
) -> Tuple[List[int], List[List[int]], Dict[int, int], Dict[int, int]]:
    """
    Perform dfs on graph

    Args:
        grp: Dict[int, List[int]] - a directed graph
        cur: int - node to strt with
        visited: Set[int] - visitd edges
        path: List[int] - the path
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

        if s in graph:
            for node in reversed(graph.get(s)):
                if node in visited and isinstance(back_edges, list):
                    back_edges.append((s, node))
                if node not in visited:
                    stack.append(node)

        stack.remove(s)

    return (path, colours, back_edges)


def cycles_dfs(
    graph: Dict[int, List[int]], start: int, end: int
) -> Iterator[List[int]]:
    """
    Do a dfs on a graph

    Args:
        graph: Dict[int, List[int]] - a graph
        start: int - the start node
        end: int - the end node

    Returns:
        Iterator[List[int]] - the list of cycles
    """
    fringe = [(start, [])]
    while fringe:
        state, path = fringe.pop()
        if path and state == end:
            yield path
            continue
        if state in graph:
            for next_state in graph[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path + [next_state]))


def get_cycle_intersections(
        odd_cycles: List[List[int]], even_cycles: List[List[int]], * ,odds: bool=False
) -> List[List[int]]:
    """
    Get intersections in lists of cycles

    Args:
        odd_cycles: List[List[int]]
        even_cycles: List[List[int]]

    Returns:
        List[List[int]] - a list of intersections
    """
    res = []
    for ec in even_cycles:
        for oc in [x for x in odd_cycles if x != ec]:
            #if (
            #    oc[i] in ec
            #    and oc[i + 1] in ec
            #    and not all(x in ec for x in oc)
            #    and (len(oc) > 3 and len(ec) > 3)
            #):
            #    res.append(ec)
            if any(x in oc and all(y not in ecc for y in ec) for ecc in even_cycles for x in ecc):
                res.append(oc)
    return res


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
    for v1, v2 in back_edges:
        if any((v2 in x and v1 not in x) or (v1 in x and v2 not in x) for x in cycles):
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


def adjacent_edges(
    graph: Dict[int, List[int]], edges: List[Tuple[int]]
) -> List[Tuple[int]]:
    """
    Get edges that are adjacent.

    Args:
        graph: Dict[int, List[int]]
        edges: List[Tuple[int]] - the list of edges

    Returns:
        List[Tuple[int]] - list of pairs of vertices of those edges
    """
    res = []
    for v1, v2 in edges:
        for v_1, v_2 in edges:
            if v1 != v_1 or v2 != v_2:
                if v1 != v_1 and v1 in graph[v_1] and (v_1, v1) not in res:
                    res.append((v1, v_1))
                if v1 != v_2 and v1 in graph[v_2] and (v_2, v1) not in res:
                    res.append((v1, v_2))
                if v2 != v_1 and v2 in graph[v_1] and (v_1, v2) not in res:
                    res.append((v2, v_1))
                if v2 != v_2 and v2 in graph[v_2] and (v_2, v2) not in res:
                    res.append((v2, v_2))
    return res


def colour_graph(
    graph: Dict[int, List[int]]
) -> List[Tuple[int]]:
    """
        We're finally at the final step of solving the colouring problem.
        I started off really hating this problem, but it's growing on me.
        Maybe it's not that bad? Nah, it's probably stockholm syndrome.
        Anything related to graphs is just pure abomination algoritmified.
        Well, at least I won't have to suffer for long now. Cheers!
    import collections
        Args:
            graph: Dict[int, List[int]] - the graph

        Returns:
            List[Tuple[int]] - list of pairs: a vertice and it's colour
    """
    # This is just for comfort, won't be faster until the node count is like 10^5
    clauses = []
    graph = {v + 1: [ver + 1 for ver in graph[v]] for v in graph}
    _, dfs_tree_colours, back_edges = dfs(
        graph, 1, set(), [], colours={}, back_edges=[]
    )
    back_edges = list(set(back_edges))
    all_cycles = [
        tuple(path)
        for node in graph
        for path in cycles_dfs(graph, node, node)
        if len(path) > 2
    ]
    # This is neccesary, even though it eats like a ton of memory
    cycles = []
    set_cycles = []
    for cycle in all_cycles:
        if set(cycle) not in set_cycles:
            set_cycles.append(set(cycle))
            cycles.append(cycle)
    odd_cycles, even_cycles = [], []
    for cycle in cycles:
        if len(cycle) % 2:
            odd_cycles.append(cycle)
        else:
            even_cycles.append(cycle)
    odd_cycles = list(set(map(tuple, odd_cycles)))
    even_cycles = list(set(map(tuple, even_cycles)))
    inters = list(set(get_cycle_intersections(odd_cycles, even_cycles)))
    odd_inters = list(set(get_cycle_intersections(odd_cycles, odd_cycles)))
    if len(odd_inters) > 1:
        print("Odd cycles intersect. The 3-colouring might not exist >:-}")
    back_edges = set(get_back_edges(odd_cycles, back_edges))
    clauses.extend((-x, -y) for x, y in set(adjacent_edges(graph, back_edges)))
    clauses.extend((-x, -y) for x, y in back_edges)
    clauses.extend((-cycle[0], -cycle[-1]) for cycle in inters)
    clauses.extend((-cycle[0], -cycle[-1]) for cycle in odd_cycles)
    strongly_connected = list(scc(make_impl_graph(clauses)))
    print(strongly_connected)

    # We gonna check if the formula is satisfiable. If not, NOBODY CARES
    # I have a general distaste for graphs, especially this stupid case
    # Why not use backtracking or even just a forward-backward approach?

    # Get unique numbers from list, gotta have them all
    uniques = set()
    apologise = True
    cols = []

    for clause in reversed(strongly_connected):
        for lit in clause:
            # No solution for CNF, so we can do nothing. The good ending
            uniques.add(abs(lit))
            if -lit in clause and apologise:
                apologise = False
                print(
                    "The 2-CNF might be unsatisfiable. The graph's colouring might not work"
                )
                #return [(v - 1, e) for v, e in dfs_tree_colours.items()]

    # Not that much a 2-SAT, but more of a hack. Too bad!
    j = len(strongly_connected) - 1
    while len(cols) < len(uniques) and j >= 0:
        if all(x not in cols and -x not in cols for x in strongly_connected[j]):
            cols.extend(strongly_connected[j])
            new = strongly_connected[j]
            new = sorted(new, key=lambda x: len(graph[abs(x)]))
            while new != []:
                el = new.pop()
                if all(dfs_tree_colours[x] != 2 for x in graph[abs(el)]):
                    if any(dfs_tree_colours[x] == dfs_tree_colours[abs(el)] for x in graph[abs(el)]):
                        dfs_tree_colours[abs(el)] = 2
        j -= 1

    return [(v - 1, e) for v, e in dfs_tree_colours.items()]
