.PHONY: install run lint fmt typecheck test check docker
install:
	uv sync
run:
	uv run streamlit run src/tcc2_dashboard/app.py
lint:
	uv run ruff check .
fmt:
	uv run ruff check --fix . && uv run ruff format .
typecheck:
	uv run mypy src
test:
	uv run pytest --cov=tcc2_dashboard
check: lint typecheck test
docker:
	docker build -t tcc2-dashboard . && docker run --rm -p 8501:8501 tcc2-dashboard
