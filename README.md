# discrete_maths_project report

## Project structure
The project itself consists of only one file - `two_sat.py`

The file consists of four functions:
- `read_csv` - reads the csv into a graph
- `write_csv` - writes a grph to csv
- `colour_graph` - returns either a recoloured graph or nothing, if the graph does not exist

**Because there are only three functions, @pmozil proposes that there be 
multiple `colour_graph functions**

Here's the distribution of work:
    - `read_csv` **(author here)**
    - `write_csv` **(author here)**
    - `colour_graph` **(author here)**

CSV example (`test.csv`):
```
0,1,1,2
0,2,1,3
1,2,2,3
3,0,2,1
2,3,3,2
```

`read_csv` on this CSV must return this python dictionary:
```python
{
    (0,1): [(1,2), (2,3), (3,2)],
    (1,2): [(0,1), (2,3)],
    (2,3): [(0,1), (1,2), (3,2)],
    (3,2): [(0,1), (2,3)]
}
```

and `write_csv` must write the same csv as `test.csv` into the file
