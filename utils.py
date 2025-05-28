import os
import json

# === DATA LOAD ===
# Loads the data to feed the graphs from the dataset folder

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")

def load_data():
    with open(os.path.join(DATASET_DIR, "movies_filtradas.json"), encoding="utf-8") as f:
        movies = json.load(f)

    with open(os.path.join(DATASET_DIR, "persons_filtradas.json"), encoding="utf-8") as f:
        persons = json.load(f)

    with open(os.path.join(DATASET_DIR, "principals_filtrados.json"), encoding="utf-8") as f:
        principals = json.load(f)

    return movies, persons, principals
