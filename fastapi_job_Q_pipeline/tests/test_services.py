from __future__ import annotations

import unittest
from unittest.mock import Mock, call

from app.services import (
    JobNotCompletedError,
    JobNotFoundError,
    JobOutputMissingError,
    JobProcessingService,
    JobQueryService,
    JobSubmissionService,
)


class TestJobSubmissionService(unittest.TestCase):
    def test_submit_creates_job_and_enqueues(self) -> None:
        repository = Mock()
        storage = Mock()
        queue = Mock()

        storage.save_upload.return_value = "/tmp/input.xlsx"
        service = JobSubmissionService(
            repository=repository,
            storage=storage,
            queue=queue,
            job_id_provider=lambda: "job-123",
        )

        job_id = service.submit(
            filename="input.xlsx",
            file_content=b"bytes",
            pipeline_config={"enabled_stages": ["stage1", "stage2"]},
            callback_url="https://example.com/callback",
        )

        self.assertEqual(job_id, "job-123")
        storage.save_upload.assert_called_once_with("input.xlsx", b"bytes")
        repository.create_job.assert_called_once_with(
            "job-123",
            {
                "input_path": "/tmp/input.xlsx",
                "pipeline_config": {"enabled_stages": ["stage1", "stage2"]},
                "callback_url": "https://example.com/callback",
            },
        )
        queue.enqueue.assert_called_once_with("job-123")


class TestJobQueryService(unittest.TestCase):
    def test_get_job_returns_job(self) -> None:
        repository = Mock()
        repository.get_job.return_value = {"status": "RUNNING"}

        service = JobQueryService(repository)
        job = service.get_job("job-1")

        self.assertEqual(job["status"], "RUNNING")
        repository.get_job.assert_called_once_with("job-1")

    def test_get_job_raises_when_not_found(self) -> None:
        repository = Mock()
        repository.get_job.return_value = None

        service = JobQueryService(repository)

        with self.assertRaises(JobNotFoundError):
            service.get_job("missing")

    def test_get_result_path_raises_when_not_completed(self) -> None:
        repository = Mock()
        repository.get_job.return_value = {"status": "RUNNING"}

        service = JobQueryService(repository)

        with self.assertRaises(JobNotCompletedError):
            service.get_result_path("job-2")

    def test_get_result_path_raises_when_output_missing(self) -> None:
        repository = Mock()
        repository.get_job.return_value = {
            "status": "COMPLETED",
            "result": {},
        }

        service = JobQueryService(repository)

        with self.assertRaises(JobOutputMissingError):
            service.get_result_path("job-3")

    def test_get_result_path_returns_path(self) -> None:
        repository = Mock()
        repository.get_job.return_value = {
            "status": "COMPLETED",
            "result": {"output_path": "/tmp/output.csv"},
        }

        service = JobQueryService(repository)
        output_path = service.get_result_path("job-4")

        self.assertEqual(output_path, "/tmp/output.csv")


class TestJobProcessingService(unittest.TestCase):
    def test_process_returns_when_job_missing(self) -> None:
        repository = Mock()
        storage = Mock()
        executor = Mock()
        notifier = Mock()

        repository.get_job.return_value = None

        service = JobProcessingService(repository, storage, executor, notifier)
        service.process("missing-job")

        repository.update_job.assert_not_called()
        executor.run.assert_not_called()
        notifier.notify.assert_not_called()

    def test_process_success_updates_status_and_notifies(self) -> None:
        repository = Mock()
        storage = Mock()
        executor = Mock()
        notifier = Mock()

        repository.get_job.return_value = {
            "input_path": "/tmp/input.xlsx",
            "callback_url": "https://example.com/callback",
            "pipeline_config": {
                "enabled_stages": ["stage1", "stage2", "stage3"],
                "order": ["stage1", "stage2", "stage3"],
                "parallel_groups": None,
            },
        }
        storage.build_output_path.return_value = "/tmp/output.csv"
        executor.run.return_value = {
            "stage1": "ok",
            "stage2": "ok",
            "stage3": "/tmp/output.csv",
        }

        service = JobProcessingService(repository, storage, executor, notifier)
        service.process("job-5")

        repository.update_job.assert_has_calls(
            [
                call("job-5", {"status": "RUNNING"}),
                call(
                    "job-5",
                    {
                        "status": "COMPLETED",
                        "result": {
                            "output_path": "/tmp/output.csv",
                            "stages": ["stage1", "stage2", "stage3"],
                        },
                    },
                ),
            ]
        )
        storage.build_output_path.assert_called_once_with("job-5")
        storage.ensure_path.assert_called_once_with("/tmp/output.csv")
        executor.run.assert_called_once_with(
            context={
                "job_id": "job-5",
                "input_path": "/tmp/input.xlsx",
                "output_path": "/tmp/output.csv",
            },
            enabled=["stage1", "stage2", "stage3"],
            order=["stage1", "stage2", "stage3"],
            parallel_groups=None,
        )
        notifier.notify.assert_called_once_with(
            "https://example.com/callback",
            "job-5",
            {"output_path": "/tmp/output.csv", "stages": ["stage1", "stage2", "stage3"]},
        )

    def test_process_failure_marks_failed_and_notifies(self) -> None:
        repository = Mock()
        storage = Mock()
        executor = Mock()
        notifier = Mock()

        repository.get_job.return_value = {
            "input_path": "/tmp/input.xlsx",
            "callback_url": "https://example.com/callback",
            "pipeline_config": {},
        }
        storage.build_output_path.return_value = "/tmp/output.csv"
        executor.run.side_effect = RuntimeError("boom")

        service = JobProcessingService(repository, storage, executor, notifier)
        service.process("job-6")

        self.assertEqual(repository.update_job.call_count, 2)
        first_call = repository.update_job.call_args_list[0]
        second_call = repository.update_job.call_args_list[1]

        self.assertEqual(first_call, call("job-6", {"status": "RUNNING"}))
        self.assertEqual(second_call.args[0], "job-6")
        failure_payload = second_call.args[1]
        self.assertEqual(failure_payload["status"], "FAILED")
        self.assertEqual(failure_payload["error"], "boom")
        self.assertIn("traceback", failure_payload)

        notifier.notify.assert_called_once_with(
            "https://example.com/callback",
            "job-6",
            {"status": "FAILED", "error": "boom"},
        )


if __name__ == "__main__":
    unittest.main()
