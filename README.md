# discrete_maths_project report

[Here's the link for the work, in which the algorithm used is described](https://www.researchgate.net/publication/220827314_Solving_3-Colouring_via_2SAT)

## Project structure
The project itself consists of only one file - `two_sat.py`

The file consists of four functions:
- `read_csv` - reads the csv into a graph
- `write_csv` - writes a grph to csv
- `colour_graph` - returns either a recoloured graph or nothing, if the graph does not exist

**Because there are only three functions, @pmozil proposes that there be 
multiple `colour_graph` functions**

Here's the distribution of work:
    - `read_csv` **(author here)**
    - `write_csv` **(author here)**
    - `colour_graph` **(author here)**

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

and `write_csv` must write the same csv as `test.csv` into the file
