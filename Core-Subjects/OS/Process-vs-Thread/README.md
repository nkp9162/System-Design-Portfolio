# Process vs Thread - Complete Guide

## Table of Contents
1. [Introduction](#introduction)
2. [What is a Process?](#what-is-a-process)
3. [What is a Thread?](#what-is-a-thread)
4. [File Descriptors (FD)](#file-descriptors)
5. [Process vs Thread - Key Differences](#process-vs-thread---key-differences)
6. [Real-World Examples](#real-world-examples)
7. [Internal Working & Memory](#internal-working--memory)
8. [Code Implementation](#code-implementation)
   - [Multiprocessing in Python](#multiprocessing-in-python)
   - [Threading in Python](#threading-in-python)
   - [Asyncio in Python](#asyncio-in-python)
9. [When to Use What?](#when-to-use-what)
10. [Process Pool vs Thread Pool](#process-pool-vs-thread-pool)
11. [Distributed Systems - Queue-Based Task Processing](#distributed-systems---queue-based-task-processing)
12. [Celery: The Distributed Task Orchestrator](#celery-the-distributed-task-orchestrator)
13. [Interview Questions](#interview-questions)
---

## Introduction

**Process** and **Thread** both are program execution units, but there are fundamental differences between them in terms of memory sharing, resource allocation, and overhead.

---

## What is a Process?

### Definition
**Process** is an independent program that executes with its own memory space. Every process has its own code, data, heap, and stack.

### Real-World Example
```
Microsoft Word, Chrome Browser, Spotify - these are all separate processes.
If Word crashes, Chrome will not be affected.
```

### Key Characteristics
- ✅ **Independent** - has its own memory space
- ✅ **Isolated** - one process cannot access another process's memory
- ✅ **Heavy** - creating a process is a costly operation (memory allocation)
- ✅ **Secure** - if one process crashes, other processes remain safe

### What Does a Process Have?
```
Process Components:
├── Code Section (Text) - Program instructions
├── Data Section - Global variables
├── Heap - Dynamic memory allocation
├── Stack - Function calls, local variables
├── Program Counter (PC) - Next instruction address
├── CPU Registers - Current processing state
└── File Descriptors - Open files, network connections
```

---

## What is a Thread?

### Definition
**Thread** is a lightweight execution unit that runs inside a process. Multiple threads share the memory of the same process.

### Real-World Example
```
Inside Chrome Browser (1 Process):
├── Thread 1: UI rendering
├── Thread 2: JavaScript execution
├── Thread 3: Network requests
└── Thread 4: Extensions handling

All threads share the same memory, so communication is faster.
```

### Key Characteristics
- ✅ **Lightweight** - uses fewer resources than a process
- ✅ **Shared Memory** - threads of the same process share memory
- ✅ **Fast** - thread creation and context switching are fast
- ✅ **Dependent** - if one thread crashes, the entire process may crash

### What Does a Thread Have?
```
Thread Components (Each thread has its own):
├── Thread ID
├── Program Counter (PC) - Current instruction
├── Stack - Function calls, local variables
├── Registers - CPU state for this thread
└── Thread-specific data

Shared Among All Threads in a Process:
├── Code Section
├── Data Section (Global variables)
├── Heap
└── File Descriptors
```

---

## 📂 File Descriptors (FD)

### Definition
In Unix-like operating systems, **"Everything is a file"**. A File Descriptor is a **low-level integer (handle)** used by a process to identify an open file or an I/O resource (like a network socket, pipe, or terminal).

### How it Works
When a process requests to open a file, the OS:
1. Grants access to the resource.
2. Creates an entry in the **File Descriptor Table**.
3. Returns a **non-negative integer** (Token) to the process.



### Standard File Descriptors
Every process starts with three default FDs:
* **0 (stdin):** Standard Input (Keyboard)
* **1 (stdout):** Standard Output (Terminal/Screen)
* **2 (stderr):** Standard Error (Error messages on Screen)

### Key Concepts
- **FD Leak:** Occurs when a program opens files/sockets but fails to `close()` them, eventually hitting the OS limit (e.g., 1024).
- **Isolation:** Each process has its own private FD table.
- **Networking:** Sockets are also treated as File Descriptors, allowing `read()` and `write()` operations just like files.

---

## Process vs Thread - Key Differences

| Feature | Process | Thread |
|---------|---------|--------|
| **Definition** | Independent program | Lightweight unit inside process |
| **Memory** | Separate memory space | Shared memory space |
| **Creation Time** | Slow (expensive) | Fast (cheap) |
| **Context Switch** | Slower | Faster |
| **Communication** | IPC (Pipes, Sockets) - slow | Shared memory - fast |
| **Isolation** | Fully isolated | Not isolated (shared resources) |
| **Crash Impact** | Only that process crashes | Entire process crashes |
| **Use Case** | CPU-bound tasks (parallel processing) | I/O-bound tasks (waiting operations) |
| **Example** | Multiple Chrome instances | Tabs in one Chrome window |

---

## Real-World Examples

### Example 1: Restaurant Analogy
```
Process = Individual Restaurants
├── Restaurant A (Process 1) - Own kitchen, staff, inventory
└── Restaurant B (Process 2) - Own kitchen, staff, inventory

Thread = Waiters in One Restaurant
├── Waiter 1 (Thread 1) - Takes orders
├── Waiter 2 (Thread 2) - Serves food
└── Waiter 3 (Thread 3) - Handles billing

All waiters share same kitchen (memory), but each has own notepad (stack).
```

### Example 2: Movie Ticket Booking System
```python
# Process-level: Multiple Django servers handling requests (separate processes)
Server 1 (Process) → Handles users from Region A
Server 2 (Process) → Handles users from Region B

# Thread-level: Inside one Django server
Thread 1 → Serve request for User 1
Thread 2 → Serve request for User 2
Thread 3 → Serve request for User 3

All threads share database connection pool, cache (shared memory).
```

---

## Internal Working & Memory

### Process Memory Layout
```
High Address
┌─────────────────────┐
│   Command-line args │  
├─────────────────────┤
│   Environment vars  │
├─────────────────────┤
│       Stack         │  ← Grows downward (function calls, local vars)
│         ↓           │
│                     │
│       (Free)        │
│                     │
│         ↑           │
│       Heap          │  ← Grows upward (dynamic allocation - malloc)
├─────────────────────┤
│  Uninitialized Data │  (BSS - static/global uninitialized)
├─────────────────────┤
│   Initialized Data  │  (Data segment - global/static initialized)
├─────────────────────┤
│    Text (Code)      │  (Read-only program instructions)
└─────────────────────┘
Low Address
```

### Thread Memory Sharing
```
Process Memory Space (Shared by all threads):
┌─────────────────────────────────────┐
│         Code Section (Shared)        │  ← All threads execute same code
├─────────────────────────────────────┤
│         Data Section (Shared)        │  ← Global variables
├─────────────────────────────────────┤
│         Heap (Shared)                │  ← Dynamic allocations
├─────────────────────────────────────┤
│                                      │
│   Thread 1 Stack (Private)           │  ← Each thread has own stack
│   Thread 2 Stack (Private)           │
│   Thread 3 Stack (Private)           │
│                                      │
└─────────────────────────────────────┘

Each thread also has:
- Own Program Counter (PC)
- Own CPU Registers
- Own Stack Pointer
```

### Why This Matters?
```python
# Global variable (Shared - in Data Section)
counter = 0

def increment():
    global counter
    # All threads can access 'counter' - RACE CONDITION possible!
    counter += 1

# Thread 1 and Thread 2 can both access 'counter'
# Without a lock, data corruption can happen
```

---

## Code Implementation

### Multiprocessing in Python

**When to Use:** CPU-bound tasks (computation heavy - data processing, ML training, image processing)
```python
import multiprocessing
import time

# CPU-bound task
def heavy_computation(n):
    """Simulate CPU-intensive work"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

if __name__ == "__main__":
    numbers = [10000000, 10000000, 10000000, 10000000]
    
    # Sequential execution
    start = time.time()
    results = [heavy_computation(n) for n in numbers]
    print(f"Sequential: {time.time() - start:.2f}s")
    
    # Parallel execution using multiprocessing
    start = time.time()
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(heavy_computation, numbers)
    print(f"Multiprocessing: {time.time() - start:.2f}s")
    
    # Output:
    # Sequential: 8.50s
    # Multiprocessing: 2.30s (4 cores used parallely)
```

**Why Multiprocessing for CPU-bound?**
- Python has **GIL (Global Interpreter Lock)** - only one thread executes Python bytecode at a time
- Processes bypass GIL - true parallelism on multi-core CPUs
- Each process runs on separate CPU core

---

### Threading in Python

**When to Use:** I/O-bound tasks (network calls, file operations, database queries)
```python
import threading
import time
import requests

# I/O-bound task
def fetch_url(url):
    """Simulate network request"""
    response = requests.get(url)
    print(f"Fetched {url}: {len(response.content)} bytes")

if __name__ == "__main__":
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
    ]
    
    # Sequential execution
    start = time.time()
    for url in urls:
        fetch_url(url)
    print(f"Sequential: {time.time() - start:.2f}s")
    
    # Threading execution
    start = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=fetch_url, args=(url,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print(f"Threading: {time.time() - start:.2f}s")
    
    # Output:
    # Sequential: 4.20s
    # Threading: 1.10s (parallel I/O waiting)
```

**Why Threading for I/O-bound?**
- Threads share memory - fast communication
- While one thread waits for I/O, others can execute
- GIL doesn't matter because threads spend time waiting (not executing Python code)

---

### Asyncio in Python

**When to Use:** High concurrency I/O-bound tasks (thousands of connections - web servers, websockets, async APIs)
```python
import asyncio
import aiohttp
import time

# Async I/O-bound task
async def fetch_url_async(session, url):
    """Async network request"""
    async with session.get(url) as response:
        content = await response.read()
        print(f"Fetched {url}: {len(content)} bytes")

async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url_async(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"Asyncio: {time.time() - start:.2f}s")
    
    # Output:
    # Asyncio: 0.80s (even faster than threading - single thread, cooperative multitasking)
```

**Why Asyncio?**
- **Single-threaded** but concurrent (event loop)
- Lightweight - can handle 10,000+ connections
- No thread overhead, no race conditions
- Perfect for web servers (FastAPI, Django Async)

---

## When to Use What?

### Decision Tree
```
┌─────────────────────────────────────┐
│   What type of task?                │
└──────────┬──────────────────────────┘
           │
    ┌──────┴──────────────┐
    │                     │
CPU-bound?            I/O-bound?
    │                     │
    │              ┌──────┴──────┐
    │              │             │
    │           Few tasks?    Many tasks (1000+)?
    │              │             │
    │              │             │
    ▼              ▼             ▼
Multiprocessing  Threading    Asyncio
```

### Comparison Table

| Use Case | Best Choice | Why? |
|----------|-------------|------|
| **Image Processing** | Multiprocessing | CPU-intensive, needs parallel cores |
| **Data Science (Pandas)** | Multiprocessing | Heavy computation on data |
| **Web Scraping (10 URLs)** | Threading | I/O-bound, waiting for network |
| **Web Server (FastAPI)** | Asyncio | High concurrency, thousands of connections |
| **File Upload/Download** | Threading or Asyncio | I/O-bound, network waiting |
| **Database Bulk Insert** | Threading | I/O-bound, waiting for DB |
| **Video Encoding** | Multiprocessing | CPU-intensive computation |
| **Chatbot (WebSockets)** | Asyncio | High concurrency, real-time |

### Code Example: When to Use What
```python
# ❌ BAD: Using threading for CPU-bound
def bad_cpu_task():
    # Threading won't help due to GIL
    # All threads will compete for single CPU core
    threads = [threading.Thread(target=heavy_computation, args=(10000000,)) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()

# ✅ GOOD: Using multiprocessing for CPU-bound
def good_cpu_task():
    with multiprocessing.Pool(4) as pool:
        pool.map(heavy_computation, [10000000] * 4)

# ❌ BAD: Using multiprocessing for I/O-bound
def bad_io_task():
    # Too much overhead creating processes for simple I/O
    with multiprocessing.Pool(4) as pool:
        pool.map(fetch_url, urls)

# ✅ GOOD: Using asyncio for I/O-bound
async def good_io_task():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch_url_async(session, url) for url in urls])
```

---

## Process Pool vs Thread Pool

### Thread Pool Executor
```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(n):
    time.sleep(1)
    return n * n

# Thread Pool - Reuses threads (no creation overhead)
with ThreadPoolExecutor(max_workers=4) as executor:
    # Submit tasks
    futures = [executor.submit(task, i) for i in range(10)]
    
    # Get results
    for future in futures:
        print(future.result())

# Benefits:
# - Thread creation expensive, pool reuses threads
# - Better than creating 10 separate threads
# - Automatic cleanup
```

### Process Pool Executor
```python
from concurrent.futures import ProcessPoolExecutor

def cpu_task(n):
    return sum(i ** 2 for i in range(n))

# Process Pool - Reuses processes
with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(cpu_task, [10000000] * 4)
    print(list(results))

# Benefits:
# - Process creation very expensive, pool reuses
# - Distributes work across CPU cores
# - Automatic cleanup
```

### Why Pools are Better?
```
Without Pool:
Task 1 → Create Thread → Execute → Destroy Thread
Task 2 → Create Thread → Execute → Destroy Thread  ← Overhead!
Task 3 → Create Thread → Execute → Destroy Thread

With Pool (4 workers):
Task 1,2,3,4 → Assigned to 4 threads (already created)
Task 5,6,7,8 → Same 4 threads reused
Task 9,10    → Same 4 threads reused  ← No creation overhead!
```

---

## Distributed Systems - Queue-Based Task Processing

### Why Queues are Better than Pools in Distributed Systems?
```
Problem with Pools:
- Limited to single machine (1 server, 4 cores = 4 parallel tasks)
- Can't scale horizontally
- If server crashes, all tasks lost

Solution with Queues:
- Multiple worker servers
- Fault-tolerant (tasks persist in queue)
- Horizontal scaling (add more workers)
```

### Architecture
```
                    ┌─────────────────┐
                    │   Django App    │
                    │   (Producer)    │
                    └────────┬────────┘
                             │
                             │ Publish task
                             ▼
                    ┌──────────────────┐
                    │  Redis / RabbitMQ│
                    │     (Queue)      │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │Worker 1 │        │Worker 2 │        │Worker 3 │
    │(Celery) │        │(Celery) │        │(Celery) │
    └─────────┘        └─────────┘        └─────────┘
   (Server A)         (Server B)         (Server C)
```

### Producer-Consumer Model with Redis Queue

#### Producer (Django/FastAPI - Publishes Tasks)
```python
# producer.py - FastAPI endpoint
from fastapi import FastAPI
import redis
import json

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.post("/send-email")
async def send_email(email: str, message: str):
    """Producer - Adds task to queue"""
    task = {
        "email": email,
        "message": message,
        "timestamp": time.time()
    }
    
    # Push task to Redis queue
    redis_client.lpush("email_queue", json.dumps(task))
    
    return {"status": "Task queued", "task": task}

# Usage:
# POST http://localhost:8000/send-email
# Body: {"email": "user@example.com", "message": "Hello!"}
```

#### Consumer (Worker - Processes Tasks)
```python
# worker.py - Consumer that processes tasks
import redis
import json
import time

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def send_email_actual(email, message):
    """Actual email sending logic"""
    print(f"Sending email to {email}: {message}")
    time.sleep(2)  # Simulate email sending
    print(f"Email sent to {email}")

def worker():
    """Consumer - Processes tasks from queue"""
    print("Worker started. Waiting for tasks...")
    
    while True:
        # Block and wait for task (BRPOP - blocking right pop)
        task_data = redis_client.brpop("email_queue", timeout=5)
        
        if task_data:
            queue_name, task_json = task_data
            task = json.loads(task_json)
            
            print(f"Processing task: {task}")
            send_email_actual(task['email'], task['message'])
        else:
            print("No tasks. Waiting...")

if __name__ == "__main__":
    worker()

# Run multiple workers:
# Terminal 1: python worker.py
# Terminal 2: python worker.py
# Terminal 3: python worker.py
# All 3 workers will consume from same queue
```

### Real Production Example with Celery
```python
# tasks.py - Celery tasks
from celery import Celery

# Celery app with Redis broker
app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def send_booking_confirmation(user_id, booking_id):
    """Background task - send email"""
    # Email sending logic
    print(f"Sending confirmation to user {user_id} for booking {booking_id}")
    time.sleep(3)
    return f"Email sent for booking {booking_id}"

@app.task
def process_payment(order_id, amount):
    """Background task - process payment"""
    print(f"Processing payment for order {order_id}: ${amount}")
    time.sleep(5)
    return f"Payment processed for order {order_id}"
```
```python
# main.py - FastAPI app (Producer)
from fastapi import FastAPI
from tasks import send_booking_confirmation, process_payment

app = FastAPI()

@app.post("/book-ticket")
async def book_ticket(user_id: int, movie_id: int):
    # Save booking to database
    booking_id = 12345  # Example
    
    # Trigger background task (async, non-blocking)
    send_booking_confirmation.delay(user_id, booking_id)
    
    return {"status": "Booking confirmed", "booking_id": booking_id}

@app.post("/checkout")
async def checkout(order_id: int, amount: float):
    # Process payment in background
    process_payment.delay(order_id, amount)
    
    return {"status": "Payment processing", "order_id": order_id}

# FastAPI returns immediately, Celery workers process tasks in background
```
```bash
# Start Celery worker (Consumer)
celery -A tasks worker --loglevel=info , for process(prefork)
or celery -A tasks worker -P eventlet -c 1000, for threads
# Output:
# [2024-01-15 10:30:00] Task tasks.send_booking_confirmation received
# [2024-01-15 10:30:03] Task tasks.send_booking_confirmation succeeded
```

### What are Workers?

**Workers** are separate processes/servers that consume tasks from the queue and execute them.
```
Workers = Processes running on servers that:
1. Connect to Redis/RabbitMQ queue
2. Wait for tasks
3. Execute task logic
4. Mark task as complete
5. Repeat

You can run:
- 1 worker on 1 server
- 10 workers on 1 server
- 100 workers across 10 servers (distributed)
```

### Why Queue-Based is Better for Distributed Systems

| Feature | Thread/Process Pool | Queue-Based (Redis/Celery) |
|---------|---------------------|----------------------------|
| **Scalability** | Limited to 1 machine | Multiple servers |
| **Fault Tolerance** | Task lost if process crashes | Tasks persist in queue |
| **Horizontal Scaling** | ❌ Can't add more servers | ✅ Add more workers anytime |
| **Monitoring** | Hard to track | Easy (Redis/Celery dashboard) |
| **Task Priority** | ❌ No priority | ✅ Priority queues |
| **Retry Logic** | Manual implementation | ✅ Built-in retry |
| **Use Case** | Single server apps | Production distributed systems |

### Real-World Use Cases
```python
# Movie Ticket Booking System

# Immediate Response (Synchronous):
@app.post("/book-ticket")
def book_ticket(user_id, movie_id, seat_id):
    # 1. Lock seat (Redis distributed lock) - FAST
    # 2. Create booking in DB - FAST
    # 3. Return booking_id immediately
    
    # Background Tasks (Asynchronous via Celery):
    send_email_confirmation.delay(user_id, booking_id)
    send_sms_confirmation.delay(user_id, booking_id)
    update_analytics.delay(movie_id, seat_id)
    notify_theatre_system.delay(theatre_id, booking_id)
    
    return {"booking_id": booking_id, "status": "confirmed"}

# User gets instant response, emails sent in background by workers
```

---
## Celery: The Distributed Task Orchestrator

Celery is an open-source distributed task queue that allows applications to execute time-consuming tasks in the background. Tasks are sent to a message broker (such as Redis or RabbitMQ), and worker processes pick up and execute those tasks asynchronously.

### 1. Worker Lifecycle Management
Celery manages the creation and supervision of worker processes.
- **Auto-Scaling:** It can dynamically increase or decrease the number of child processes based on the load.
- **Process Supervision:** If a child worker process crashes, the Celery master process detects it and spawns a new one to maintain the concurrency level.
- **Resource Limits:** It manages how many tasks a worker can process before being restarted to prevent memory leaks.

### 2. Task Scheduling & Routing
Celery doesn't just push tasks; it manages their destination and timing.
- **Routing:** You can route high-priority tasks (e.g., Payments) to a specific set of workers and low-priority tasks (e.g., Newsletters) to others.
- **Celery Beat:** An inbuilt scheduler that manages periodic tasks (Cron jobs), ensuring tasks are queued at the exact right time.

### 3. Reliability & Fault Tolerance
This is the core strength of Celery over manual threading.
- **Retries:** Celery manages automatic retries with custom strategies (like Exponential Backoff) if a task fails due to temporary issues (e.g., API timeout).
- **Acknowledgment (ACK):** It ensures a task is not deleted from the broker (Redis/RabbitMQ) until the worker confirms successful execution.
- **Dead Letter Queues:** It manages tasks that consistently fail, moving them to a separate queue for manual debugging.

### 4. Serialization & Transport
- **Message Packaging:** Celery manages the conversion of Python objects/arguments into a format (JSON/Msgpack/Pickle) that can be sent over the network to the broker.
- **Broker Abstraction:** It provides a unified interface to communicate with different brokers like Redis, RabbitMQ, or Amazon SQS without changing your code.

### 5. Result Management (State Tracking)
- **State Persistence:** Celery tracks the status of a task (PENDING, STARTED, SUCCESS, FAILURE).
- **Result Backend:** It manages storing the return values of functions in a backend (Redis, Postgres, etc.) so the main application can retrieve them later if needed.

---


## Interview Questions

### Q1: What is the difference between Process and Thread?

**Answer:**
- **Process** is an independent program with its own memory space
- **Thread** is a lightweight unit inside a process that shares memory
- Processes are isolated, threads share resources
- Process creation is expensive, thread creation is cheaper
- Example: Chrome browser is a process, each tab is a thread

### Q2: Why is multiprocessing better for CPU-bound tasks?

**Answer:**
- Python has GIL (Global Interpreter Lock)
- Only one thread can execute Python bytecode at a time
- Multiprocessing bypasses GIL - each process has own Python interpreter
- True parallelism on multi-core CPUs
- Example: Image processing, ML training benefit from multiprocessing

### Q3: What is GIL and how does it affect threading?

**Answer:**
- **GIL = Global Interpreter Lock** in CPython
- Prevents multiple threads from executing Python bytecode simultaneously
- Only one thread holds GIL at a time
- **Impact:** Threading doesn't give speedup for CPU-bound tasks
- **Solution:** Use multiprocessing for CPU-bound, threading for I/O-bound

### Q4: When would you use asyncio over threading?

**Answer:**
- **Asyncio:** High concurrency I/O tasks (web servers, thousands of connections)
- **Threading:** Moderate concurrency I/O tasks (web scraping 10-100 URLs)
- **Why asyncio?**
  - Single-threaded, no race conditions
  - Very lightweight (can handle 10,000+ connections)
  - Better for modern async frameworks (FastAPI, aiohttp)


- ### The "Blocking Function" Constraint (Crucial Point)

One of the most critical factors in choosing between these two is the **nature of the function or library** you are using:

 #### 1. When to avoid Asyncio?

- If your function or third-party library is **Synchronous/Blocking** (e.g., `requests`, `time.sleep()`, or legacy DB drivers like `psycopg2`), **Asyncio will NOT work effectively.** - **The Pitfall:** Since `asyncio` runs on a single thread, a blocking call will freeze the entire Event Loop. No other task will progress until that blocking call finishes.
- **The Solution:** In such cases, you **must use Threading.** Threads are managed by the OS, so when one thread blocks on I/O, the OS can preempt it and let another thread run.

 #### 2. The Hybrid Approach (`run_in_executor`)

- If you are working in a modern async framework (like FastAPI) but need to call a blocking function, you should use a **Thread Pool** within the async loop:
```python
# Moving a blocking call to a separate thread to keep the Event Loop free
loop = asyncio.get_event_loop()
result = await loop.run_in_executor(None, blocking_function, args)
```

### Q5: Explain process memory layout

**Answer:**
```
Stack: Function calls, local variables (grows downward)
Heap: Dynamic memory allocation (grows upward)
Data: Global and static variables
Text: Program code (read-only)
```

### Q6: How do threads share memory? What are the risks?

**Answer:**
- Threads share: Code, Data (globals), Heap
- Each thread has own: Stack, Program Counter, Registers
- **Risk:** Race condition - multiple threads modify shared data simultaneously
- **Solution:** Locks, Semaphores, Mutex to synchronize access

### Q7: What is a race condition? How to prevent it?

**Answer:**
```python
# Race condition example
counter = 0

def increment():
    global counter
    counter += 1  # Not atomic! (read-modify-write)

# Thread 1 and Thread 2 execute simultaneously
# Both read counter=0, both write counter=1
# Expected: 2, Actual: 1

# Solution: Use Lock
import threading
lock = threading.Lock()

def increment_safe():
    global counter
    with lock:
        counter += 1  # Only one thread at a time
```

### Q8: What is the difference between Thread Pool and creating threads manually?

**Answer:**
- **Manual threads:** Create new thread for each task (expensive overhead)
- **Thread Pool:** Pre-created threads that are reused
- **Benefits:** Lower overhead, better resource management, automatic cleanup
- **Example:** ProcessPoolExecutor, ThreadPoolExecutor

### Q9: Why use message queues (Redis/RabbitMQ) instead of thread pools in production?

**Answer:**
- **Thread pools:** Limited to single server
- **Message queues:** Distributed across multiple servers
- **Benefits:**
  - Horizontal scaling (add more worker servers)
  - Fault tolerance (tasks persist in queue)
  - Better monitoring and retry logic
- **Use case:** Production systems with high load (millions of tasks)

### Q10: Explain producer-consumer pattern with example

**Answer:**
```python
Producer: FastAPI endpoint that adds tasks to Redis queue
Consumer: Celery workers that process tasks from queue

Example - Movie Booking:
1. User books ticket (Producer adds "send_email" task to queue)
2. Worker picks task from queue and sends email (Consumer)
3. Multiple workers can process different emails parallelly
4. If one worker crashes, other workers continue
```

### Q11: What happens during context switching?

**Answer:**
- **Context switch:** CPU switches from one process/thread to another
- **Steps:**
  1. Save current process state (PC, registers, stack pointer)
  2. Load next process state from memory
  3. Resume execution
- **Overhead:** Saving/loading state takes time
- **Why it matters:** Too many threads = too much context switching = slower performance

### Q12: Can threads from different processes communicate?

**Answer:**
- **No, directly not possible** (separate memory spaces)
- **Solution:** Use IPC (Inter-Process Communication)
  - Pipes
  - Sockets
  - Shared Memory
  - Message Queues (Redis, RabbitMQ)

### Q13: What is thread-safe code?

**Answer:**
- Code that works correctly when accessed by multiple threads simultaneously
- **Example:**
```python
# Not thread-safe
def increment():
    global counter
    counter += 1

# Thread-safe
def increment_safe():
    with lock:
        counter += 1
```

### Q14: Difference between daemon thread and normal thread?

**Answer:**
```python
# Normal thread: Main program waits for it to finish
thread = threading.Thread(target=task)
thread.start()
thread.join()  # Wait for completion

# Daemon thread: Main program doesn't wait
thread = threading.Thread(target=background_task, daemon=True)
thread.start()
# Main exits, daemon thread killed automatically

# Use case: Background monitoring, logging
```

### Q15: In a distributed movie booking system, how would you handle concurrent seat bookings?

**Answer:**
```python
# Problem: 2 users try to book same seat simultaneously

# Solution: Distributed Lock (Redis)
import redis
from redis.lock import Lock

redis_client = redis.Redis()

@app.post("/book-seat")
def book_seat(seat_id):
    lock = redis_client.lock(f"seat_lock:{seat_id}", timeout=10)
    
    if lock.acquire(blocking=True, blocking_timeout=5):
        try:
            # Check if seat available
            if is_seat_available(seat_id):
                # Book seat
                create_booking(seat_id)
                return {"status": "booked"}
            else:
                return {"status": "already booked"}
        finally:
            lock.release()
    else:
        return {"status": "couldn't acquire lock"}

# Only one user can book at a time (distributed lock across servers)
```

---

## Summary Cheatsheet
```
┌─────────────────────────────────────────────────────┐
│               QUICK DECISION GUIDE                  │
├─────────────────────────────────────────────────────┤
│ CPU-bound (computation)     → Multiprocessing       │
│ I/O-bound (few tasks)       → Threading             │
│ I/O-bound (many tasks)      → Asyncio               │
│ Single server tasks         → Thread/Process Pool   │
│ Distributed system tasks    → Redis Queue + Celery  │
└─────────────────────────────────────────────────────┘

Process: Heavy, isolated, own memory
Thread: Light, shared memory, faster communication
Asyncio: Single-threaded, event loop, highest concurrency

Production: Use Celery + Redis for background tasks
```

---

**Resources:**
- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
- [Python Multiprocessing Documentation](https://docs.python.org/3/library/multiprocessing.html)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Real Python - Threading vs Multiprocessing](https://realpython.com/python-concurrency/)

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** March 2026
