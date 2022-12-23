# discrete_maths_project report


# The algorithm principle
The colouring is done be solving a 2-CNF formula.

These formulas look like this
> (x1∨¬x2)∧(¬x2∨¬x3)∧(x2∨¬x3)∧(x1∨x3)

> **Note that (x1∨x2) ≡ (¬x1→x2)∧(¬x2→x1)**
> **Also, (x1→x2)∧(x2→x3) ≡ x1→x3**

We solve these formulas by building an implication graph as such:
1. Replace all disjuncitons with the conjunction of implications
2. By the transitivity of implications, the strongly connected components have to be of the same sign: T→T→F ≡ F ⇒ all elements in the chain either have to be false, or true.
3. ↑ That is true, because a strongly connected component [x1, x2, x3] is the same as [x2, x3, x1], So if even one element is true, and all the others are false, then there exists a loop which breks it all
4. If x and ¬x are in the same component, it all breaks for the same reason
5. The last step is to simply enumerate elements in the SCC to be of the same value (T/F)

That is the solution to the 2-SAT problem. On to the specifics of this graph colouring.
Because the vertice has to change color, it can only have one of **two** colours. That makes it possible to make logical clauses that state the fact that no adjacent vertice can have the same colourolour, and that the vertice has to have one colour for every pair of adjacent vertices.

Thus, we form this for every pair of vertices:
1. Every vertice now has three variables tied to it: xr, xg, xb (for R/G/B colours)
2. Suppose the base colour of x is red, the base colour of y is also red. Then, for every pair of adjacent vertices {x, y} the following clauses are added to th 2-CNF:
- (¬xg∨¬yg)∧(¬xb∨¬yb)∧(xb∨xg)∧(yb∨yg)∧(
*Note that as the colour vary, there may be only three disjunctions*
3. Solve the underlying 2-CNF
4. Colour the vertices by the boolean values

This is the description of the algorithm used in `two_sat` [Here's the link for the work, in which the algorithm used in `alternative_sat` is described](https://www.researchgate.net/publication/220827314_Solving_3-Colouring_via_2SAT)

The `alternative_algorithm` uses a genetic algorithm similar to backtracking so as to colour a graph into a non-constant amount of colours in ± constant time.

## Project structure
The project itself consists of only one file - `two_sat.py`

The file consists of four functions:
- `read_csv` - reads the csv into a graph



- `write_csv` - writes a grph to csv


- `colour_graph` - returns either a recoloured graph or nothing, if the graph does not exist


- `alternative_sat`, `alternative_algorithm` - the alternative algorithms for colouring a graph. Those don't check it the colour of the vertice changes.

**Because there are only three functions, @pmozil proposes that there be 
multiple `colour_graph` functions**

Here's the distribution of work:
- `read_csv`, `invert_graph`: Bohdan Pavliuk


- `colour_graph`, `dfs`: Denys Humeniuk, Iryna Voitsitska, Yulia Vistak


- `scc`, `alternative_sat`, `alternative_algorithm`: Petro Mozil

CSV example (`test.csv`):
```
0,1,0,1
0,2,0,2
1,2,1,2
0,3,0,1
4,3,0,1
5,3,1,1
5,0,1,0
```

`read_csv` on this CSV must return this python dictionary:
```python
{
    0: [1, 2, 3, 5],
    1: [0, 2],
    2: [0, 1],
    3: [0, 4, 5],
    4: [3], 5: [0, 3]
}
{0: 0, 1: 1, 2: 2, 3: 1, 4: 0, 5: 1}
```

- colour_graph - returns either a recoloured graph or nothing, if the graph does not exist


- make_impl_graph Make a directed implication graph from an undirected graph
For each vertex makes the edges the same, only with a vertex of the opposite value
dfs searches for the dfs-path from the point ‘cur'
Sorts the edges of the input graph, throws the cur point into the stack
Then when key = stack[-1], filters the key value, throws each subsequent point from the key value  in the stack and parallel to the path. After that delete ‘cur’ from the stack
Сontinue these actions until the stack is empty


- invert_graph inverts graph
Goes through each key of the input dictionary, then goes through each element of the key value and make each a key in the new dictionary, and its value is a list of keys in the old one
scc searches strongly connected components
Searches the dfs-path from the point, then inverts the graph. Then looks for the return path (dfs-path from the last point of the path to the initial one)
If the path exists, there is also a strongly connected component


- colour_graph Colour a graph with 2-SAT
It is then run through each vertex and forms an auxiliary list of edges
Converts it into a directed implication graph and looks for strongly connected components

