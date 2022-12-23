import argparse
import alternative_sat as al
import two_sat as ts
# Tests, that's why they are commented out
# grp, _ = ts.read_csv("test.csv")
# cols = list(sorted(al.colour_graph(grp), key=lambda x: x[0]))
# grp1, _ = ts.read_csv("tmp.csv")
# cols_grp1 = {0: 1, 1: 0, 2: 0, 3:0}
# cols1 = list(sorted(al.colour_graph(grp1), key=lambda x: x[0]))
# wheel = {0 :[1, 3, 5], 1:[0, 2, 5], 2:[1, 3, 5], 3:[2, 0, 5], 5:[0,1,2,3]}
# cols_wheel = list(sorted(al.colour_graph(wheel), key=lambda x: x[0]))
# res = ts.colour_graph(grp, dict(cols))
# res1 = ts.colour_graph(grp1, dict(cols1))
# res_wheel = ts.colour_graph(wheel, {0:0, 1:1, 2:0, 3:1, 5:1})

parser = argparse.ArgumentParser()
parser.add_argument("fname")

args = parser.parse_args()

graph, cols = ts.read_csv(args.fname)
