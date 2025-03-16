# Classifier 2 Rerrank Infinity Proxy for mxbai-rerank-v2

This app is a PoC. This app acts as a proxy for your existing running infinity inference. It utilizes classifier endpoint route of the infinity on backend, and presents itself as a reranking endpoint on the frontend so you can use it with LiteLLM.

## Reasoning

Michael from Infinity [recommended](https://github.com/michaelfeil/infinity/issues/552) to run model as a classifier. If you want to utilize this model via reranking endpoint with your application (such as LiteLLM) that expects reranking endpoint format you need to run application like this.

## Prepare

Using the [setup.sh](setup.sh) script.

## Run this proxy

Using Python
```shell
python proxy-classifier.py
```

Or using docker:
```shell
docker compose -f docker-compose.yaml up -d
```

## Run infinity inference with mxbai-rerank-v2 model

In a separate terminal. Use the model Michael Feil already converted for us, thanks Michael!

- [michaelfeil/mxbai-rerank-large-v2-seq](https://huggingface.co/michaelfeil/mxbai-rerank-large-v2-seq)
- [michaelfeil/mxbai-rerank-base-v2-seq](https://huggingface.co/michaelfeil/mxbai-rerank-base-v2-seq)

```shell
infinity_emb v2 --port 7997 \
  --model-id michaelfeil/mxbai-rerank-large-v2-seq --batch-size 1 --revision "refs/heads/main" \
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
      "relevance_score": 0.9999301433563232,
      "index": 2,
      "document": null
    },
    {
      "relevance_score": 0.8872248530387878,
      "index": 0,
      "document": null
    },
    {
      "relevance_score": 0.8324779272079468,
      "index": 1,
      "document": null
    },
    {
      "relevance_score": 0.44686806201934814,
      "index": 3,
      "document": null
    }
  ],
  "model": "michaelfeil/mxbai-rerank-large-v2-seq",
  "usage": {
    "prompt_tokens": 2282,
    "total_tokens": 2282
  },
  "id": "infinity-9d00343b-20a9-4d69-9367-438a68bc08cb",
  "created": 1742163022
}
```
