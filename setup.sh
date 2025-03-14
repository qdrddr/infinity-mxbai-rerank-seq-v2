pyver=3.12
uv init --python ${pyver} .
uv python install ${pyver}


uv venv --python ${pyver}
source .venv/bin/activate
uv python pin ${pyver}

uv pip install typing pydantic fastapi dotenv requests uvicorn api


