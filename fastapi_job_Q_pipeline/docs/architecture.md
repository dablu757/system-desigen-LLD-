# Excel Pipeline Architecture

This document captures the High-Level Design (HLD), Low-Level Design (LLD), UML, and Data Flow Diagram for the project.

## HLD

### System Overview
- Frontend uploads Excel through `POST /upload`.
- FastAPI validates input, stores the file, writes initial job metadata, and enqueues job id in Redis-backed RQ.
- Worker replicas consume job ids, execute pipeline stages, and update job state/result.
- Client checks progress with `GET /jobs/{job_id}` and downloads output with `GET /jobs/{job_id}/result`.
- Optional callback URL is notified when processing finishes.

### Architecture Diagram
```mermaid
flowchart LR
  FE["Frontend Client"]
  LB["Load Balancer"]
  API["FastAPI API (Gunicorn + Uvicorn Workers)"]
  RQ["Redis Queue (RQ)"]
  RS["Redis Job Store"]
  WK["Worker Replicas (RQ Workers)"]
  FS["Shared Storage Volume"]
  CB["Client Callback Endpoint"]

  FE -->|"POST /upload (excel, config, callback_url)"| LB
  LB --> API
  API -->|"save upload file"| FS
  API -->|"create job metadata"| RS
  API -->|"enqueue job_id"| RQ
  WK -->|"dequeue job_id"| RQ
  WK -->|"read/update job state"| RS
  WK -->|"read input and write output.csv"| FS
  WK -->|"POST completion payload"| CB
  FE -->|"GET /jobs/{job_id}"| API
  FE -->|"GET /jobs/{job_id}/result"| API
  API -->|"read status/result"| RS
  API -->|"stream output.csv"| FE
```

## LLD

### Module Responsibilities
| Layer | File | Responsibility |
|---|---|---|
| API | `app/main.py` | HTTP endpoints only. |
| Composition Root | `app/dependencies.py` | Wires concrete adapters into services. |
| Use Cases | `app/services.py` | Submission, querying, processing workflows. |
| Contracts | `core/contracts.py` | Abstractions for repo, storage, queue, executor, notifier. |
| Pipeline Engine | `core/pipeline.py` | Dependency validation and execution planning. |
| Stage Contract | `core/interfaces.py` | Stage abstraction for all stage implementations. |
| Stage Implementations | `core/stages.py` | Stage1 load/normalize, Stage2 CPU transform, Stage3 output write. |
| Executor | `core/executors.py` | Creates stage map and runs pipeline. |
| Infra Adapter | `infrastructure/repository.py` | Redis-backed job repository. |
| Infra Adapter | `infrastructure/queue.py` | RQ enqueue adapter. |
| Infra Adapter | `infrastructure/file_storage.py` | Shared file storage adapter. |
| Infra Adapter | `infrastructure/notifier.py` | HTTP callback notifier. |
| Worker Entrypoint | `app/tasks.py` | Worker task invoking processing service. |

### Processing Flow
1. `POST /upload` parses config and file.
2. `JobSubmissionService.submit` saves file, creates job metadata, enqueues job.
3. Worker executes `run_pipeline_job`.
4. `JobProcessingService.process` updates status to `RUNNING`, executes pipeline, stores result as `COMPLETED` or `FAILED`, then notifies callback if provided.
5. Client reads job status or downloads generated CSV.

## UML

### Class Diagram
```mermaid
classDiagram
  class JobRepositoryContract {
    <<interface>>
    +create_job(job_id, data)
    +update_job(job_id, data)
    +get_job(job_id)
  }

  class FileStorageContract {
    <<interface>>
    +save_upload(filename, file_content)
    +build_output_path(job_id)
    +ensure_path(path)
  }

  class JobQueueContract {
    <<interface>>
    +enqueue(job_id)
  }

  class PipelineExecutorContract {
    <<interface>>
    +run(context, enabled, order, parallel_groups)
  }

  class CompletionNotifierContract {
    <<interface>>
    +notify(callback_url, job_id, payload)
  }

  class JobSubmissionService {
    +submit(filename, file_content, pipeline_config, callback_url)
  }

  class JobQueryService {
    +get_job(job_id)
    +get_result_path(job_id)
  }

  class JobProcessingService {
    +process(job_id)
  }

  class RedisJobRepository
  class LocalFileStorage
  class RQJobQueue
  class HttpCallbackNotifier
  class PipelineExecutor
  class Pipeline
  class Stage {
    <<interface>>
    +run(context, results)
  }
  class Stage1LoadAndNormalize
  class Stage2CpuTransform
  class Stage3WriteOutput

  JobSubmissionService --> JobRepositoryContract
  JobSubmissionService --> FileStorageContract
  JobSubmissionService --> JobQueueContract
  JobQueryService --> JobRepositoryContract
  JobProcessingService --> JobRepositoryContract
  JobProcessingService --> FileStorageContract
  JobProcessingService --> PipelineExecutorContract
  JobProcessingService --> CompletionNotifierContract

  RedisJobRepository ..|> JobRepositoryContract
  LocalFileStorage ..|> FileStorageContract
  RQJobQueue ..|> JobQueueContract
  HttpCallbackNotifier ..|> CompletionNotifierContract
  PipelineExecutor ..|> PipelineExecutorContract

  PipelineExecutor --> Pipeline
  Pipeline --> Stage
  Stage1LoadAndNormalize ..|> Stage
  Stage2CpuTransform ..|> Stage
  Stage3WriteOutput ..|> Stage
```

### Sequence Diagram
```mermaid
sequenceDiagram
  participant C as "Client"
  participant A as "FastAPI API"
  participant S as "JobSubmissionService"
  participant F as "FileStorage"
  participant R as "RedisJobRepository"
  participant Q as "RQJobQueue"
  participant W as "Worker"
  participant P as "JobProcessingService"
  participant E as "PipelineExecutor"
  participant N as "CallbackNotifier"

  C->>A: "POST /upload (excel, config, callback_url)"
  A->>S: "submit(...)"
  S->>F: "save_upload(...)"
  S->>R: "create_job(status=QUEUED)"
  S->>Q: "enqueue(job_id)"
  A-->>C: "job_id, status=QUEUED"

  W->>P: "process(job_id)"
  P->>R: "get_job(job_id)"
  P->>R: "update_job(status=RUNNING)"
  P->>E: "run(context, enabled/order/parallel_groups)"
  E-->>P: "results"
  P->>R: "update_job(status=COMPLETED, result)"
  P->>N: "notify(callback_url, payload)"
```

## Data Flow Diagram
```mermaid
flowchart TD
  E1["External Entity: Frontend"]
  E2["External Entity: Callback Receiver"]

  P1["Process: Upload API"]
  P2["Process: Worker Pipeline Processing"]
  P3["Process: Status and Result API"]

  D1["Data Store: Redis Job Metadata"]
  D2["Data Store: Redis Queue"]
  D3["Data Store: Shared File Storage"]

  E1 -->|"excel file + pipeline config"| P1
  P1 -->|"job metadata (QUEUED, config, paths)"| D1
  P1 -->|"job_id message"| D2
  P1 -->|"uploaded excel file"| D3
  P1 -->|"job_id response"| E1

  D2 -->|"job_id"| P2
  D1 -->|"job config + input path"| P2
  D3 -->|"input excel"| P2
  P2 -->|"RUNNING/COMPLETED/FAILED + result"| D1
  P2 -->|"output.csv"| D3
  P2 -->|"completion payload"| E2

  E1 -->|"status/result request"| P3
  P3 -->|"read job metadata"| D1
  P3 -->|"read output.csv"| D3
  P3 -->|"status/result response"| E1
```
