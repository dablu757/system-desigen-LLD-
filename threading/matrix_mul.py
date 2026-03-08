import random
import threading
import time
from multiprocessing import Pool, cpu_count, freeze_support

N = 200

# Globals used only by multiprocessing workers (set via initializer).
_MP_A = None
_MP_B = None
_MP_N = None


def generate_matrices(n: int) -> tuple[list[list[int]], list[list[int]]]:
    a = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    b = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    return a, b


def multiply_single(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    n = len(a)
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += a[i][k] * b[k][j]
            c[i][j] = total
    return c


def multiply_threaded(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    n = len(a)
    c = [[0] * n for _ in range(n)]

    def multiply_row_thread(i: int) -> None:
        for j in range(n):
            total = 0
            for k in range(n):
                total += a[i][k] * b[k][j]
            c[i][j] = total

    threads: list[threading.Thread] = []
    for i in range(n):
        t = threading.Thread(target=multiply_row_thread, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return c


def _init_worker(a: list[list[int]], b: list[list[int]], n: int) -> None:
    global _MP_A, _MP_B, _MP_N
    _MP_A = a
    _MP_B = b
    _MP_N = n


def _multiply_row_mp(i: int) -> list[int]:
    row: list[int] = []
    for j in range(_MP_N):
        total = 0
        for k in range(_MP_N):
            total += _MP_A[i][k] * _MP_B[k][j]
        row.append(total)
    return row


def multiply_multiprocessing(
    a: list[list[int]], b: list[list[int]], processes: int | None = None
) -> list[list[int]]:
    n = len(a)
    proc_count = processes or cpu_count()
    with Pool(proc_count, initializer=_init_worker, initargs=(a, b, n)) as pool:
        return pool.map(_multiply_row_mp, range(n))


def benchmark() -> None:
    a, b = generate_matrices(N)

    start = time.perf_counter()
    _ = multiply_single(a, b)
    end = time.perf_counter()
    print("Single Thread Time:", end - start)

    start = time.perf_counter()
    _ = multiply_threaded(a, b)
    end = time.perf_counter()
    print("Thread Time:", end - start)

    start = time.perf_counter()
    _ = multiply_multiprocessing(a, b)
    end = time.perf_counter()
    print("Multiprocessing Time:", end - start)


if __name__ == "__main__":
    # Required for spawn-based multiprocessing environments (macOS/Windows).
    freeze_support()
    benchmark()
