from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx

app = FastAPI()
G = nx.Graph()

# Permitir peticiones desde el frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Edge(BaseModel):
    source: str
    target: str

@app.post("/add-edge")
def add_edge(edge: Edge):
    G.add_edge(edge.source, edge.target)
    return {"status": "ok", "nodes": list(G.nodes), "edges": list(G.edges)}

@app.get("/ping")
def ping():
    return {"message": "pong"}