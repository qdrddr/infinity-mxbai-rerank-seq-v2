## install 
Using the setup.sh script

## Run this proxy

```shell
python proxy-classifier.py
```


## Run infinity
in a separate terminal. Use the model michael already converted for us: `michaelfeil/mxbai-rerank-large-v2-seq` or `michaelfeil/mxbai-rerank-base-v2-seq`:
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