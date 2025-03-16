FROM python:3.12-slim

# Set working directory and copy all files
WORKDIR /app
COPY . /app

# Upgrade pip and install dependencies (adjust if you add a requirements.txt)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir fastapi pydantic requests uvicorn python-dotenv

# Expose the port used by the proxy (8002)
EXPOSE 8002

# Run the proxy-classifier app using uvicorn (reload is enabled for development)
CMD ["uvicorn", "proxy-classifier:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]