# Matrix Multiplication Performance - Interview Prep Notes

Context: In our Python benchmark (`threading/matrix_mul.py`), timings were roughly:
- Single Thread: `~0.279s`
- Threading: `~0.289s`
- Multiprocessing: `~0.362s`

## 1) Direct Interview Answer (30-45 sec)

Single-thread is faster here because this implementation is pure Python CPU-bound loops.
`threading` does not help much due to the GIL, so threads cannot run Python bytecode truly in parallel for this workload. It also adds thread management/context-switch overhead.
`multiprocessing` can run in parallel, but on macOS/Python 3.12 it uses `spawn`, which has high process startup and serialization cost. For this matrix size (`N=200`), overhead is larger than compute benefit.

## 2) Deeper Explanation

## Why threading is not faster
- Work type is CPU-bound (nested loops in Python).
- GIL allows only one thread to execute Python bytecode at a time.
- Extra overhead:
  - creating many threads
  - scheduling/context switching
  - synchronization/joining

Result: small slowdown vs single-thread is expected.

## Why multiprocessing is not faster here
- Worker process creation cost (spawn model).
- Data sharing overhead (pickling/copying large matrices to workers).
- Task granularity is small (row-wise tasks); coordination overhead dominates.

Result: parallelism exists, but overhead dominates at this problem size.

## 3) What to Say If Asked: "When will multiprocessing win?"

Multiprocessing wins when:
- per-task CPU work is large,
- process startup cost is amortized,
- data transfer overhead is reduced,
- and task batching is coarse enough.

Example: much larger `N` (e.g., 800+ or 1000+), chunked workloads, and reusable process pools.

## 4) Optimization Talking Points

1. Use `numpy.dot` / BLAS for matrix multiplication (best practical answer).
2. Increase matrix size before comparing parallel approaches.
3. Use chunk-based multiprocessing (multiple rows per task).
4. Reuse the process pool across repeated runs.
5. Avoid heavy serialization (shared memory / memory-mapped arrays).

## 5) Interview Q&A Cheat Sheet

## Q: Why did threads not speed up CPU-bound code?
Because of Python GIL for CPython; only one thread runs Python bytecode at once.

## Q: Why is multiprocessing slower than expected?
Because startup + IPC/serialization overhead can exceed compute time for smaller jobs.

## Q: Is multiprocessing always better for CPU-bound tasks?
No. Better only when compute is large enough to amortize overhead.

## Q: Best production approach for matrix multiply in Python?
Use `numpy`/`scipy` backed by optimized native libraries (BLAS/LAPACK), not Python triple loops.

## 6) One-Liner Summary

For `N=200` pure-Python matrix multiply, overhead dominates parallelism benefits; therefore single-thread can be faster than both threading and multiprocessing.
