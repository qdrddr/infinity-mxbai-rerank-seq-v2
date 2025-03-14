# Classifier 2 Rerrank Infinity Proxy for mxbai-rerank-v2
This app acts as a proxy to your running infinity inference. It utilizes classifier endpoint of the infinity on backend, and presents it as a reranking endpoint on the frontend so you can use it with LiteLLM.

## Reasoning
Michael from Infinity [recommended](https://github.com/michaelfeil/infinity/issues/552) to run model as a classifier. If you want to utilize this model via reranking endpoint with your application (such as LiteLLM) that expects reranking endpoint format you need to run this proxy.

## Prepare
Using the [setup.sh](setup.sh) script.

## Run this proxy

```shell
python proxy-classifier.py
```


## Run infinity inference with mxbai-rerank-v2 model
In a separate terminal. Use the model Michael Feil already converted for us, thanks Michael!
- [michaelfeil/mxbai-rerank-large-v2-seq](https://huggingface.co/michaelfeil/mxbai-rerank-large-v2-seq)
- [michaelfeil/mxbai-rerank-base-v2-seq](https://huggingface.co/michaelfeil/mxbai-rerank-base-v2-seq)
```shell
infinity_emb v2 --port 7997 \
  --model-id michaelfeil/mxbai-rerank-large-v2-seq --batch-size 8 --revision "refs/heads/main" \
  --url-prefix "/v1"
```

## make a reranking request

```shell
curl --location 'http://localhost:8002/v1/rerank' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "model": "michaelfeil/mxbai-rerank-large-v2-seq",
    "query": "What is the capital of the United States?",
    "documents": [
        "Carson City is the capital city of the American state of Nevada.",
        "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
        "Washington, D.C. is the capital of the United States.",
        "Capital punishment has existed in the United States since before it was a country."
    ],
    "top_n": 4
  }'
```

### Result Example
```json
{
    "object": "rerank",
    "results": [
        {
            "relevance_score": 0.9999322891235352,
            "index": 2,
            "document": null
        },
        {
            "relevance_score": 0.8560222387313843,
            "index": 0,
            "document": null
        },
        {
            "relevance_score": 0.7231764197349548,
            "index": 1,
            "document": null
        },
        {
            "relevance_score": 0.44487491250038147,
            "index": 3,
            "document": null
        }
    ],
    "model": "michaelfeil/mxbai-rerank-large-v2-seq",
    "usage": {
        "prompt_tokens": 1642,
        "total_tokens": 1642
    },
    "id": "infinity-6fd026a3-ea6b-4b5e-bc04-4b6f1953766a",
    "created": 1741979826
}
```