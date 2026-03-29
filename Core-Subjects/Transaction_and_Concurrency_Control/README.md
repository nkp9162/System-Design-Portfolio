# Transactions and Concurrency Control - Complete Guide

## Table of Contents
1. [Introduction](#introduction)
2. [What is a Transaction?](#what-is-a-transaction)
3. [Concurrency Control](#concurrency-control)
4. [Locking Mechanisms](#locking-mechanisms)
   - [Pessimistic Locking](#pessimistic-locking)
   - [Optimistic Locking](#optimistic-locking)
   - [Version-Based Locking](#version-based-locking)
5. [MVCC (Multi-Version Concurrency Control)](#mvcc-multi-version-concurrency-control)
6. [Distributed Transactions](#distributed-transactions)
7. [SAGA Pattern](#saga-pattern)
8. [Two-Phase Commit (2PC)](#two-phase-commit-2pc)
9. [Isolation Levels Recap](#isolation-levels-recap)
10. [Interview Questions](#interview-questions)
11. [Resources](#resources)

---

## Introduction

**Concurrency Control** ensures multiple transactions can execute simultaneously without causing data inconsistencies. This is critical in multi-user systems where many operations happen at the same time.

**Key Challenge:** How to allow concurrent access while maintaining ACID properties?

---

## What is a Transaction?

**Transaction:** A unit of work that either completes fully or has no effect at all (atomicity).

**Properties:** Already covered in ACID (Atomicity, Consistency, Isolation, Durability)

**Transaction States:**
```
BEGIN TRANSACTION
    ↓
Active (executing)
    ↓
    ├─→ Committed (success) → Durable
    └─→ Aborted (failure) → Rolled back
```

**Quick Recap:**
```sql
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- Both updates succeed

-- Or:
ROLLBACK;  -- Both updates reverted
```

---

## Concurrency Control

**Goal:** Allow multiple transactions to run concurrently without interfering with each other.

**Problems Without Concurrency Control:**

**1. Lost Update:**
```
T1: Read balance = 1000
T2: Read balance = 1000
T1: Write balance = 900  (1000 - 100)
T2: Write balance = 800  (1000 - 200)

Result: Balance = 800 (T1's update lost!)
Expected: Balance = 700 (1000 - 100 - 200)
```

**2. Dirty Read:** (Already covered in ACID - Isolation Levels)

**3. Non-Repeatable Read:** (Already covered in ACID - Isolation Levels)

**Solutions:** Locking mechanisms, MVCC

---

## Locking Mechanisms

### Pessimistic Locking

**Concept:** **Lock data before modifying** it. Assume conflicts will happen, so prevent them.

**How it Works:**
```
1. Transaction acquires lock on row
2. Other transactions wait (blocked)
3. Transaction modifies data
4. Transaction releases lock
5. Waiting transactions can now proceed
```

**Types of Locks:**

**Shared Lock (S-Lock):** Multiple transactions can read, but none can write
```sql
-- PostgreSQL
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR SHARE;  -- Shared lock
-- Others can read, but cannot write until this transaction commits
COMMIT;
```

**Exclusive Lock (X-Lock):** Only one transaction can read/write
```sql
-- PostgreSQL
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- Exclusive lock
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- No other transaction can read or write this row
COMMIT;
```

**Django Example:**
```python
from django.db import transaction

def transfer_money_pessimistic(from_id, to_id, amount):
    with transaction.atomic():
        # Pessimistic locking: Lock rows before reading
        from_account = Account.objects.select_for_update().get(id=from_id)
        to_account = Account.objects.select_for_update().get(id=to_id)
        
        # Rows are locked, safe to modify
        from_account.balance -= amount
        to_account.balance += amount
        
        from_account.save()
        to_account.save()
        
        # Locks released on commit

# If two transactions try to modify same account:
# T1: Acquires lock on account 1
# T2: Waits for lock on account 1
# T1: Commits, releases lock
# T2: Acquires lock, proceeds
```

**Pros:**
- ✅ Prevents conflicts (no lost updates)
- ✅ Simple to understand
- ✅ Works well for high-contention scenarios

**Cons:**
- ❌ Blocking (transactions wait)
- ❌ Potential deadlocks
- ❌ Reduced concurrency

**When to Use:**
- High conflict probability (many users editing same data)
- Critical data (financial transactions)
- Short transactions

---

### Optimistic Locking

**Concept:** **Don't lock**, assume conflicts are rare. Check for conflicts before committing.

**How it Works:**
```
1. Transaction reads data (no lock)
2. Transaction modifies data locally
3. Before commit, check if data was modified by another transaction
4. If modified → Abort and retry
5. If not modified → Commit
```

**Implementation: Version Number**
```sql
-- Add version column
CREATE TABLE accounts (
    id INT PRIMARY KEY,
    balance DECIMAL(10,2),
    version INT DEFAULT 0  -- Version number
);

-- Transaction T1:
BEGIN;
SELECT id, balance, version FROM accounts WHERE id = 1;
-- Returns: id=1, balance=1000, version=5

UPDATE accounts 
SET balance = 900, version = version + 1
WHERE id = 1 AND version = 5;  -- Check version hasn't changed

-- If UPDATE affects 0 rows → Someone else modified → Retry
COMMIT;
```

**Django Example:**
```python
from django.db import transaction
from django.db.models import F

class Account(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    version = models.IntegerField(default=0)

def transfer_money_optimistic(from_id, to_id, amount, max_retries=3):
    for attempt in range(max_retries):
        try:
            with transaction.atomic():
                # Read current version
                from_account = Account.objects.get(id=from_id)
                old_version = from_account.version
                              
                # Update with version check
                updated = Account.objects.filter(
                    id=from_id,
                    version=old_version  # Check version hasn't changed
                    balance__gte=amount  # db level validation
                ).update(
                    balance=F('balance') - amount,
                    version=F('version') + 1
                )
                
                if updated == 0:
                    # Version mismatch, someone else modified
                    raise Exception("Conflict detected, retrying...")
                
                # Update to_account similarly
                to_account = Account.objects.get(id=to_id)
                to_account.balance += amount
                to_account.version += 1
                to_account.save()
                
                return {"success": True}
        
        except Exception as e:
            if attempt == max_retries - 1:
                return {"success": False, "error": "Max retries exceeded"}
            time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
    
    return {"success": False}

# Concurrent scenario:
# T1: Read version=5
# T2: Read version=5
# T1: Update (version 5→6) ✅ Success
# T2: Update (version=5) ❌ Fails (version already 6), retries
```

**Pros:**
- ✅ No blocking (high concurrency)
- ✅ No deadlocks
- ✅ Better performance for low-contention

**Cons:**
- ❌ Retries needed on conflict
- ❌ Wasted work if conflict frequent
- ❌ Complexity in application logic

**When to Use:**
- Low conflict probability (many users, different data)
- Read-heavy workloads
- Long-running transactions (avoid holding locks)

---

### Version-Based Locking

**Concept:** Track changes using version numbers or timestamps. Detect conflicts without locks.

**Techniques:**

#### 1. Version Number (Optimistic Locking)

Already covered above. Increment version on each update.
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    stock = models.IntegerField()
    version = models.IntegerField(default=0)

def update_stock_safe(product_id, quantity):
    product = Product.objects.get(id=product_id)
    old_version = product.version
    
    # Update with version check
    updated = Product.objects.filter(
        id=product_id,
        version=old_version
    ).update(
        stock=F('stock') - quantity,
        version=F('version') + 1
    )
    
    if updated == 0:
        raise Exception("Product was modified by another transaction")
```

#### 2. Timestamp-Based

Use timestamp instead of version number.
```python
class Order(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_modified = models.DateTimeField(auto_now=True)

def update_order(order_id, new_amount, expected_timestamp):
    updated = Order.objects.filter(
        id=order_id,
        last_modified=expected_timestamp  # Check timestamp
    ).update(
        total_amount=new_amount,
        last_modified=timezone.now()
    )
    
    if updated == 0:
        raise Exception("Order was modified by another transaction")
```

**Pros:**
- ✅ Simple to implement
- ✅ No database locks needed
- ✅ Works across distributed systems

**Cons:**
- ❌ Requires additional column (version/timestamp)
- ❌ Application must handle retries
- ❌ Not suitable for all scenarios

---

## MVCC (Multi-Version Concurrency Control)

**Concept:** Database keeps **multiple versions** of each row. Readers see consistent snapshot, writers create new versions.

**How it Works:**
```
Database stores multiple versions of same row:

Account (id=1):
Version 1: balance=1000, transaction_id=100 (committed)
Version 2: balance=900,  transaction_id=101 (committed)
Version 3: balance=800,  transaction_id=102 (active)

Transaction T1 (started at transaction_id=101):
- Reads Account 1
- Sees Version 2 (balance=900)
- Even though Version 3 exists, T1 sees snapshot at its start time

Transaction T2 (started at transaction_id=102):
- Reads Account 1
- Sees Version 3 (balance=800)
```

**PostgreSQL MVCC Example:**
```sql
-- PostgreSQL uses MVCC by default

-- Transaction T1
BEGIN;  -- Snapshot created here
SELECT balance FROM accounts WHERE id = 1;  -- Returns 1000

-- Transaction T2 (concurrent)
BEGIN;
UPDATE accounts SET balance = 900 WHERE id = 1;
COMMIT;  -- New version created

-- Transaction T1 (still running)
SELECT balance FROM accounts WHERE id = 1;  -- Still returns 1000!
-- T1 sees its snapshot, not T2's changes

COMMIT;

-- Now all new transactions see balance = 900
```

**Django with PostgreSQL MVCC:**
```python
from django.db import transaction

# Transaction 1
with transaction.atomic():
    account = Account.objects.get(id=1)
    print(account.balance)  # 1000
    
    # Transaction 2 (in another request/thread) commits change to 900
    
    # Still in Transaction 1
    account = Account.objects.get(id=1)
    print(account.balance)  # Still 1000 (snapshot isolation)

# After commit, see new value
account = Account.objects.get(id=1)
print(account.balance)  # 900
```

**Benefits:**
- ✅ Readers don't block writers
- ✅ Writers don't block readers
- ✅ High concurrency
- ✅ Consistent snapshots (Repeatable Read isolation)

**Costs:**
- ❌ Extra storage (multiple versions)
- ❌ Vacuum/garbage collection needed (clean old versions)
- ❌ Complexity in implementation

**Used By:** PostgreSQL, MySQL InnoDB, Oracle

---

## Distributed Transactions

**Challenge:** Maintain ACID properties across **multiple databases/services** on different servers.

**Problem:**
```
Service A (Database A): Deduct $100 from account
Service B (Database B): Add $100 to account

What if Service A succeeds but Service B fails?
→ Distributed transaction must ensure both succeed or both fail
```

**Solutions:**
1. Two-Phase Commit (2PC)
2. SAGA Pattern

---

## Two-Phase Commit (2PC)

**Concept:** Coordinator ensures all participants agree before committing.

**Phases:**

**Phase 1 - Prepare (Voting):**
```
Coordinator: "Can you commit this transaction?"
Participant A: "Yes, ready to commit"
Participant B: "Yes, ready to commit"
Participant C: "No, cannot commit" (failure)
```

**Phase 2 - Commit/Abort:**
```
If ALL participants vote YES:
    Coordinator: "Commit!"
    All participants: Commit transaction
Else:
    Coordinator: "Abort!"
    All participants: Rollback transaction
```

**Flow Diagram:**
```
Coordinator                Participant A          Participant B
    |                           |                      |
    |----PREPARE--------------->|                      |
    |----PREPARE-------------------------------->|
    |                           |                      |
    |<---VOTE YES---------------|                      |
    |<---VOTE YES-----------------------------|
    |                           |                      |
    |----COMMIT---------------->|                      |
    |----COMMIT----------------------------------->|
    |                           |                      |
    |<---ACK--------------------|                      |
    |<---ACK---------------------------------------|
    |                           |                      |
   Done                       Done                   Done
```

**Example: Distributed Money Transfer**
```python
# Pseudo-code (simplified)
class TwoPhaseCommitCoordinator:
    def transfer_distributed(self, from_db, to_db, amount):
        transaction_id = generate_id()
        
        # Phase 1: Prepare
        prepare_results = []
        
        # Ask Participant A (from_db) to prepare
        result_a = from_db.prepare(transaction_id, "UPDATE accounts SET balance = balance - %s", amount)
        prepare_results.append(result_a)
        
        # Ask Participant B (to_db) to prepare
        result_b = to_db.prepare(transaction_id, "UPDATE accounts SET balance = balance + %s", amount)
        prepare_results.append(result_b)
        
        # Phase 2: Commit or Abort
        if all(result == "YES" for result in prepare_results):
            # All voted YES, commit
            from_db.commit(transaction_id)
            to_db.commit(transaction_id)
            return {"status": "committed"}
        else:
            # At least one voted NO, abort
            from_db.abort(transaction_id)
            to_db.abort(transaction_id)
            return {"status": "aborted"}
```

**Pros:**
- ✅ Strong consistency (ACID across multiple databases)
- ✅ All-or-nothing guarantee

**Cons:**
- ❌ Blocking (participants wait for coordinator)
- ❌ Single point of failure (coordinator crashes)
- ❌ Slow (two network round-trips)
- ❌ Locks held during prepare phase (low availability)

**When to Use:**
- Critical transactions requiring strong consistency
- Small number of participants
- Short-lived transactions

**Not Used Much in Modern Systems** (replaced by SAGA for microservices)

---

## SAGA Pattern

**Concept:** Break distributed transaction into **sequence of local transactions**. Each step has a **compensating transaction** (undo).

**How it Works:**
```
Transaction: Book flight + Book hotel + Charge payment

SAGA Steps:
1. Book flight → Success
2. Book hotel → Success
3. Charge payment → FAILURE

Compensating Transactions (Undo):
3. (Skip, payment failed)
2. Cancel hotel booking ← Undo step 2
1. Cancel flight booking ← Undo step 1

Result: All compensated (rolled back)
```

**Two Types:**

### 1. Choreography SAGA (Event-Driven)

Each service listens to events and triggers next step.
```
Service A ──[Event: FlightBooked]──> Service B
Service B ──[Event: HotelBooked]───> Service C
Service C ──[Event: PaymentFailed]─> Service B
Service B ──[Event: CancelHotel]───> Service A
Service A ──[Event: CancelFlight]──> Done
```

**Example:**
```python
# Service A: Flight Booking
class FlightService:
    def book_flight(self, booking_id, flight_id):
        # Book flight locally
        flight_booking = FlightBooking.objects.create(
            booking_id=booking_id,
            flight_id=flight_id,
            status='booked'
        )
        
        # Publish event
        publish_event('FlightBooked', {
            'booking_id': booking_id,
            'flight_id': flight_id
        })
    
    def cancel_flight(self, booking_id):
        # Compensating transaction
        FlightBooking.objects.filter(booking_id=booking_id).update(status='cancelled')
        publish_event('FlightCancelled', {'booking_id': booking_id})

# Service B: Hotel Booking (listens to FlightBooked event)
class HotelService:
    def on_flight_booked(self, event):
        booking_id = event['booking_id']
        
        # Book hotel locally
        hotel_booking = HotelBooking.objects.create(
            booking_id=booking_id,
            status='booked'
        )
        
        # Publish event
        publish_event('HotelBooked', {'booking_id': booking_id})
    
    def on_payment_failed(self, event):
        # Compensating transaction
        booking_id = event['booking_id']
        HotelBooking.objects.filter(booking_id=booking_id).update(status='cancelled')
        publish_event('HotelCancelled', {'booking_id': booking_id})

# Service C: Payment (listens to HotelBooked event)
class PaymentService:
    def on_hotel_booked(self, event):
        booking_id = event['booking_id']
        
        try:
            # Charge payment
            charge_payment(booking_id, amount=500)
            publish_event('PaymentSuccess', {'booking_id': booking_id})
        except PaymentException:
            # Payment failed, trigger compensation
            publish_event('PaymentFailed', {'booking_id': booking_id})
```

**Pros:**
- ✅ No central coordinator
- ✅ Loose coupling between services
- ✅ Scalable

**Cons:**
- ❌ Complex to debug (distributed flow)
- ❌ Hard to understand overall flow
- ❌ Cyclic dependencies possible

---

### 2. Orchestration SAGA (Centralized)

Central orchestrator controls the flow.
```
Orchestrator:
1. Call Service A: Book flight
2. Call Service B: Book hotel
3. Call Service C: Charge payment (FAILS)
4. Call Service B: Cancel hotel (compensation)
5. Call Service A: Cancel flight (compensation)
```

**Example:**
```python
class BookingOrchestrator:
    def book_trip(self, user_id, flight_id, hotel_id, amount):
        booking_id = generate_booking_id()
        
        try:
            # Step 1: Book flight
            flight_result = FlightService.book_flight(booking_id, flight_id)
            if not flight_result['success']:
                raise Exception("Flight booking failed")
            
            # Step 2: Book hotel
            hotel_result = HotelService.book_hotel(booking_id, hotel_id)
            if not hotel_result['success']:
                # Compensate: Cancel flight
                FlightService.cancel_flight(booking_id)
                raise Exception("Hotel booking failed")
            
            # Step 3: Charge payment
            payment_result = PaymentService.charge(user_id, amount)
            if not payment_result['success']:
                # Compensate: Cancel hotel, then flight
                HotelService.cancel_hotel(booking_id)
                FlightService.cancel_flight(booking_id)
                raise Exception("Payment failed")
            
            # All steps successful
            return {"status": "success", "booking_id": booking_id}
        
        except Exception as e:
            # Compensation already done in try block
            return {"status": "failed", "error": str(e)}
```

**Pros:**
- ✅ Clear flow (easy to understand)
- ✅ Centralized logic
- ✅ Easier to debug

**Cons:**
- ❌ Single point of failure (orchestrator)
- ❌ Orchestrator can become complex
- ❌ Tight coupling to orchestrator

---

**SAGA vs 2PC:**

| Feature | 2PC | SAGA |
|---------|-----|------|
| Consistency | Strong (ACID) | Eventual |
| Locking | Yes (blocking) | No (local transactions) |
| Availability | Lower (blocks on failure) | Higher (continues on failure) |
| Complexity | Lower (built-in database support) | Higher (application logic) |
| Use Case | Critical transactions | Microservices, long-running |

**Real-World:**
- Banking core transactions: 2PC (strong consistency needed)
- E-commerce order flow: SAGA (better availability)

---

## Isolation Levels Recap

Quick reference (already covered in ACID):

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Performance |
|-------|------------|---------------------|--------------|-------------|
| Read Uncommitted | Possible | Possible | Possible | Fastest |
| Read Committed | ❌ | Possible | Possible | Fast |
| Repeatable Read | ❌ | ❌ | Possible | Moderate |
| Serializable | ❌ | ❌ | ❌ | Slowest |

**Most Common:** Read Committed (PostgreSQL/MySQL default)

---

## Interview Questions

### Q1: What is the difference between pessimistic and optimistic locking?

**Answer:**

**Pessimistic Locking:**
- Locks data **before** reading/writing
- Assumes conflicts will happen
- Blocks other transactions
- Use `SELECT FOR UPDATE`

**Optimistic Locking:**
- No locks, check for conflicts **before commit**
- Assumes conflicts are rare
- Uses version numbers or timestamps
- Retries on conflict

**When to use:**
- Pessimistic: High contention (banking, inventory)
- Optimistic: Low contention (social media, CMS)

---

### Q2: How does MVCC improve concurrency?

**Answer:**

**MVCC (Multi-Version Concurrency Control):**
- Database keeps multiple versions of each row
- Readers see consistent snapshot (no locks needed)
- Writers create new versions (don't block readers)

**Benefits:**
- Readers don't block writers ✅
- Writers don't block readers ✅
- High concurrency ✅

**Example:**
```
T1: Reads account balance = 1000 (Version 1)
T2: Updates balance to 900 (creates Version 2)
T1: Reads again, still sees 1000 (snapshot isolation)
```

**Used by:** PostgreSQL, MySQL InnoDB, Oracle

---

### Q3: Explain the SAGA pattern and when to use it.

**Answer:**

**SAGA Pattern:**
- Break distributed transaction into local transactions
- Each step has a compensating transaction (undo)
- Used in microservices instead of 2PC

**Example:**
```
Steps: Book flight → Book hotel → Charge payment
If payment fails:
Compensate: Cancel hotel → Cancel flight
```

**Types:**
1. **Choreography:** Event-driven, no coordinator
2. **Orchestration:** Central orchestrator controls flow

**When to use:**
- Microservices architecture
- Long-running transactions
- Need high availability over strong consistency

**Not for:** Critical transactions needing ACID (use 2PC instead)

---

### Q4: What is version-based locking and how does it work?

**Answer:**

**Version-Based Locking:**
- Track changes using version number or timestamp
- Check version before updating
- If version changed → Conflict → Retry

**Implementation:**
```python
class Product(models.Model):
    stock = models.IntegerField()
    version = models.IntegerField(default=0)

# Read version
product = Product.objects.get(id=1)
old_version = product.version  # version = 5

# Update with version check
updated = Product.objects.filter(
    id=1,
    version=old_version  # Check version = 5
).update(
    stock=F('stock') - 1,
    version=F('version') + 1
)

if updated == 0:
    # Version mismatch, someone else modified
    raise Exception("Conflict, retry")
```

**Benefits:**
- No database locks (optimistic)
- Works in distributed systems
- Simple to implement

---

### Q5: In a booking system, how would you prevent double booking using locking?

**Answer:**

**Pessimistic Locking (Recommended for bookings):**
```python
from django.db import transaction

def book_seat(user_id, seat_id):
    with transaction.atomic():
        # Lock seat row (exclusive lock)
        seat = Seat.objects.select_for_update().get(id=seat_id)
        
        if seat.is_booked:
            return {"success": False, "error": "Seat already booked"}
        
        # Mark as booked
        seat.is_booked = True
        seat.booked_by = user_id
        seat.save()
        
        # Create booking
        booking = Booking.objects.create(user_id=user_id, seat_id=seat_id)
        
        return {"success": True, "booking_id": booking.id}

# Concurrent requests:
# T1: Locks seat 5A
# T2: Waits for lock on seat 5A
# T1: Books seat, commits, releases lock
# T2: Acquires lock, sees seat.is_booked=True, returns error
```

**Why pessimistic:**
- High contention (many users booking same seats)
- Critical data (no double bookings allowed)
- Short transaction (lock held briefly)

---

### Q6: What is Two-Phase Commit (2PC)? What are its drawbacks?

**Answer:**

**Two-Phase Commit:**
- Ensures distributed transaction commits atomically
- **Phase 1:** Coordinator asks participants "Can you commit?" (Prepare)
- **Phase 2:** If all YES → Commit, else → Abort

**Drawbacks:**
1. **Blocking:** Participants wait for coordinator decision
2. **Single point of failure:** Coordinator crashes → Participants stuck
3. **Slow:** Two network round-trips
4. **Low availability:** Locks held during prepare phase

**Why not used in microservices:**
- SAGA pattern better (eventual consistency, high availability)

**Still used in:**
- Traditional databases (MySQL XA transactions)
- Critical banking transactions

---

### Q7: How does optimistic locking handle concurrent updates?

**Answer:**

**Optimistic Locking Flow:**
```
T1: Read product (version=5, stock=10)
T2: Read product (version=5, stock=10)

T1: Update stock to 9, version to 6
    UPDATE products SET stock=9, version=6 WHERE id=1 AND version=5
    → Success (1 row updated)

T2: Update stock to 8, version to 6
    UPDATE products SET stock=8, version=6 WHERE id=1 AND version=5
    → Failure (0 rows updated, version already 6)

T2: Retry
    Read product (version=6, stock=9)
    Update stock to 8, version to 7
    → Success
```

**Key:** Version check ensures only one transaction succeeds. Loser retries with fresh data.

---



### Q8: How would you implement a distributed transaction in microservices?

**Answer:**

**Use SAGA Pattern (Orchestration):**
```python
class OrderOrchestrator:
    def place_order(self, order_data):
        order_id = create_order_id()
        
        try:
            # Step 1: Reserve inventory
            inventory_result = InventoryService.reserve(order_data['items'])
            if not inventory_result['success']:
                raise Exception("Inventory reservation failed")
            
            # Step 2: Charge payment
            payment_result = PaymentService.charge(order_data['amount'])
            if not payment_result['success']:
                # Compensate: Release inventory
                InventoryService.release(order_data['items'])
                raise Exception("Payment failed")
            
            # Step 3: Create order record
            OrderService.create(order_id, order_data)
            
            # Step 4: Send confirmation email
            NotificationService.send_email(order_id)
            
            return {"success": True, "order_id": order_id}
        
        except Exception as e:
            # Compensation already handled in try block
            return {"success": False, "error": str(e)}
```

**Key:** Each service has local transaction + compensating transaction.

---

### Q10: When would you use Read Committed vs Repeatable Read isolation level?

**Answer:**

**Read Committed:**
- Most common default (PostgreSQL, MySQL)
- Prevents dirty reads
- Allows non-repeatable reads (same query, different results)

**Use when:**
- Most web applications (good balance)
- Moderate concurrency needed
- Don't need consistent snapshot

**Repeatable Read:**
- Stricter (prevents dirty + non-repeatable reads)
- Transaction sees snapshot at start time

**Use when:**
- Financial reports (need consistent snapshot)
- Booking systems (seat availability check)
- Analytics (data shouldn't change during analysis)

**Example:**
```sql
-- Read Committed:
T1: SELECT balance WHERE id=1;  → 1000
T2: UPDATE balance to 900; COMMIT;
T1: SELECT balance WHERE id=1;  → 900 (different!)

-- Repeatable Read:
T1: SELECT balance WHERE id=1;  → 1000
T2: UPDATE balance to 900; COMMIT;
T1: SELECT balance WHERE id=1;  → 1000 (same, snapshot)
```

---

## Resources

### Official Documentation
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL MVCC](https://www.postgresql.org/docs/current/mvcc-intro.html)
- [Django Transactions](https://docs.djangoproject.com/en/stable/topics/db/transactions/)

### Articles
- [Understanding MVCC](https://nagvekar.medium.com/understanding-multi-version-concurrency-control-mvcc-in-postgresql-a-comprehensive-guide-9b4f82153860)
- [SAGA Pattern - Microservices.io](https://microservices.io/patterns/data/saga.html)
- [Optimistic vs Pessimistic Locking](https://vladmihalcea.com/optimistic-vs-pessimistic-locking/)


---

**Summary Cheatsheet**
```
┌──────────────────────────────────────────────────────────┐
│         TRANSACTIONS & CONCURRENCY CONTROL               │
├──────────────────────────────────────────────────────────┤
│ Locking Strategies:                                      │
│  Pessimistic: Lock BEFORE modify (blocking)              │
│  Optimistic:  Check BEFORE commit (version check)        │
│  MVCC:        Multiple versions (readers don't block)    │
├──────────────────────────────────────────────────────────┤
│ Pessimistic Locking:                                     │
│  SELECT ... FOR UPDATE (exclusive lock)                  │
│  Use: High contention, critical data                     │
├──────────────────────────────────────────────────────────┤
│ Optimistic Locking:                                      │
│  Version number check before update                      │
│  Retry on conflict                                       │
│  Use: Low contention, long transactions                  │
├──────────────────────────────────────────────────────────┤
│ Distributed Transactions:                                │
│  2PC:  Strong consistency, blocking, slow                │
│  SAGA: Eventual consistency, non-blocking, scalable      │
├──────────────────────────────────────────────────────────┤
│ SAGA Types:                                              │
│  Choreography: Event-driven, decentralized               │
│  Orchestration: Central coordinator, easier to debug     │
├──────────────────────────────────────────────────────────┤
│ Use Cases:                                               │
│  Banking transfers: Pessimistic + 2PC                    │
│  E-commerce orders: Optimistic + SAGA                    │
│  Booking systems: Pessimistic locking                    │
│  Social media: MVCC + Optimistic                         │
└──────────────────────────────────────────────────────────┘
```
---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** March 2026