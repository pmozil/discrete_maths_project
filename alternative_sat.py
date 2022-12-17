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

        if s in graph:
            for node in graph.get(s):
                if node in path and isinstance(cycles, list):
                    cycle = path[path.index(node) : path.index(s) + 1]
                    if cycle not in cycles:
                        cycles.append(cycle)
                if node in visited and isinstance(back_edges, list):
                    back_edges.append((s, node))
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
    res = []
    for ec in even_cycles:
        for oc in [x for x in odd_cycles if x != ec]:
            for el in ec:
                if el in oc and ec not in res:
                    res.append(ec)
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
                if v_1 in graph[v1] and (v_1, v1) not in graph:
                    res.append((v1, v_1))
                if v_2 in graph[v1] and (v_2, v1) not in graph:
                    res.append((v1, v_2))
                if v_1 in graph[v2] and (v_1, v2) not in graph:
                    res.append((v2, v_1))
                if v_2 in graph[v2] and (v_2, v2) not in graph:
                    res.append((v2, v_2))
    return res


def colour_graph(
    graph: Dict[int, List[int]], *, start_cols: List[Tuple[int]] = []
) -> List[Tuple[int]]:
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
    # This is just for comfort, won't be faster until the node count is like 10^5
    start_cols = dict(start_cols)
    graph = {v+1: [ver + 1 for ver in graph[v]] for v in graph}
    cycles, dfs_tree_colours, back_edges = [], {}, []
    for elem in graph:
        _ = dfs(
            graph, 1, set(), [], colours=dfs_tree_colours, back_edges=back_edges, cycles=cycles
        )
    cycles = [cycle for cycle in cycles if len(cycle) > 2]
    print(cycles)
    odd_cycles, even_cycles = [], []
    for cycle in cycles:
        if len(cycle) % 2:
            odd_cycles.append(cycle)
        else:
            even_cycles.append(cycle)
    print(odd_cycles, even_cycles)
    inters = get_cycle_intersections(odd_cycles, even_cycles)
    odd_inters = get_cycle_intersections(odd_cycles, odd_cycles)
    if len(odd_inters) > 0:
        # Some odd cycles intersect, thus no solution. Yay!
        print("this")
        return {v-1: e for v, e in dfs_tree_colours.items()}
    back_edges = list(get_back_edges(odd_cycles, back_edges))
    # TODO: finish the function
    clauses = []
    clauses.extend((-x, -y) for x, y in adjacent_edges(graph, back_edges))
    clauses.extend(back_edges)
    clauses.extend((-x, -y) for x, y in back_edges)
    clauses.extend((cycle[0], cycle[-1]) for cycle in inters)
    strongly_connected = list(scc(make_impl_graph(clauses)))

    # We gonna check if the formula is satisfiable. If not, NOBODY CARES
    # I have a general distaste for graphs, especially this stupid case
    # Why not use backtracking or even just a forward-backward approach?

    # Get unique numbers from list, gotta have them all
    uniques = set()
    colours = set()

    for clause in strongly_connected:
        for lit in clause:
            # No solution for CNF, so we can do nothing. The good ending
            uniques.add(abs(lit))
            if -lit in clause:
                print("The 2-CNF is unsatisfiable. Sorry(")
                return {v-1: e for v, e in dfs_tree_colours.items()}

    i = 0
    while len(colours) != len(uniques) and i < len(strongly_connected):
        clause = strongly_connected[i]
        for lit in clause:
            if -lit in colours:
                colours.remove(-lit)
            colours.add(lit)
        i += 1
    # Man, it's like a billion checks for the colouring being proper.
    if not all(x in colours or -x in colours for x in uniques):
        print("What? Why would the 2-CNF be satisfiable, but have no solution?")
        return {v-1: e for v, e in dfs_tree_colours.items()}

    for col in colours:
        if col > 0:
            dfs_tree_colours[abs(col)] = 2

    print({v-1 : [vv-1 for vv in graph[v]] for v in graph})
    return {v-1: e for v, e in dfs_tree_colours.items()}
