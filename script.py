from alternative_algorithm import rg
from alternative_sat import *
grp, _ = read_graph("test.csv")
cols = list(sorted(colour_graph(grp), key=lambda x: x[0]))
grp1, _ = read_graph("tmp.csv")
cols1 = list(sorted(colour_graph(grp1), key=lambda x: x[0]))
wheel = {0 :[1, 5], 1:[2,5 ], 2:[3,5], 3:[4,5], 5:[0,1,2,3]}
cols_wheel = list(sorted(colour_graph(wheel), key=lambda x: x[0]))
