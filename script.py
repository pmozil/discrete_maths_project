from alternative_algorithm import rg
import two_sat as ts
from alternative_sat import *
grp, _ = read_graph("test.csv")
cols = list(sorted(colour_graph(grp), key=lambda x: x[0]))
grp1, _ = read_graph("tmp.csv")
cols_grp1 = {0: 1, 1: 0, 2: 0, 3:0}
cols1 = list(sorted(colour_graph(grp1), key=lambda x: x[0]))
wheel = {0 :[1, 4, 5], 1:[0, 2, 5], 2:[1, 3, 5], 3:[2, 4, 5], 4:[0,3,5], 5:[0,1,2,3,4]}
cols_wheel = list(sorted(colour_graph(wheel), key=lambda x: x[0]))
res = ts.colour_graph(grp1, dict(cols1))
