# Excel Pipeline API

FastAPI service that uploads an Excel file, enqueues a Redis-backed job, and processes a 3-stage pipeline.

## Requirements
- Redis running locally (for local run)
- Python 3.10+
- Docker + Docker Compose (for container run)

## Install (Local)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (Local)
```bash
# terminal 1
redis-server

# terminal 2 (worker)
python3 worker.py

# terminal 3 (api)
gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app
```

## Run (Docker)
```bash
docker compose up --build
```

API will be available at `http://localhost:8000`.

## Scale Workers (Docker)
```bash
docker compose up --build --scale worker=4
```

Change `4` based on CPU and throughput targets.
Each worker replica consumes jobs from Redis in parallel.
`api` and `worker` share a Docker volume for uploaded and output files.

## API
- `POST /upload` (multipart form)
  - `file`: Excel file
  - `config` (optional JSON string)
  - `callback_url` (optional)

Example config:
```json
{
  "enabled_stages": ["stage1", "stage2", "stage3"],
  "order": ["stage1", "stage2", "stage3"],
  "parallel_groups": null
}
```

- `GET /jobs/{job_id}`
- `GET /jobs/{job_id}/result`

## Notes
- Stages are defined in `core/stages.py`.
- Dependencies are enforced by the pipeline engine in `core/pipeline.py`.
- Parallel groups allow running independent stages concurrently.

## SOLID-Oriented Structure
- `app/main.py` only handles HTTP concerns (SRP).
- `app/services.py` contains business use-cases (`JobSubmissionService`, `JobQueryService`, `JobProcessingService`).
- `core/contracts.py` defines abstractions for repository, storage, queue, executor, and notifier (DIP + ISP).
- `infrastructure/repository.py`, `infrastructure/file_storage.py`, `infrastructure/queue.py`, `infrastructure/notifier.py` provide concrete adapters (OCP).
- `core/interfaces.py` and stage implementations preserve substitutability for pipeline stages (LSP).
