import threading, time
from contextlib import contextmanager

lock_1 = threading.Lock()
lock_2 = threading.Lock()
lock_3 = threading.Lock()

# @contextmanager
def acquire_multiple_locks(*locks):
    """
    Context manager to acquire multiple locks safely
    Always acquires in sorted order to prevent circular wait
    """
    # Sort locks by id for consistent order
    sorted_locks = sorted(locks, key=id)
    
    # Acquire all locks
    for lock in sorted_locks:
        lock.acquire()
    
    try:
        yield sorted_locks
    finally:
        # Release in reverse order
        for lock in reversed(sorted_locks):
            lock.release()

def safe_thread():
    """Use context manager for safe multi-lock acquisition"""
    with acquire_multiple_locks(lock_1, lock_2, lock_3) as managed_locks:
        print("Thread: Acquired all locks safely", managed_locks)
        time.sleep(1)
        print("Thread: Done!")

# Run threads
threads = [threading.Thread(target=safe_thread) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
