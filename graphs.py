import networkx as nx
from itertools import combinations
from collections import defaultdict

# === GENERAL ===

def graph_to_json(graph: nx.Graph):
    nodes = [{"id": n, **graph.nodes[n]} for n in graph.nodes]
    edges = [{"source": u, "target": v, **graph[u][v]} for u, v in graph.edges]
    return {"nodes": nodes, "edges": edges}

def enrich_person_nodes(G: nx.Graph, persons: list):
    id_to_name = {p["nconst"]: p["primaryName"] for p in persons}
    id_to_gender = {p["nconst"]: p.get("gender", "U") for p in persons}

    for node in G.nodes:
        if G.nodes[node].get("type") == "person" or node in id_to_name:
            G.nodes[node]["name"] = id_to_name.get(node, node)
            G.nodes[node]["gender"] = id_to_gender.get(node, "U")

def enrich_movie_nodes(G: nx.Graph, movies: list):
    id_to_title = {m["tconst"]: m["primaryTitle"] for m in movies}

    for node in G.nodes:
        if G.nodes[node].get("type") == "movie":
            G.nodes[node]["name"] = id_to_title.get(node, node)

# === BIPARTITE GRAPH ===

# Represents the relationship between persons that worked in a movie in any role

def create_bipartite_graph(movies, persons, principals):
    B = nx.Graph()

    for movie in movies:
        B.add_node(movie["tconst"], bipartite=0, type="movie")

    for person in persons:
        B.add_node(person["nconst"], bipartite=1, type="person")

    for principal in principals:
        B.add_edge(principal["nconst"], principal["tconst"])

    enrich_person_nodes(B, persons)
    enrich_movie_nodes(B, movies)
    return B

# === PROJECTED GRAPH ===

# Represents the network of colaborations between persons that worked on the same movie together

def create_projected_graph(persons, principals):
    P = nx.Graph()

    coact_dict = defaultdict(list)
    for p in principals:
        coact_dict[p["tconst"]].append(p["nconst"])

    for participantes in coact_dict.values():
        for p1, p2 in combinations(participantes, 2):
            if p1 != p2:
                if P.has_edge(p1, p2):
                    P[p1][p2]["weight"] += 1
                else:
                    P.add_edge(p1, p2, weight=1)

    enrich_person_nodes(P, persons)
    return P

def get_projected_clusters(graph: nx.Graph):
    components = nx.connected_components(graph)
    return [graph_to_json(graph.subgraph(c).copy()) for c in components]

def get_bipartite_clusters(graph: nx.Graph):
    components = nx.connected_components(graph)
    return [graph_to_json(graph.subgraph(c).copy()) for c in components]