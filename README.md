# 🎬 API de Visualización de Redes IMDb

Este proyecto es una API construida con **FastAPI** que permite generar y servir grafos derivados del dataset público de **IMDb**. Está diseñada para trabajar en conjunto con un cliente Vue.js, y permite explorar relaciones de colaboración en la industria cinematográfica con un enfoque en la **representación de género**.

## 🚀 Tecnologías utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) — Framework moderno para construir APIs con Python  
- [NetworkX](https://networkx.org/) — Para crear y procesar grafos  
- [Pydantic](https://docs.pydantic.dev/) — Para validación de datos  
- [IMDb Dataset (procesado)](https://www.imdb.com/interfaces/) — Fuente principal de datos  

## 🧠 Funcionalidad

La API carga y transforma los datos en dos tipos de grafos:

### 1. Grafo Bipartito (`/bipartite`)
Representa relaciones entre **personas** y **películas**.  
Cada nodo es una persona o una película, y las aristas representan participaciones en producciones.

### 2. Grafo Proyectado (`/projected`)
Proyecta el grafo bipartito sobre personas, conectando aquellas que trabajaron **juntas** en al menos una película.  
Incluye información enriquecida como género, nombre y peso de conexión.

## 📁 Estructura del proyecto

```
backend/
├── main.py              # Archivo principal de la API
├── graphs.py            # Lógica de construcción y enriquecimiento de grafos
├── utils.py             # Carga de datos desde JSON
├── dataset/
│   ├── movies.json
│   ├── persons.json
│   └── principals.json
```

## 🔁 Endpoints

| Método | Ruta           | Descripción                                     |
|--------|----------------|-------------------------------------------------|
| GET    | `/bipartite`   | Retorna clusters del grafo bipartito           |
| GET    | `/projected`   | Retorna clusters del grafo proyectado (personas) |

## 🔐 CORS

La API permite solicitudes **únicamente desde**:  
`http://localhost:5173` (por defecto, puerto del frontend con Vite)

## 🛠️ Instalación y ejecución

```bash
# Instala dependencias
pip install fastapi uvicorn networkx

# Ejecuta la API localmente
uvicorn main:app --reload
```

## 📄 Licencia y uso

Este proyecto tiene fines **académicos** y no debe utilizarse con fines comerciales sin autorización. Utiliza datos públicos de IMDb bajo su [licencia de uso](https://www.imdb.com/interfaces/).

---

> ¿Necesitas también un `requirements.txt`? Te puedo generar uno en segundos.
