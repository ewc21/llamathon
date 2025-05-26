import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import json
from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
print("CWD:", os.getcwd())
all_chunks=[]
foodgroup1 = pd.read_csv('backend/api/rag/datasets/FOOD-DATA-GROUP1.csv')
foodgroup2 = pd.read_csv('backend/api/rag/datasets/FOOD-DATA-GROUP2.csv')
foodgroup3 = pd.read_csv('backend/api/rag/datasets/FOOD-DATA-GROUP3.csv')
foodgroup4 = pd.read_csv('backend/api/rag/datasets/FOOD-DATA-GROUP4.csv')
foodgroup5 = pd.read_csv('backend/api/rag/datasets/FOOD-DATA-GROUP5.csv')
fastfood = pd.read_csv('backend/api/rag/datasets/fastfood.csv')
csvs = [foodgroup1, foodgroup2, foodgroup3, foodgroup4, foodgroup5, fastfood]
for csv in csvs:
    text = csv.astype(str).apply(lambda x: " ".join(x), axis=1).str.cat(sep="\n")
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    all_chunks.extend(chunks)
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(all_chunks)
index = faiss.IndexFlatL2(embeddings.shape[1])
index = faiss.IndexFlatL2(embeddings[0].shape[0])
index.add(np.array(embeddings))
Path("data").mkdir(exist_ok=True)
faiss.write_index(index, "data/food_index.faiss")

# Save original chunks
with open("data/food_chunks.json", "w") as f:
    json.dump(all_chunks, f)
    

