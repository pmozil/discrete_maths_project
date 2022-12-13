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
def make_impl_graph(graph: Dict[int, List[int]]) -> Dict[int, List[int]]:
    """
    Make a directed implication graph from an undirected graph
    Args:
        graph: Dict[int, List[int]] - a dictionary.
            Basically an unsparsed adjacency matrix
    Returns:
        bool - whether the graph edge colouring is valid
    x v y = !x -> y & !y -> x
    """
    # Need to multiply by three, because there's three nodes for each colour
    graph = {vert * 3: {v * 3 for v in graph[vert]} for vert in graph}
    result = {}
    # The implication graph is the hardest damn part of it all.
    # This will only check the uniquness of the colors, 
    # AND ONLY THEN we use ANOTHER TWO FUNCTIONS to check
    # whether the zll the vertices actually have exacty one colour >:[
    # Man, the Catalan numbers would've been so much more fun.
    for vertice, items in graph.items():
        for i in range(3):
            if (vertice + i) not in result:
                result[vertice+i] = list(
                        filter(
                            lambda x: x != -vertice-i,
                            range(-vertice-2, -vertice+1)
                            )
                        )
                print(vertice+i)
            for item in items:
                if -item-i not in result[vertice+i]:
                    result[vertice+i].append(-item-i)
                if (item + i) not in result:
                    result[item+i] = list(
                            filter(
                                lambda x: x != -item-i,
                                range(-item-2, -item+1)
                                )
                            )
                if -vertice-i not in result[item+i]:
                    result[item+i].append(-vertice-i)
                
    return result, min(result)


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
            for index, p in enumerate(paths):
                for node in p:
                    if node in map(abs, path):
                        paths[i].extend
            yield path[:]
            path.clear()
    return
