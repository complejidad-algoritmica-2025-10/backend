from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx
import json
import os
from itertools import combinations
from collections import defaultdict

app = FastAPI()

# Permitir peticiones desde el frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# === CARGA DE DATOS ===
DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")

with open(os.path.join(DATASET_DIR, "movies_filtradas.json"), encoding="utf-8") as f:
    movies = json.load(f)
with open(os.path.join(DATASET_DIR, "persons_filtradas.json"), encoding="utf-8") as f:
    persons = json.load(f)
with open(os.path.join(DATASET_DIR, "principals_filtrados.json"), encoding="utf-8") as f:
    principals = json.load(f)

# === CREAR GRAFO BIPARTITO ===
B = nx.Graph()
for movie in movies:
    B.add_node(movie["tconst"], bipartite=0, type="movie")
for person in persons:
    B.add_node(person["nconst"], bipartite=1, type="person", gender=person.get("gender", "U"))
for p in principals:
    B.add_edge(p["nconst"], p["tconst"])

# === GRAFO PROYECTADO DE COACTUACIÓN ===
P = nx.Graph()

# Crear diccionario: tconst -> lista de nconst de actores/actrices
coact_dict = defaultdict(list)
for p in principals:
    if p["category"] in ["actor", "actress"]:
        coact_dict[p["tconst"]].append(p["nconst"])

# Crear aristas entre actores que trabajaron juntos
for actores in coact_dict.values():
    for a1, a2 in combinations(actores, 2):
        if a1 != a2:
            if P.has_edge(a1, a2):
                P[a1][a2]["weight"] += 1
            else:
                P.add_edge(a1, a2, weight=1)

# Asignar nombre y género como atributos
id_to_name = {person["nconst"]: person["primaryName"] for person in persons}
id_to_gender = {person["nconst"]: person.get("gender", "U") for person in persons}

for node in P.nodes:
    P.nodes[node]["name"] = id_to_name.get(node, node)
    P.nodes[node]["gender"] = id_to_gender.get(node, "U")





# === MODELOS Y ENDPOINTS ===
class Edge(BaseModel):
    source: str
    target: str

@app.get("/ping")
def ping():
    return {"message": "pong"}

def graph_to_json(graph: nx.Graph):
    nodes = [{"id": n, **graph.nodes[n]} for n in graph.nodes]
    edges = [{"source": u, "target": v, **graph[u][v]} for u, v in graph.edges]
    return {"nodes": nodes, "edges": edges}

@app.get("/bipartite")
def get_bipartite():
    return graph_to_json(B)

@app.get("/projected")
def get_projected():
    return graph_to_json(P)