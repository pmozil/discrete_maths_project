from alternative_algorithm import rg
from alternative_sat import *
grp, _ = read_graph("test.csv")
cols = list(sorted(colour_graph(grp), key=lambda x: x[0]))
