from alternative_algorithm import rg
from alternative_sat import *
gr = rg("test.csv")
grp = {vert[0]: [v[0] for v in gr[vert]] for vert in gr}
gr, n = make_impl_graph(grp)
