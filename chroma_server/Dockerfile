FROM python:3.10-slim

WORKDIR /app

# Copy vector store and requirements
COPY chroma_style_guide_store /app/chroma_style_guide_store
COPY requirements.txt .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["chroma", "run", "--host", "0.0.0.0", "--port", "8000", "--path", "/app/chroma_langchain_store"]
