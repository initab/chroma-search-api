import json
from typing import Annotated

import chromadb
from chromadb.utils import embedding_functions
from fastapi import FastAPI, Body
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import os

config_path = os.getenv('CHROMA_SEARCH_API_CONFIG', 'config.json')

with open(config_path) as f:
    config = json.load(f)

app = FastAPI(root_path=config["root"])
host = config["chroma-host"]
port = config["chroma-port"]
client = chromadb.HttpClient(host, port)
embedding_prompt = config["embedding-prompt"]
collection_name = config["collection-name"]
model_name = config["model"]
key = config["prompt-key"]
collection = client.get_collection(name=collection_name,
                                   embedding_function=embedding_functions.
                                   SentenceTransformerEmbeddingFunction(
                                       model_name=model_name,
                                       prompts={
                                           key:
                                               embedding_prompt,
                                       }
                                   )
                                   )

model = SentenceTransformer(
    model_name,
    prompts={
        key: embedding_prompt,
    },
)


class Query(BaseModel):
    prompt: str
    num_results: int | None = 3


@app.post(config["endpoint"])
async def search(
        query: Annotated[Query, Body(title="Query prompt to search for")],
):
    q_res = collection.query(
        query_embeddings=model.encode(query.prompt,
                                      prompt_name=key).tolist(),
        n_results=query.num_results
    )

    response = {
        "ids": q_res["ids"][0],
        "distances": q_res["distances"][0],
        "documents": q_res["documents"][0],
        "metadata": q_res["metadatas"][0],
    }

    return response
