def create_mxbai_v2_reranker_prompt_template(query: str, document: str, instruction: str = "") -> str:
    """
    Create a carefully formatted chat template string (without tokenizer) for ranking relevance.

    Parameters:
        query (str): The search query.
        document (str): The document text to evaluate.
        instruction (str): Special instructions (e.g., "You are an expert for Mockingbirds.")

    Returns:
        str: The formatted chat template.
    """
    instruction = f"instruction: {instruction}\n" if instruction else ""    
    # fixed system prompt, keep as is.
    system_prompt = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
    assert not "\n" in system_prompt
    assert not "\n" in instruction[:-1]
    assert isinstance(query, str)
    assert isinstance(document, str)
    templated = (
        # keep spacing, newlines as is.
        # template for mixedbread reranker v2
        # https://huggingface.co/michaelfeil/mxbai-rerank-base-v2-seq/
       f"<|endoftext|><|im_start|>system\n{system_prompt}\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"{instruction}"
        f"query: {query} \n"
        f"document: {document} \n"
        "You are a search relevance expert who evaluates how well documents match search queries. "
        "For each query-document pair, carefully analyze the semantic relationship between them, then provide your binary relevance judgment (0 for not relevant, 1 for relevant).\n"
        "Relevance:<|im_end|>\n"
        "<|im_start|>assistant\n"
    )
    return templated