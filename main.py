# App dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# App logic
from utils import load_data
from graphs import create_bipartite_graph, create_projected_graph, get_projected_clusters, get_bipartite_clusters

# Instantiate app
app = FastAPI()

# Allow requests ONLY from local frontend -> set to be on port 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# === LOAD FROM DATASET ===
MOVIES, PERSONS, PRINCIPALS = load_data()

# === INSTANTIATE BIPARTITE GRAPH ===
B = create_bipartite_graph(MOVIES, PERSONS, PRINCIPALS)

# === INSTANTIATE PROJECTED GRAPH ===
P = create_projected_graph(PERSONS, PRINCIPALS)

# === MODELOS Y ENDPOINTS ===
class Edge(BaseModel):
    source: str
    target: str

@app.get("/bipartite")
def bipartite_clusters():
    return {"clusters": get_bipartite_clusters(B)}

@app.get("/projected")
def projected_clusters():
    return {"clusters": get_projected_clusters(P)}