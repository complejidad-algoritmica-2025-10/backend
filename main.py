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

@app.get("/api/graph/bipartite")
def get_bipartite():
    return graph_to_json(B)

#@app.get("/api/graph/coactuacion")
#def get_coactuacion():
#    return graph_to_json(G)
