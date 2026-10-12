FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --locked --no-dev
EXPOSE 8501
CMD ["uv", "run", "--no-dev", "streamlit", "run", "src/tcc2_dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
