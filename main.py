# Computes the upper bound in performance out of a sqlite db with interactions and a dataset

import csv, sys, sqlite3
import itertools as it
import networkx as nx



def parse_data_file(pathway_path):
    with open(pathway_path) as f:
        reader = csv.reader(f, delimiter='\t')
        pathways = [tuple(p) for p in reader]

    return pathways

def breakout_pathways(pathways):
    interactions = set()
    for pathway in pathways:
        left, right = it.tee(pathway)
        next(right, None)
        for l, r in it.izip(left, right):
            interactions.add((l, r))

    return interactions

def build_network(sqlite_path):
    with sqlite3.connect(sqlite_path) as conn:
        result_set = conn.execute("SELECT controller, controlled FROM Interactions;")
        interactions = {(row[0], row[1]) for row in result_set}

    G = nx.DiGraph()
    for a, b in interactions:
        G.add_edge(a, b)

    return G


def find_interactions(network, interactions):
    recoverability = dict()
    shortest_paths = dict()
    for i in interactions:
        recoverable = False
        try:
            path = nx.shortest_path(network, i[0], i[1])
            shortest_paths[i] = path
            recoverable = True
        except nx.NetworkXNoPath:
            print "No path between %s and %s" % i


        recoverability[i] = recoverable

    return recoverability


def is_recoverable(pathway, recoveravility):
    interactions = breakout_pathways([pathway])
    recoverable = [recoveravility[i] for i in interactions]

    return all(recoverable)


def main(pathway_path, sqlite_path):
    pathways = parse_data_file(pathway_path)
    interactions = breakout_pathways(pathways)
    network = build_network(sqlite_path)
    interaction_recovery = find_interactions(network, interactions)

    pathway_recovery = {p:is_recoverable(p, interaction_recovery) for p in pathways}

    not_recoverable = [p for p, r in pathway_recovery.iteritems() if not r]

    print "Not recoverable paths: %i" % len(not_recoverable)
    for p in not_recoverable:
        print p

if __name__ == "__main__":
    pathway_path = sys.argv[1]
    sqlite_path = sys.argv[2]
    main(pathway_path, sqlite_path)