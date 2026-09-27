FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PYTHONPATH=/app/src

WORKDIR /app

RUN apt-get update

COPY pyproject.toml ./
COPY README.md ./
COPY src ./src
COPY img ./img

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "eink_f1.main:app", "--host", "0.0.0.0", "--port", "8000"]
