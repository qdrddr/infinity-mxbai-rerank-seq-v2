import requests
import json
import time
import os
import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Header


app = FastAPI(title="MXbai Rerank API")

# Define request/response models
class RerankRequest(BaseModel):
    query: str
    documents: List[str]
    model: str = "michaelfeil/mxbai-rerank-large-v2-seq"
    top_n: Optional[int] = None
    return_documents: bool = False
    max_chunks_per_doc: Optional[int] = None

class RerankResult(BaseModel):
    relevance_score: float
    index: int
    document: Optional[str] = None

class RerankUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int

class RerankResponse(BaseModel):
    object: str = "rerank"
    results: List[RerankResult]
    model: str
    usage: RerankUsage
    id: str
    created: int

@app.post("/v1/rerank", response_model=RerankResponse)
async def rerank(request: RerankRequest, authorization: Optional[str] = Header(None)):
    # Prepare inputs for the classifier endpoint
    inputs = [
        f"Query: {request.query}\nDocument: \"{doc}\"\n\nYou are a search relevance expert who evaluates how well documents match search queries. For each query-document pair, carefully analyze the semantic relationship between them, then provide your binary relevance judgment (0 for not relevant, 1 for relevant).\nRelevance:\n"
        for doc in request.documents
    ]

    # Create payload for the classification API
    payload = {
        "input": inputs,
        "model": request.model,
        "raw_scores": True
    }

    # Set headers and forward the incoming Authorization header if provided
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    if authorization:
        headers["Authorization"] = authorization

    try:
        # Call classification endpoint
        response = requests.post(
            "http://0.0.0.0:7997/v1/classify", 
            headers=headers, 
            data=json.dumps(payload)
        )
        response.raise_for_status()
        response_data = response.json()

        # Extract scores from the response structure
        scores = []
        if "data" in response_data:
            for item in response_data["data"]:
                # Get the score for the "1"/relevant label
                relevant_score = next(
                    (x["score"] for x in item if x["label"] == "1"),
                    max(x["score"] for x in item)
                )
                scores.append(relevant_score)
        else:
            raise HTTPException(status_code=500, detail="Unexpected response format from classification API")
        
        # Create list of results with index and scores
        formatted_results = [
            {
                "relevance_score": score,
                "index": idx,
                "document": doc if request.return_documents else None
            }
            for idx, (score, doc) in enumerate(zip(scores, request.documents))
        ]

        # Sort results by score in descending order
        formatted_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Apply top_n filter if specified
        if request.top_n is not None and request.top_n > 0:
            formatted_results = formatted_results[:request.top_n]

        # Get token counts from response or estimate otherwise
        total_tokens = response_data.get("usage", {}).get("prompt_tokens", len(''.join(inputs)))

        # Create final response
        final_response = {
            "object": "rerank",
            "results": formatted_results,
            "model": response_data.get("model", request.model),
            "usage": {
                "prompt_tokens": total_tokens,
                "total_tokens": total_tokens
            },
            "id": response_data.get("id", f"rerank-{uuid.uuid4()}"),
            "created": response_data.get("created", int(time.time()))
        }

        return final_response

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling classification API: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("proxy-classifier:app", host="0.0.0.0", port=8002, reload=True)