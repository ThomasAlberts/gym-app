FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

# Install deps first so this layer is cached unless pyproject/uv.lock change
COPY backend/pyproject.toml backend/uv.lock ./backend/
RUN cd backend && uv sync --frozen --no-install-project

# Copy the rest of the backend source
COPY backend ./backend

EXPOSE 8000

# backend.main:app is imported relative to /app, matching how you run it
# locally from the gym-app root ("uv run uvicorn backend.main:app")
CMD ["/app/backend/.venv/bin/python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
