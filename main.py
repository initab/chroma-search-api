from typing import Annotated

import chromadb
from chromadb.utils import embedding_functions
from fastapi import FastAPI, Body
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI(root_path="/api")
client = chromadb.HttpClient()
embedding_prompt = "Vad handlar denna text om: "
collection = client.get_collection(name="init-sharepoint",
                                   embedding_function=embedding_functions.
                                   SentenceTransformerEmbeddingFunction(
                                       model_name="KBLab/sentence-bert-swedish-cased",
                                       prompts={
                                           "init":
                                               embedding_prompt,
                                       }
                                   )
                                   )

model = SentenceTransformer(
    'KBLab/sentence-bert-swedish-cased',
    prompts={
        "init": embedding_prompt,
    },
)


class Query(BaseModel):
    prompt: str
    num_results: int | None = 3


@app.post("/search")
async def search(
        query: Annotated[Query, Body(title="Query prompt to search for")],
):
    q_res = collection.query(
        query_embeddings=model.encode(query.prompt,
                                      prompt_name="init").tolist(),
        n_results=query.num_results
    )

    response = {
        "ids": q_res["ids"][0],
        "distances": q_res["distances"][0],
        "documents": q_res["documents"][0],
        "metadata": q_res["metadatas"][0],
    }

    return response
