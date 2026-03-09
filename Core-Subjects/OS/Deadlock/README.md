# Deadlock - Complete Guide

## Table of Contents
1. [Introduction](#introduction)
2. [What is Deadlock?](#what-is-deadlock)
3. [Real-World Examples](#real-world-examples)
4. [Four Necessary Conditions for Deadlock](#four-necessary-conditions-for-deadlock)
5. [Deadlock in Different Contexts](#deadlock-in-different-contexts)
   - [Process-Level Deadlock](#process-level-deadlock)
   - [Thread-Level Deadlock](#thread-level-deadlock)
   - [Database-Level Deadlock](#database-level-deadlock)
   - [Distributed System Deadlock](#distributed-system-deadlock)
6. [How Operating System Handles Deadlock](#how-operating-system-handles-deadlock)
7. [Deadlock Prevention Strategies](#deadlock-prevention-strategies)
8. [Deadlock Avoidance](#deadlock-avoidance)
9. [Deadlock Detection and Recovery](#deadlock-detection-and-recovery)
10. [Code Examples - Deadlock Scenarios](#code-examples---deadlock-scenarios)
11. [Code Examples - Prevention Techniques](#code-examples---prevention-techniques)
12. [Real-World Case Study: Movie Ticket Booking](#real-world-case-study-movie-ticket-booking)
13. [Interview Questions](#interview-questions)
14. [Resources](#resources)

---

## Introduction

**Deadlock** is a situation in concurrent programming where two or more processes/threads are blocked forever, each waiting for the other to release a resource. It's like a "circular wait" where no one can proceed.

**Key Point:** Deadlock is one of the most critical problems in operating systems, databases, and distributed systems. Understanding deadlock is essential for building robust, production-ready applications.

---

## What is Deadlock?

### Definition
A **deadlock** occurs when a set of processes/threads are permanently blocked because each process is waiting for a resource held by another process in the set, creating a circular dependency.

### Simple Analogy
```
Imagine two people at a narrow bridge:
- Person A enters from left, holding left side
- Person B enters from right, holding right side
- Both need to cross, but neither can move forward
- Both are stuck waiting for the other to move back
- Result: DEADLOCK (nobody moves)
```

### Technical Definition
```
Process P1: Holds Resource R1, Needs Resource R2
Process P2: Holds Resource R2, Needs Resource R1

P1 waits for P2 to release R2
P2 waits for P1 to release R1
↓
Circular wait → DEADLOCK
```

---

## Real-World Examples

### Example 1: Banking System
```
Transaction T1:
1. Lock Account A (to debit $100)
2. Wait for Lock on Account B (to credit $100)

Transaction T2:
1. Lock Account B (to debit $50)
2. Wait for Lock on Account A (to credit $50)

Result: T1 holds A, needs B
        T2 holds B, needs A
        → DEADLOCK
```

### Example 2: Two Philosophers Problem (Classic OS Example)
```
Two philosophers at a table with one fork between them:
- Philosopher 1 picks up fork, waits for second fork
- Philosopher 2 picks up fork, waits for second fork
- Only one fork exists
- Both wait forever → DEADLOCK
```

---

## Four Necessary Conditions for Deadlock

Deadlock occurs **only if ALL four conditions are met simultaneously**. If any one condition is broken, deadlock cannot occur.

### 1. Mutual Exclusion
**Definition:** At least one resource must be held in a non-shareable mode (only one process can use it at a time).

**Example:**
```
Printer can only be used by one process at a time.
If Process P1 is printing, Process P2 must wait.

Code Example:
lock.acquire()  # Only one thread can hold this lock
# Critical section
lock.release()
```

**Why it causes deadlock:**
- If resources could be shared, multiple processes could use them simultaneously
- No waiting needed → No deadlock

---

### 2. Hold and Wait
**Definition:** A process holding at least one resource is waiting to acquire additional resources held by other processes.


**Code Example:**
```python
lock_A.acquire()
print("Thread 1: Holding Lock A...")
time.sleep(1)
# Still holding Lock A while waiting for Lock B
lock_B.acquire()  # Waiting here while holding A
```

---

### 3. No Preemption
**Definition:** Resources cannot be forcibly taken away from a process. A process must voluntarily release resources.

**Example:**
```
Process P1 holds Printer.
OS cannot forcibly take away Printer from P1.
P1 must release it voluntarily.
```

**Why it causes deadlock:**
- If OS could forcibly take resources, it could break deadlock
- But in reality, abruptly taking resources can corrupt data

---

### 4. Circular Wait
**Definition:** A set of processes waiting for each other in a circular chain.

**Example:**
```
P1 → Waiting for resource held by P2
P2 → Waiting for resource held by P3
P3 → Waiting for resource held by P1

Forms a cycle: P1 → P2 → P3 → P1
```

**Visual Representation:**
```
    ┌─────┐
    │  P1 │──────┐
    └─────┘      │
       ↑         │ Needs R2
       │         ↓
    Needs R3  ┌─────┐
       │      │  P2 │
       │      └─────┘
       │         │
    ┌─────┐      │ Needs R3
    │  P3 │←─────┘
    └─────┘

Circular dependency: P1 → P2 → P3 → P1
```

---

## Deadlock in Different Contexts

### Process-Level Deadlock

**Using multiprocessing.Lock() - OS-level locks between processes**
```python
import multiprocessing
import time

def process_1(lock_A, lock_B):
    """Process 1 - Separate memory space"""
    print("Process 1: Trying to acquire Lock A...")
    lock_A.acquire()
    print("Process 1: Acquired Lock A")
    time.sleep(2)  # Simulate work
    
    print("Process 1: Trying to acquire Lock B...")
    lock_B.acquire()  # ← DEADLOCK: Waiting for Process 2
    print("Process 1: Acquired Lock B")
    
    lock_B.release()
    lock_A.release()

def process_2(lock_A, lock_B):
    """Process 2 - Separate memory space"""
    print("Process 2: Trying to acquire Lock B...")
    lock_B.acquire()
    print("Process 2: Acquired Lock B")
    time.sleep(2)  # Simulate work
    
    print("Process 2: Trying to acquire Lock A...")
    lock_A.acquire()  # ← DEADLOCK: Waiting for Process 1
    print("Process 2: Acquired Lock A")
    
    lock_A.release()
    lock_B.release()

if __name__ == "__main__":
    # OS-level locks (shared between processes)
    lock_A = multiprocessing.Lock()
    lock_B = multiprocessing.Lock()
    
    # Create separate processes (NOT threads)
    p1 = multiprocessing.Process(target=process_1, args=(lock_A, lock_B))
    p2 = multiprocessing.Process(target=process_2, args=(lock_A, lock_B))
    
    p1.start()
    p2.start()
    
    p1.join()  # Wait for processes
    p2.join()

# Output:
# Process 1: Acquired Lock A
# Process 2: Acquired Lock B
# Process 1: Trying to acquire Lock B...  ← Stuck
# Process 2: Trying to acquire Lock A...  ← Stuck

# [Both processes hang forever] → DEADLOCK


**Why This Matters:**
- **Threads**: Share memory within same process
- **Processes**: Separate memory, communicate via OS-level mechanisms
- **Production**: Celery workers are processes, not threads!
```

**Real Example in OS:**
```
Process A: Needs 2 tape drives (currently has 1, waiting for another)
Process B: Needs 2 tape drives (currently has 1, waiting for another)
Total tape drives available: 2

Both processes stuck waiting → DEADLOCK
```

---

### Thread-Level Deadlock

**Yes, deadlock can occur with threads too!** Threads share memory but compete for locks.

**Code Example:**
```python
import threading
import time

lock_A = threading.Lock()
lock_B = threading.Lock()

def thread_1():
    print("Thread 1: Trying to acquire Lock A...")
    lock_A.acquire()
    print("Thread 1: Acquired Lock A")
    time.sleep(1)  # Simulate work
    
    print("Thread 1: Trying to acquire Lock B...")
    lock_B.acquire()  # ← DEADLOCK: Waiting for Thread 2 to release Lock B
    print("Thread 1: Acquired Lock B")
    
    lock_B.release()
    lock_A.release()

def thread_2():
    print("Thread 2: Trying to acquire Lock B...")
    lock_B.acquire()
    print("Thread 2: Acquired Lock B")
    time.sleep(1)  # Simulate work
    
    print("Thread 2: Trying to acquire Lock A...")
    lock_A.acquire()  # ← DEADLOCK: Waiting for Thread 1 to release Lock A
    print("Thread 2: Acquired Lock A")
    
    lock_A.release()
    lock_B.release()

# Run both threads
t1 = threading.Thread(target=thread_1)
t2 = threading.Thread(target=thread_2)

t1.start()
t2.start()

t1.join()
t2.join()

# Output:
# Thread 1: Acquired Lock A
# Thread 2: Acquired Lock B
# Thread 1: Trying to acquire Lock B...  ← Stuck here
# Thread 2: Trying to acquire Lock A...  ← Stuck here
# Program hangs forever → DEADLOCK
```

**Why it happens:**
- Thread 1 holds Lock A, needs Lock B
- Thread 2 holds Lock B, needs Lock A
- Circular wait → Deadlock

---

### Database-Level Deadlock

**Yes, databases can also have deadlocks!** Multiple transactions competing for row-level locks.

**Scenario:**
```sql
-- Transaction T1
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;  -- Lock Row 1
-- ... some delay ...
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;  -- Need Lock Row 2
COMMIT;

-- Transaction T2 (running simultaneously)
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 50 WHERE account_id = 2;   -- Lock Row 2
-- ... some delay ...
UPDATE accounts SET balance = balance + 50 WHERE account_id = 1;   -- Need Lock Row 1
COMMIT;

Result:
T1 holds lock on Row 1, waiting for lock on Row 2
T2 holds lock on Row 2, waiting for lock on Row 1
→ DEADLOCK
```

**How Databases Handle Deadlock:**
1. **Detection:** Database detects circular wait using wait-for graph
2. **Victim Selection:** Database chooses one transaction to abort (usually the one that did less work)
3. **Rollback:** Aborted transaction is rolled back, releasing locks
4. **Retry:** Application can retry the aborted transaction

**Example: PostgreSQL Deadlock Detection**
```
ERROR: deadlock detected
DETAIL: Process 12345 waits for ShareLock on transaction 67890;
        blocked by process 54321.
        Process 54321 waits for ShareLock on transaction 12345;
        blocked by process 12345.
HINT: See server log for query details.
```

**Database Deadlock in Django ORM:**
```python
from django.db import transaction

# Transaction T1
with transaction.atomic():
    account_1 = Account.objects.select_for_update().get(id=1)  # Lock row 1
    time.sleep(0.1)
    account_2 = Account.objects.select_for_update().get(id=2)  # Wait for row 2
    account_1.balance -= 100
    account_2.balance += 100
    account_1.save()
    account_2.save()

# Transaction T2 (running simultaneously)
with transaction.atomic():
    account_2 = Account.objects.select_for_update().get(id=2)  # Lock row 2
    time.sleep(0.1)
    account_1 = Account.objects.select_for_update().get(id=1)  # Wait for row 1
    account_2.balance -= 50
    account_1.balance += 50
    account_2.save()
    account_1.save()

# Result: Database detects deadlock, aborts one transaction
```

**Database Prevention Strategy:**
```python
# Always acquire locks in the same order
def transfer_money(from_id, to_id, amount):
    # Sort IDs to ensure consistent lock order
    id1, id2 = sorted([from_id, to_id])
    
    with transaction.atomic():
        account_1 = Account.objects.select_for_update().get(id=id1)
        account_2 = Account.objects.select_for_update().get(id=id2)
        
        if from_id == id1:
            account_1.balance -= amount
            account_2.balance += amount
        else:
            account_2.balance -= amount
            account_1.balance += amount
        
        account_1.save()
        account_2.save()

# No deadlock because locks always acquired in sorted order
```

---

### Distributed System Deadlock

**Deadlock can occur across multiple servers in a distributed system.**

**Scenario: Microservices Deadlock**
```
Service A (Server 1):
- Holds lock on User DB
- Makes API call to Service B
- Waits for response

Service B (Server 2):
- Holds lock on Order DB
- Makes API call to Service A
- Waits for response

Both services waiting for each other → DEADLOCK
```

**Example: Distributed Lock Deadlock (Redis)**

**IMPORTANT:** In production distributed systems (Celery, RQ, etc.), workers are **separate processes**, often on **different servers**.
```python
# Celery Worker Architecture
Server 1:
├── Worker Process 1 (PID: 1234)
├── Worker Process 2 (PID: 1235)
└── Worker Process 3 (PID: 1236)

Server 2:
├── Worker Process 4 (PID: 5678)
└── Worker Process 5 (PID: 5679)

# Each worker is a SEPARATE PROCESS
```

**Redis Lock in Distributed System:**
```python
# Worker on Server 1 (Process ID: 1234)
def worker_process_server_1(user_id, order_id):
    # Acquire distributed lock
    user_lock = redis_client.lock(f"user:{user_id}", timeout=10)
    user_lock.acquire()  # Lock held by Process 1234 on Server 1
    
    time.sleep(1)
    
    order_lock = redis_client.lock(f"order:{order_id}", timeout=10)
    order_lock.acquire()  # Waiting if Server 2's process holds it
    
    # Process
    user_lock.release()
    order_lock.release()

# Worker on Server 2 (Process ID: 5678)
def worker_process_server_2(order_id, user_id):
    # Same Redis instance, different server
    order_lock = redis_client.lock(f"order:{order_id}", timeout=10)
    order_lock.acquire()  # Lock held by Process 5678 on Server 2
    
    time.sleep(1)
    
    user_lock = redis_client.lock(f"user:{user_id}", timeout=10)
    user_lock.acquire()  # Waiting if Server 1's process holds it
    
    # Process
    order_lock.release()
    user_lock.release()

# If both execute simultaneously:
# Process 1234 (Server 1): Holds user lock, waits for order lock
# Process 5678 (Server 2): Holds order lock, waits for user lock

# → DEADLOCK across servers!
```


---

## How Operating System Handles Deadlock

The OS uses several strategies to handle deadlock:

### 1. Deadlock Ignorance (Ostrich Algorithm)
```
Strategy: Pretend deadlock doesn't exist
Used by: Windows, Linux (in some cases)

Why?
- Deadlock is rare
- Prevention/detection is expensive
- Easier to reboot system if deadlock occurs
- Used in systems where uptime is not critical
```

### 2. Deadlock Detection and Recovery
```
Strategy: Let deadlock occur, detect it, then recover

Detection: Periodically check for circular wait using Resource Allocation Graph

Recovery:
1. Kill one or more processes to break cycle
2. Preempt resources from processes
3. Rollback processes to previous safe state
```

**Resource Allocation Graph:**
```
Process → Resource (Request Edge)
Resource → Process (Assignment Edge)

If cycle exists → DEADLOCK detected

Example:
P1 → R1 → P2 → R2 → P1
     ↑_____________↓
        Cycle detected!
```

### 3. Deadlock Prevention
```
Strategy: Eliminate at least one of the four necessary conditions

How OS prevents:
- Break Mutual Exclusion: Make resources shareable (not always possible)
- Break Hold and Wait: Allocate all resources at once
- Break No Preemption: Allow resource preemption
- Break Circular Wait: Impose ordering on resource acquisition
```

### 4. Deadlock Avoidance (Banker's Algorithm)
```
Strategy: Dynamically examine resource allocation to ensure system never enters unsafe state

Banker's Algorithm:
- Before granting resource, check if system remains in safe state
- If unsafe, deny request (even if resource available)
- Only grant if safe sequence exists
```

---

## Deadlock Prevention Strategies

To prevent deadlock, we must break at least one of the four necessary conditions.

### Strategy 1: Break Mutual Exclusion
**Idea:** Make resources shareable (allow multiple processes to use simultaneously)

**Problem:** Not always possible (e.g., printer, file locks)

**Example:**
```python
# Read-only files can be shared
with open("data.txt", "r") as f:  # Multiple processes can read simultaneously
    data = f.read()

# Write locks must be exclusive
with open("data.txt", "w") as f:  # Only one process can write
    f.write("New data")
```

**When it works:**
- Read-only resources (files, memory)
- Spooling (print jobs queued, not directly to printer)

---

### Strategy 2: Break Hold and Wait
**Idea:** Process must request all resources at once (before execution starts)

**Implementation:**
```python
# BAD: Hold and Wait (can cause deadlock)
def bad_approach():
    lock_A.acquire()
    time.sleep(1)
    lock_B.acquire()  # Holding A while waiting for B
    # Work
    lock_B.release()
    lock_A.release()

# GOOD: Request all resources at once
def good_approach():
    acquired = False
    while not acquired:
        if lock_A.acquire(blocking=False):
            if lock_B.acquire(blocking=False):
                acquired = True
                # Work with both locks
                lock_B.release()
                lock_A.release()
            else:
                lock_A.release()  # Release A if couldn't get B
                time.sleep(0.01)  # Small delay before retry
        else:
            time.sleep(0.01)
```

**Advantages:**
- No deadlock possible
- Simple to implement

**Disadvantages:**
- Low resource utilization (resources held but not used)
- Starvation possible (process keeps waiting for all resources)
- Not always possible to know all resources needed upfront

---

### Strategy 3: Break No Preemption
**Idea:** If a process holding resources requests another resource that cannot be immediately allocated, release all held resources.

**Implementation:**
```python
def preemption_approach():
    while True:
        lock_A.acquire()
        
        # Try to get lock B with timeout
        if lock_B.acquire(timeout=5):
            # Got both locks, do work
            # Work
            lock_B.release()
            lock_A.release()
            break
        else:
            # Couldn't get lock B, release lock A (preemption)
            print("Couldn't acquire lock B, releasing lock A and retrying...")
            lock_A.release()
            time.sleep(0.1)  # Backoff before retry
```

**Advantages:**
- Prevents deadlock
- Better resource utilization than "all at once" approach

**Disadvantages:**
- Work done before preemption may be wasted
- Overhead of saving and restoring state
- Not suitable for all resources (e.g., printer - can't abort mid-print)

---

### Strategy 4: Break Circular Wait (Best and Most Common)
**Idea:** Impose a total ordering on all resource types. Processes must request resources in increasing order.

**Implementation:**
```python
# Assign unique numbers to locks
LOCK_ORDER = {
    "lock_A": 1,
    "lock_B": 2,
    "lock_C": 3,
}

# BAD: Acquiring in different orders (can deadlock)
def thread_1_bad():
    lock_A.acquire()  # Order: 1
    lock_B.acquire()  # Order: 2

def thread_2_bad():
    lock_B.acquire()  # Order: 2
    lock_A.acquire()  # Order: 1 ← Reverse order → DEADLOCK

# GOOD: Always acquire in same order
def thread_1_good():
    lock_A.acquire()  # Order: 1
    lock_B.acquire()  # Order: 2

def thread_2_good():
    lock_A.acquire()  # Order: 1 (same as thread_1)
    lock_B.acquire()  # Order: 2 (same as thread_1)
    
# No deadlock because both threads acquire locks in same order
```

**Real Example:**
```python
import threading

lock_A = threading.Lock()
lock_B = threading.Lock()

def transfer_money_ordered(from_account, to_account, amount):
    """
    Always acquire locks in sorted order of account IDs
    This prevents circular wait
    """
    # Sort account IDs to ensure consistent order
    first_account = min(from_account.id, to_account.id)
    second_account = max(from_account.id, to_account.id)
    
    # Acquire locks in order
    if from_account.id == first_account:
        lock_1, lock_2 = from_account.lock, to_account.lock
    else:
        lock_1, lock_2 = to_account.lock, from_account.lock
    
    with lock_1:
        with lock_2:
            from_account.balance -= amount
            to_account.balance += amount

# Thread 1: transfer(A, B, 100) → Locks acquired: A, B
# Thread 2: transfer(B, A, 50)  → Locks acquired: A, B (same order!)
# No circular wait → No deadlock
```

**Advantages:**
- Most practical solution
- Widely used in production systems
- Simple to implement

**Disadvantages:**
- Need to know all resources upfront
- May not be feasible for complex systems

---

## Deadlock Avoidance

### Banker's Algorithm

**Concept:** Before allocating resources, check if allocation will lead to a safe state. Only allocate if safe.

**Safe State:** A state where there exists at least one sequence of processes that can finish without deadlock.

**Example:**
```
System Resources: 12 tape drives

Processes:
P1: Max need = 10, Currently allocated = 5
P2: Max need = 4,  Currently allocated = 2
P3: Max need = 9,  Currently allocated = 2

Available resources: 12 - (5 + 2 + 2) = 3

Check if safe:
1. Can P2 finish? Yes (needs 2 more, 3 available) → Finish P2, release 4
2. Available now: 3 + 4 = 7
3. Can P1 finish? Yes (needs 5 more, 7 available) → Finish P1, release 10
4. Available now: 7 + 10 = 17
5. Can P3 finish? Yes (needs 7 more, 17 available) → Finish P3

Safe sequence exists: P2 → P1 → P3
→ System is in SAFE STATE
```

**Implementation (Simplified):**
```python
class BankersAlgorithm:
    def __init__(self, total_resources):
        self.total_resources = total_resources
        self.available = total_resources
        self.allocation = {}  # {process: allocated}
        self.max_need = {}    # {process: max_needed}
    
    def is_safe_state(self):
        """Check if current state is safe"""
        work = self.available
        finish = {p: False for p in self.allocation}
        
        while True:
            found = False
            for process in self.allocation:
                if not finish[process]:
                    need = self.max_need[process] - self.allocation[process]
                    if need <= work:
                        # Process can finish
                        work += self.allocation[process]
                        finish[process] = True
                        found = True
            
            if not found:
                break
        
        # If all processes can finish, safe state
        return all(finish.values())
    
    def request_resources(self, process, request):
        """Try to allocate resources"""
        if request > self.available:
            return False  # Not enough resources
        
        # Tentatively allocate
        self.available -= request
        self.allocation[process] += request
        
        # Check if still in safe state
        if self.is_safe_state():
            return True  # Grant request
        else:
            # Rollback allocation
            self.available += request
            self.allocation[process] -= request
            return False  # Deny request (would lead to deadlock)
```

**Disadvantages:**
- Need to know max resource needs upfront (not always possible)
- Overhead of checking safe state on every request
- Rarely used in modern OS (too complex)

---

## Deadlock Detection and Recovery

### Detection Algorithm

**Resource Allocation Graph (RAG):**
```
Nodes:
- Processes (circles)
- Resources (rectangles)

Edges:
- Request Edge: Process → Resource (process requests resource)
- Assignment Edge: Resource → Process (resource allocated to process)

If cycle exists in graph → DEADLOCK
```

**Example:**
```
P1 → R1 → P2 → R2 → P1
     ↑_______________↓
Cycle detected → DEADLOCK

P1 is waiting for R2 (held by P2)
P2 is waiting for R1 (held by P1)
```

**Detection Code (Simplified):**
```python
def detect_deadlock(allocation, request):
    """
    allocation: {process: [resources]}
    request: {process: [resources_needed]}
    """
    available = calculate_available_resources()
    finish = {p: False for p in allocation}
    
    while True:
        found = False
        for process in request:
            if not finish[process]:
                if all(request[process][i] <= available[i] for i in range(len(available))):
                    # Process can finish
                    for i in range(len(available)):
                        available[i] += allocation[process][i]
                    finish[process] = True
                    found = True
        
        if not found:
            break
    
    # Processes that couldn't finish are in deadlock
    deadlocked = [p for p, done in finish.items() if not done]
    return deadlocked
```

### Recovery Strategies

**1. Process Termination**
```
Option A: Abort all deadlocked processes (drastic, but simple)
Option B: Abort one process at a time until deadlock is resolved

Victim Selection Criteria:
- Process priority
- How long process has run
- Resources used
- Resources needed to complete
- Number of processes to terminate
```

**2. Resource Preemption**
```
1. Select a victim process
2. Rollback process to safe state
3. Preempt resources from victim
4. Allocate resources to other processes

Issues:
- How to rollback? (need checkpoints)
- Starvation: same process always chosen as victim
```

---

## Code Examples - Deadlock Scenarios

### Example 1: Classic Thread Deadlock
```python
import threading
import time

lock_1 = threading.Lock()
lock_2 = threading.Lock()

def thread_A():
    print("Thread A: Acquiring lock_1...")
    with lock_1:
        print("Thread A: Acquired lock_1")
        time.sleep(1)  # Simulate work
        
        print("Thread A: Acquiring lock_2...")
        with lock_2:  # ← DEADLOCK: Waiting for Thread B to release lock_2
            print("Thread A: Acquired lock_2")
            print("Thread A: Done!")

def thread_B():
    print("Thread B: Acquiring lock_2...")
    with lock_2:
        print("Thread B: Acquired lock_2")
        time.sleep(1)  # Simulate work
        
        print("Thread B: Acquiring lock_1...")
        with lock_1:  # ← DEADLOCK: Waiting for Thread A to release lock_1
            print("Thread B: Acquired lock_1")
            print("Thread B: Done!")

# Run threads
t1 = threading.Thread(target=thread_A)
t2 = threading.Thread(target=thread_B)

t1.start()
t2.start()

t1.join()
t2.join()

# Output:
# Thread A: Acquired lock_1
# Thread B: Acquired lock_2
# Thread A: Acquiring lock_2...  ← Stuck
# Thread B: Acquiring lock_1...  ← Stuck
# [Program hangs forever]
```

---

### Example 2: Database Transaction Deadlock
```python
from django.db import transaction
import time

# Transaction 1
def transfer_A_to_B():
    with transaction.atomic():
        # Lock account A
        account_A = Account.objects.select_for_update().get(id=1)
        time.sleep(0.1)  # Simulate processing
        
        # Try to lock account B (might be locked by Transaction 2)
        account_B = Account.objects.select_for_update().get(id=2)
        
        account_A.balance -= 100
        account_B.balance += 100
        account_A.save()
        account_B.save()

# Transaction 2
def transfer_B_to_A():
    with transaction.atomic():
        # Lock account B
        account_B = Account.objects.select_for_update().get(id=2)
        time.sleep(0.1)  # Simulate processing
        
        # Try to lock account A (might be locked by Transaction 1)
        account_A = Account.objects.select_for_update().get(id=1)
        
        account_B.balance -= 50
        account_A.balance += 50
        account_B.save()
        account_A.save()

# Run both transactions simultaneously
thread1 = threading.Thread(target=transfer_A_to_B)
thread2 = threading.Thread(target=transfer_B_to_A)

thread1.start()
thread2.start()

# Result: Database detects deadlock, aborts one transaction
# ERROR: deadlock detected
```

---

### Example 3: Distributed Lock Deadlock (Redis)
```python
import redis
import time
from redis.lock import Lock

redis_client = redis.Redis(host='localhost', port=6379)

def process_order_service_1(user_id, order_id):
    """Service 1: Process order"""
    user_lock = redis_client.lock(f"user:{user_id}", timeout=10)
    
    print("Service 1: Acquiring user lock...")
    user_lock.acquire()
    print("Service 1: Acquired user lock")
    time.sleep(1)
    
    print("Service 1: Acquiring order lock...")
    order_lock = redis_client.lock(f"order:{order_id}", timeout=10)
    order_lock.acquire()  # ← DEADLOCK: Waiting for Service 2
    print("Service 1: Acquired order lock")
    
    # Process
    print("Service 1: Processing...")
    
    order_lock.release()
    user_lock.release()

def process_payment_service_2(order_id, user_id):
    """Service 2: Process payment"""
    order_lock = redis_client.lock(f"order:{order_id}", timeout=10)
    
    print("Service 2: Acquiring order lock...")
    order_lock.acquire()
    print("Service 2: Acquired order lock")
    time.sleep(1)
    
    print("Service 2: Acquiring user lock...")
    user_lock = redis_client.lock(f"user:{user_id}", timeout=10)
    user_lock.acquire()  # ← DEADLOCK: Waiting for Service 1
    print("Service 2: Acquired user lock")
    
    # Process
    print("Service 2: Processing...")
    
    user_lock.release()
    order_lock.release()

# Run both services simultaneously
thread1 = threading.Thread(target=process_order_service_1, args=(123, 456))
thread2 = threading.Thread(target=process_payment_service_2, args=(456, 123))

thread1.start()
thread2.start()

# Result: Both services stuck waiting for each other → DEADLOCK
```

---

## Code Examples - Prevention Techniques

### Technique 1: Lock Ordering (Break Circular Wait)
```python
import threading
import time

lock_1 = threading.Lock()
lock_2 = threading.Lock()

def acquire_locks_ordered(*locks):
    """
    Acquire multiple locks in a consistent order to prevent circular wait
    """
    # Sort locks by id to ensure consistent order
    sorted_locks = sorted(locks, key=id)
    
    for lock in sorted_locks:
        lock.acquire()
    
    return sorted_locks

def release_locks_ordered(locks):
    """Release locks in reverse order"""
    for lock in reversed(locks):
        lock.release()

def thread_A_safe():
    print("Thread A: Acquiring locks in order...")
    locks = acquire_locks_ordered(lock_1, lock_2)
    
    try:
        print("Thread A: Acquired all locks")
        time.sleep(1)
        print("Thread A: Done!")
    finally:
        release_locks_ordered(locks)

def thread_B_safe():
    print("Thread B: Acquiring locks in order...")
    locks = acquire_locks_ordered(lock_2, lock_1)  # Different order, but sorted internally
    
    try:
        print("Thread B: Acquired all locks")
        time.sleep(1)
        print("Thread B: Done!")
    finally:
        release_locks_ordered(locks)

# Run threads
t1 = threading.Thread(target=thread_A_safe)
t2 = threading.Thread(target=thread_B_safe)

t1.start()
t2.start()

t1.join()
t2.join()

# Output:
# Thread A: Acquired all locks
# Thread A: Done!
# Thread B: Acquired all locks
# Thread B: Done!
# No deadlock! Both threads acquire locks in same sorted order
```

---

### Technique 2: Timeout (Detect and Retry)
```python
import threading
import time

lock_1 = threading.Lock()
lock_2 = threading.Lock()

def try_acquire_with_timeout(lock, timeout=5):
    """Try to acquire lock with timeout"""
    start = time.time()
    while time.time() - start < timeout:
        if lock.acquire(blocking=False):
            return True
        time.sleep(0.01)
    return False

def thread_with_timeout():
    max_retries = 3
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}: Acquiring lock_1...")
        if try_acquire_with_timeout(lock_1):
            print("Acquired lock_1")
            
            print("Acquiring lock_2...")
            if try_acquire_with_timeout(lock_2):
                print("Acquired lock_2")
                try:
                    # Do work
                    print("Doing work...")
                    time.sleep(1)
                    return  # Success
                finally:
                    lock_2.release()
                    lock_1.release()
            else:
                # Couldn't get lock_2, release lock_1 and retry
                print("Timeout acquiring lock_2, releasing lock_1 and retrying...")
                lock_1.release()
                time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
        else:
            print("Timeout acquiring lock_1, retrying...")
            time.sleep(0.1 * (2 ** attempt))
    
    print("Failed to acquire locks after retries")

# Run threads
t1 = threading.Thread(target=thread_with_timeout)
t2 = threading.Thread(target=thread_with_timeout)

t1.start()
t2.start()

t1.join()
t2.join()

# Even if deadlock occurs temporarily, timeout breaks it and retries
```

---

### Technique 3: Try-Lock (Non-blocking Acquire)
```python
import threading
import time

lock_1 = threading.Lock()
lock_2 = threading.Lock()

def try_lock_approach():
    """
    Try to acquire all locks without blocking
    If can't get all, release and retry
    """
    while True:
        # Try to acquire lock_1 without blocking
        if lock_1.acquire(blocking=False):
            print("Acquired lock_1")
            
            # Try to acquire lock_2 without blocking
            if lock_2.acquire(blocking=False):
                print("Acquired lock_2")
                try:
                    # Do work
                    print("Doing work...")
                    time.sleep(1)
                    return  # Success
                finally:
                    lock_2.release()
                    lock_1.release()
            else:
                # Couldn't get lock_2, release lock_1
                print("Couldn't acquire lock_2, releasing lock_1")
                lock_1.release()
        
        # Small delay before retry
        time.sleep(0.01)

# Run threads
t1 = threading.Thread(target=try_lock_approach)
t2 = threading.Thread(target=try_lock_approach)

t1.start()
t2.start()

t1.join()
t2.join()

# No deadlock because threads don't block waiting for locks
```

---

### Technique 4: Context Manager for Multiple Locks
```python
import threading
from contextlib import contextmanager

lock_1 = threading.Lock()
lock_2 = threading.Lock()
lock_3 = threading.Lock()

@contextmanager
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
    with acquire_multiple_locks(lock_1, lock_2, lock_3):
        print("Thread: Acquired all locks safely")
        time.sleep(1)
        print("Thread: Done!")

# Run threads
threads = [threading.Thread(target=safe_thread) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# No deadlock! All threads acquire locks in same order
```

---

## Real-World Case Study: Movie Ticket Booking

### Problem: Concurrent Seat Booking Deadlock

**Scenario:**
```
User 1: Wants to book seats A1 and A2
User 2: Wants to book seats A2 and A1 (same seats, different order)

Both users click "Book" simultaneously

Thread 1 (User 1):
- Lock seat A1 ✅
- Wait for lock on A2... (held by Thread 2)

Thread 2 (User 2):
- Lock seat A2 ✅
- Wait for lock on A1... (held by Thread 1)

Result: DEADLOCK
```

### Solution 1: Lock Ordering
```python
import threading
import time
from django.db import transaction

class SeatBookingService:
    locks = {}  # {seat_id: Lock}
    
    @classmethod
    def get_lock(cls, seat_id):
        """Get or create lock for seat"""
        if seat_id not in cls.locks:
            cls.locks[seat_id] = threading.Lock()
        return cls.locks[seat_id]
    
    @staticmethod
    def book_seats_safe(user_id, seat_ids):
        """
        Book multiple seats safely (no deadlock)
        Always acquire locks in sorted order
        """
        # Sort seat IDs to ensure consistent lock order
        sorted_seat_ids = sorted(seat_ids)
        
        # Acquire locks in order
        locks = [SeatBookingService.get_lock(sid) for sid in sorted_seat_ids]
        
        for lock in locks:
            lock.acquire()
        
        try:
            with transaction.atomic():
                # Check all seats are available
                seats = Seat.objects.select_for_update().filter(
                    id__in=sorted_seat_ids,
                    is_booked=False
                )
                
                if len(seats) != len(sorted_seat_ids):
                    return {"success": False, "error": "Some seats already booked"}
                
                # Book all seats
                for seat in seats:
                    seat.is_booked = True
                    seat.booked_by = user_id
                    seat.save()
                
                # Create booking
                booking = Booking.objects.create(
                    user_id=user_id,
                    seats=list(seats),
                    total_amount=len(seats) * 100
                )
                
                return {"success": True, "booking_id": booking.id}
        finally:
            # Release locks in reverse order
            for lock in reversed(locks):
                lock.release()

# Usage
# User 1: book_seats_safe(user_id=1, seat_ids=[101, 102])  → Locks: 101, 102
# User 2: book_seats_safe(user_id=2, seat_ids=[102, 101])  → Locks: 101, 102 (same order!)
# No deadlock because both acquire locks in sorted order
```

---

### Solution 2: Distributed Lock with Redis (Production-Ready)
```python
import redis
from redis.lock import Lock
from django.db import transaction
import time

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

class DistributedSeatBooking:
    @staticmethod
    def book_seats_distributed(user_id, seat_ids, timeout=10):
        """
        Book seats using distributed Redis locks
        Works across multiple servers
        """
        # Sort seat IDs for consistent order
        sorted_seat_ids = sorted(seat_ids)
        
        # Acquire distributed locks
        locks = []
        acquired_locks = []
        
        try:
            # Try to acquire all locks
            for seat_id in sorted_seat_ids:
                lock = redis_client.lock(
                    f"seat_lock:{seat_id}",
                    timeout=timeout,
                    blocking_timeout=5
                )
                if lock.acquire(blocking=True):
                    locks.append(lock)
                    acquired_locks.append(seat_id)
                else:
                    # Couldn't acquire lock, release all and fail
                    raise Exception(f"Couldn't acquire lock for seat {seat_id}")
            
            # All locks acquired, proceed with booking
            with transaction.atomic():
                seats = Seat.objects.select_for_update().filter(
                    id__in=sorted_seat_ids,
                    is_booked=False
                )
                
                if len(seats) != len(sorted_seat_ids):
                    return {"success": False, "error": "Some seats already booked"}
                
                # Book seats
                for seat in seats:
                    seat.is_booked = True
                    seat.booked_by = user_id
                    seat.save()
                
                booking = Booking.objects.create(
                    user_id=user_id,
                    seats=list(seats),
                    total_amount=len(seats) * 100
                )
                
                return {"success": True, "booking_id": booking.id}
        
        finally:
            # Release all acquired locks
            for lock in locks:
                try:
                    lock.release()
                except:
                    pass  # Lock might have expired

# Usage
# Server 1: book_seats_distributed(user_id=1, seat_ids=[101, 102])
# Server 2: book_seats_distributed(user_id=2, seat_ids=[102, 101])
# No deadlock because locks acquired in sorted order across all servers
```

---

### Solution 3: Optimistic Locking (No Locks, Use Versioning)
```python
from django.db import transaction
from django.db.models import F

class Seat(models.Model):
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)
    version = models.IntegerField(default=0)  # For optimistic locking
    
class OptimisticSeatBooking:
    @staticmethod
    def book_seats_optimistic(user_id, seat_ids, max_retries=3):
        """
        Optimistic locking: No locks, use version numbers
        Retry if conflict detected
        """
        for attempt in range(max_retries):
            try:
                with transaction.atomic():
                    # Read seats with current version
                    seats = Seat.objects.filter(
                        id__in=seat_ids,
                        is_booked=False
                    )
                    
                    if len(seats) != len(seat_ids):
                        return {"success": False, "error": "Some seats unavailable"}
                    
                    # Record current versions
                    seat_versions = {seat.id: seat.version for seat in seats}
                    
                    # Try to update with version check
                    for seat in seats:
                        updated = Seat.objects.filter(
                            id=seat.id,
                            version=seat_versions[seat.id],  # Check version hasn't changed
                            is_booked=False
                        ).update(
                            is_booked=True,
                            booked_by=user_id,
                            version=F('version') + 1  # Increment version
                        )
                        
                        if updated == 0:
                            # Version mismatch or seat booked by someone else
                            raise Exception("Conflict detected, retrying...")
                    
                    # Success
                    booking = Booking.objects.create(
                        user_id=user_id,
                        seat_ids=seat_ids,
                        total_amount=len(seat_ids) * 100
                    )
                    
                    return {"success": True, "booking_id": booking.id}
            
            except Exception as e:
                if attempt == max_retries - 1:
                    return {"success": False, "error": "Too many conflicts, try again"}
                time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
        
        return {"success": False, "error": "Booking failed"}

# No locks used! If two users try to book same seat:
# 1. Both read seat with version=1
# 2. User 1 updates: version=2, booked=True
# 3. User 2 tries to update with version=1 → Fails (version mismatch)
# 4. User 2 retries, sees seat already booked
```

---

### Comparison: Which Solution to Use?

| Approach | Pros | Cons | Use Case |
|----------|------|------|----------|
| **Lock Ordering** | Simple, no deadlock | Only works in single server | Small apps, single server |
| **Distributed Locks (Redis)** | Works across servers, no deadlock | Requires Redis, complex | Production, multi-server |
| **Optimistic Locking** | No locks, high performance | Retries on conflict, can fail | High-traffic, read-heavy |

**Recommendation for Production:**
```python
# Use Distributed Locks (Redis) for movie booking
# Why?
# - Multiple servers (load balanced)
# - Strong consistency needed (no double booking)
# - Moderate traffic (not millions per second)

# Use Optimistic Locking for high-traffic scenarios
# - Product inventory (e-commerce)
# - Like counts (social media)
# - View counts (analytics)
```

---

## Interview Questions

### Q1: Difference between deadlock prevention and deadlock avoidance?

**Answer:**

| Feature | Prevention | Avoidance |
|---------|-----------|-----------|
| **Approach** | Break one of 4 conditions | Dynamically check safe state |
| **When** | Design time (static) | Runtime (dynamic) |
| **Example** | Lock ordering | Banker's algorithm |
| **Overhead** | Low | High (check on every request) |
| **Practical** | Yes (widely used) | Rarely (too complex) |


---

### Q2: Can you have deadlock in a single-threaded application?

**Answer:**
**No, deadlock cannot occur in single-threaded applications.**

**Why?**
- Deadlock requires at least 2 processes/threads
- Single thread executes sequentially
- No concurrent resource competition
- No circular wait possible

**However:** Single-threaded async applications (event loop) can have **livelock** (different from deadlock).

---

### Q3: What is the difference between deadlock and livelock?

**Answer:**

| Feature | Deadlock | Livelock |
|---------|----------|----------|
| **State** | Processes blocked, not doing anything | Processes active, but not progressing |
| **Example** | Two threads waiting for each other's locks | Two people in hallway, both stepping aside in same direction repeatedly |
| **Detection** | Easy (check circular wait) | Hard (processes appear active) |
| **Solution** | Break one of 4 conditions | Add randomness, backoff |

---

### Q4: In a distributed system with multiple servers, how would you prevent deadlock when accessing shared resources?

**Answer:**
**Use Distributed Locking with Consistent Ordering**
```python
# Use Redis distributed locks
# Always acquire in sorted order of resource IDs

def acquire_resources(resource_ids):
    sorted_ids = sorted(resource_ids)
    locks = []
    
    for rid in sorted_ids:
        lock = redis_client.lock(f"resource:{rid}", timeout=10)
        if lock.acquire(blocking_timeout=5):
            locks.append(lock)
        else:
            # Couldn't acquire, release all and retry
            for l in locks:
                l.release()
            raise Exception("Retry")
    
    return locks

# Works across multiple servers
# No circular wait because locks acquired in sorted order
```

---

### Q5: How does Python's `threading.RLock()` help prevent deadlock?

**Answer:**
**RLock (Reentrant Lock)** allows same thread to acquire lock multiple times.

**Use case:**
```python
lock = threading.RLock()

def outer():
    with lock:
        inner()  # Can acquire lock again (same thread)

def inner():
    with lock:  # Doesn't block (reentrant)
        print("Inner function")

# Regular Lock would deadlock here (same thread waiting for itself)
# RLock allows it (tracks acquisition count)
```

**Note:** RLock doesn't prevent deadlock between different threads, only helps with recursive function calls in same thread.

---

### Q6: What is a timeout-based deadlock recovery approach?

**Answer:**
**Set timeout when acquiring locks. If timeout expires, release held locks and retry.**
```python
def acquire_with_timeout():
    if lock_A.acquire(timeout=5):
        if lock_B.acquire(timeout=5):
            # Got both locks
            # Do work
            lock_B.release()
            lock_A.release()
        else:
            # Timeout on lock_B, release lock_A
            lock_A.release()
            # Retry with backoff
```

**Pros:**
- Prevents indefinite blocking
- Simple to implement

**Cons:**
- May not actually be deadlock (just slow)
- Wasted work if already did computation before timeout

---

### Q7: In Django, how would you prevent deadlock when updating multiple related database rows?

**Answer:**
**Use `select_for_update()` with consistent ordering**
```python
from django.db import transaction

def transfer_money_safe(from_id, to_id, amount):
    # Sort IDs to ensure consistent lock order
    id1, id2 = sorted([from_id, to_id])
    
    with transaction.atomic():
        # Acquire locks in sorted order
        account1 = Account.objects.select_for_update().get(id=id1)
        account2 = Account.objects.select_for_update().get(id=id2)
        
        # Determine which is from/to after sorting
        if from_id == id1:
            from_account, to_account = account1, account2
        else:
            from_account, to_account = account2, account1
        
        # Update balances
        from_account.balance -= amount
        to_account.balance += amount
        
        from_account.save()
        to_account.save()

# No deadlock because locks always acquired in sorted order
```

---

## Resources

### Official Documentation
- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
- [Python Multiprocessing Documentation](https://docs.python.org/3/library/multiprocessing.html)
- [PostgreSQL Deadlock Documentation](https://www.postgresql.org/docs/current/explicit-locking.html)
- [Redis Distributed Locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/)

### Books
- **Operating System Concepts** by Silberschatz, Galvin, Geltzer (Chapter on Deadlocks)
- **Database System Concepts** by Silberschatz (Transaction Management)
- **Concurrency in Python** by Real Python

### Online Resources
- [Deadlock in Operating Systems - GeeksforGeeks](https://www.geeksforgeeks.org/introduction-of-deadlock-in-operating-system/)
- [Understanding Deadlocks - Microsoft Docs](https://docs.microsoft.com/en-us/troubleshoot/windows-server/performance/understand-deadlock)
- [Distributed Locks with Redis - Martin Kleppmann](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)


### Advanced Topics
- [The Dining Philosophers Problem](https://en.wikipedia.org/wiki/Dining_philosophers_problem)
- [Redlock Algorithm for Distributed Locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/)


---

**Summary Cheatsheet**
```
┌─────────────────────────────────────────────────────┐
│             DEADLOCK QUICK REFERENCE                │
├─────────────────────────────────────────────────────┤
│ 4 Necessary Conditions (ALL must be true):          │
│ 1. Mutual Exclusion                                 │
│ 2. Hold and Wait                                    │
│ 3. No Preemption                                    │
│ 4. Circular Wait                                    │
├─────────────────────────────────────────────────────┤
│ Prevention (Break one condition):                   │
│ ✅ Lock Ordering → Break Circular Wait (BEST)      │
│ ⚠️ Acquire All at Once → Break Hold and Wait       │
│ ⚠️ Timeout & Retry → Break No Preemption           │
├─────────────────────────────────────────────────────┤
│ Detection & Recovery:                               │
│ - Resource Allocation Graph (check for cycles)      │
│ - Kill victim process                               │
│ - Rollback and retry                                │
├─────────────────────────────────────────────────────┤
│ Production Best Practices:                          │
│ - Always acquire locks in sorted order              │
│ - Use distributed locks (Redis) for multi-server    │
│ - Set timeouts to prevent infinite blocking         │
│ - Monitor and log lock acquisitions                 │
└─────────────────────────────────────────────────────┘
```


---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** March 2026