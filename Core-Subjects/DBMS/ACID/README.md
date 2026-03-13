# ACID Properties - Complete Guide

## Table of Contents
1. [Introduction](#introduction)
2. [What are ACID Properties?](#what-are-acid-properties)
3. [Atomicity](#atomicity)
   - [What is Atomicity?](#what-is-atomicity)
   - [How Databases Ensure Atomicity](#how-databases-ensure-atomicity)
   - [Code Examples - Atomicity](#code-examples---atomicity)
4. [Consistency](#consistency)
   - [What is Consistency?](#what-is-consistency)
   - [Consistency vs Integrity](#consistency-vs-integrity)
   - [Code Examples - Consistency](#code-examples---consistency)
5. [Isolation](#isolation)
   - [What is Isolation?](#what-is-isolation)
   - [Isolation Levels](#isolation-levels)
   - [When to Use Which Isolation Level](#when-to-use-which-isolation-level)
   - [Code Examples - Isolation](#code-examples---isolation)
6. [Durability](#durability)
   - [What is Durability?](#what-is-durability)
   - [How Databases Ensure Durability](#how-databases-ensure-durability)
   - [WAL and Crash Recovery](#wal-and-crash-recovery)
7. [ACID in Real-World Applications](#acid-in-real-world-applications)
8. [ACID vs BASE (NoSQL)](#acid-vs-base-nosql)
9. [Interview Questions](#interview-questions)
10. [Resources](#resources)

---

## Introduction

**ACID** is a set of properties that guarantee reliable processing of database transactions. These properties ensure data integrity and consistency even in the presence of errors, crashes, or concurrent access.

**Why ACID Matters:**
- Banking systems: Money transfers must be reliable
- E-commerce: Inventory updates must be consistent
- Booking systems: No double bookings
- Any critical application where data correctness is non-negotiable

---

## What are ACID Properties?

ACID stands for:

| Property | What it Guarantees | Example |
|----------|-------------------|---------|
| **A - Atomicity** | Transaction is all-or-nothing | Money transfer: Both debit and credit happen, or neither |
| **C - Consistency** | Database moves from one valid state to another | Account balance never negative (if rule exists) |
| **I - Isolation** | Concurrent transactions don't interfere | Two users booking same seat see consistent state |
| **D - Durability** | Committed data survives crashes | After "Payment Successful", data persists even if server crashes |

---

## Atomicity

### What is Atomicity?

**Definition:** A transaction is **atomic** - it either completes entirely or has no effect at all. There's no partial completion.

**Analogy:**
```
Buying a product online:
1. Deduct money from wallet
2. Deduct item from inventory
3. Create order record

Atomicity ensures:
✅ Either ALL 3 happen
❌ OR NONE happen

Not possible: Money deducted but order not created (partial state)
```

### Real-World Example

**Bank Transfer:**
```sql
BEGIN TRANSACTION;

-- Step 1: Deduct $100 from Account A
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'A';

-- Step 2: Add $100 to Account B
UPDATE accounts SET balance = balance + 100 WHERE account_id = 'B';

COMMIT;

-- Atomicity guarantees:
-- If Step 1 succeeds but Step 2 fails (server crash, network error)
-- → Database automatically ROLLS BACK Step 1
-- → Money doesn't disappear
```

**Without Atomicity (Disaster):**
```
Step 1: ✅ Deducted $100 from Account A (balance = $400)
[CRASH - Power failure]
Step 2: ❌ Never added $100 to Account B

Result: $100 disappeared! Account A lost money, Account B didn't receive it.
```

**With Atomicity (Safe):**
```
Step 1: ✅ Deducted $100 from Account A
[CRASH - Power failure]
Database on restart: "Step 2 never committed, ROLLBACK Step 1"
Step 1: ⏪ Reversed (balance back to $500)

Result: Transaction never happened (safe state)
```

---

### How Databases Ensure Atomicity

Databases use **Transaction Logs (Write-Ahead Logging)** to ensure atomicity.

#### Mechanism:
```
1. BEGIN TRANSACTION
   ↓
2. Write operation to LOG FILE first (not actual data yet)
   LOG: "Will update Account A: balance 500 → 400"
   ↓
3. Write operation to LOG FILE
   LOG: "Will update Account B: balance 200 → 300"
   ↓
4. COMMIT (mark in log)
   LOG: "TRANSACTION COMMITTED"
   ↓
5. Now apply changes to actual database files
   ↓
6. Done

If crash happens:
- Before COMMIT log entry → ROLLBACK (undo using log)
- After COMMIT log entry → REDO (complete using log)
```

#### Example: What Happens at 900/1000 Operations

**Scenario:** Database executing 1000 INSERT operations, crashes at 900th operation.
```
Transaction:
INSERT INTO orders (id, user_id, amount) VALUES (1, 101, 50);
INSERT INTO orders (id, user_id, amount) VALUES (2, 102, 75);
...
INSERT INTO orders (id, user_id, amount) VALUES (900, 999, 100);  ← CRASH HERE
INSERT INTO orders (id, user_id, amount) VALUES (901, 1000, 120); ← Never executed
...
INSERT INTO orders (id, user_id, amount) VALUES (1000, 1099, 90);

Database Recovery Process:
1. Database restarts
2. Reads transaction log
3. Finds: "Transaction started but NO COMMIT entry"
4. ROLLBACK all 900 operations using UNDO log
5. Database back to state before transaction started
6. All 900 inserts are reversed (atomicity preserved)
```

**Key Point:** Database doesn't do operations 901-1000. It **rolls back** all 900 operations already done.

---

### Code Examples - Atomicity

#### Example 1: Django ORM Transaction (Atomic)
```python
from django.db import transaction
from django.db.models import F

def transfer_money(from_account_id, to_account_id, amount):
    """
    Atomic money transfer - either both updates happen or neither
    """
    try:
        with transaction.atomic():  # Start atomic transaction
            # Step 1: Deduct from sender
            from_account = Account.objects.select_for_update().get(id=from_account_id)
            
            if from_account.balance < amount:
                raise ValueError("Insufficient balance")
            
            from_account.balance -= amount
            from_account.save()
            
            # Step 2: Add to receiver
            to_account = Account.objects.select_for_update().get(id=to_account_id)
            to_account.balance += amount
            to_account.save()
            
            # Both steps successful → COMMIT automatically
            return {"success": True, "message": "Transfer successful"}
    
    except Exception as e:
        # ANY error → Automatic ROLLBACK
        # Both updates reversed, money not lost
        return {"success": False, "error": str(e)}

# Usage
result = transfer_money(from_account_id=1, to_account_id=2, amount=100)

# If crash happens after Step 1:
# - Django/PostgreSQL automatically rolls back Step 1
# - No partial state (atomicity preserved)
```

---

#### Example 2: Movie Ticket Booking (Atomic)
```python
from django.db import transaction

def book_movie_tickets(user_id, seat_ids, movie_id):
    """
    Book multiple seats atomically
    Either all seats booked or none (no partial booking)
    """
    try:
        with transaction.atomic():
            # Step 1: Check all seats available
            seats = Seat.objects.select_for_update().filter(
                id__in=seat_ids,
                is_booked=False
            )
            
            if len(seats) != len(seat_ids):
                raise ValueError("Some seats already booked")
            
            # Step 2: Update all seats
            for seat in seats:
                seat.is_booked = True
                seat.booked_by_user_id = user_id
                seat.save()
            
            # Step 3: Create booking record
            booking = Booking.objects.create(
                user_id=user_id,
                movie_id=movie_id,
                seats=list(seats),
                total_amount=len(seats) * 100
            )
            
            # Step 4: Deduct money from wallet
            wallet = Wallet.objects.select_for_update().get(user_id=user_id)
            if wallet.balance < booking.total_amount:
                raise ValueError("Insufficient wallet balance")
            
            wallet.balance -= booking.total_amount
            wallet.save()
            
            # All 4 steps successful → COMMIT
            return {"success": True, "booking_id": booking.id}
    
    except Exception as e:
        # ANY failure → ROLLBACK all steps
        # Seats unmarked, booking deleted, money not deducted
        return {"success": False, "error": str(e)}

# Atomicity ensures:
# ✅ All 4 steps happen together
# ❌ Or none happen (if crash/error at any step)
```

---

#### Example 3: Non-Atomic vs Atomic (Comparison)
```python
# ❌ BAD: Non-Atomic (Dangerous!)
def transfer_money_bad(from_id, to_id, amount):
    # NO transaction wrapper
    from_account = Account.objects.get(id=from_id)
    from_account.balance -= amount
    from_account.save()  # COMMITTED to database immediately
    
    # If crash happens here, money lost!
    
    to_account = Account.objects.get(id=to_id)
    to_account.balance += amount
    to_account.save()

# ✅ GOOD: Atomic (Safe!)
def transfer_money_good(from_id, to_id, amount):
    with transaction.atomic():  # Atomic wrapper
        from_account = Account.objects.get(id=from_id)
        from_account.balance -= amount
        from_account.save()
        
        # Even if crash here, first save will be rolled back
        
        to_account = Account.objects.get(id=to_id)
        to_account.balance += amount
        to_account.save()
    
    # COMMIT happens only after this block (both saves together)
```

---

## Consistency

### What is Consistency?

**Definition:** A transaction brings the database from one **valid state** to another **valid state**. All database rules (constraints, triggers, cascades) are enforced.

**Analogy:**
```
Database Rule: "Total money in system = constant"

Before Transaction:
Account A: $500
Account B: $200
Total: $700

After Transaction (Transfer $100 from A to B):
Account A: $400
Account B: $300
Total: $700  ✅ (Rule maintained)

Consistency ensures total never becomes $600 or $800 (invalid state)
```

### Real-World Example

**E-commerce Inventory:**
```sql
-- Database Constraint
ALTER TABLE products ADD CONSTRAINT check_stock 
CHECK (stock_quantity >= 0);  -- Stock can't be negative

-- Transaction
BEGIN TRANSACTION;

UPDATE products SET stock_quantity = stock_quantity - 5 
WHERE product_id = 123;

-- If this makes stock = -2, database REJECTS transaction
-- Consistency: Database never in invalid state (negative stock)

COMMIT;
```

---

### Consistency vs Integrity

| Feature | Consistency | Integrity |
|---------|-------------|-----------|
| **Definition** | Database moves from valid state to valid state | Database enforces rules/constraints |
| **Scope** | Transaction-level guarantee | Database-level rules |
| **Example** | Transfer maintains total balance | Foreign key constraint prevents orphan records |
| **Enforced By** | Transaction logic + constraints | Database constraints, triggers |

**Simple Explanation:**
- **Integrity** = Rules of the database (constraints, foreign keys, data types)
- **Consistency** = Transactions respect these rules

**Example:**
```python
# Database Integrity Rules (Constraints)
class Account(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(balance__gte=0),
                name='balance_non_negative'
            )
        ]

# Consistency: Transaction respects integrity rule
def withdraw_money(account_id, amount):
    with transaction.atomic():
        account = Account.objects.get(id=account_id)
        
        # Check before update (application-level consistency)
        if account.balance < amount:
            raise ValueError("Insufficient balance")
        
        account.balance -= amount
        account.save()  # Database also checks constraint (database-level integrity)

# If we try to violate constraint:
withdraw_money(account_id=1, amount=1000)  # Balance = $500
# Raises: IntegrityError (constraint violation)
# Transaction rolled back → Consistency maintained
```

---

### Code Examples - Consistency

#### Example: Order Processing with Consistency
```python
from django.db import transaction, IntegrityError

def process_order(user_id, product_id, quantity):
    """
    Ensure database consistency during order processing
    All business rules enforced
    """
    try:
        with transaction.atomic():
            # Rule 1: Product must exist
            product = Product.objects.select_for_update().get(id=product_id)
            
            # Rule 2: Sufficient stock
            if product.stock < quantity:
                raise ValueError("Insufficient stock")
            
            # Rule 3: User must have enough money
            user = User.objects.select_for_update().get(id=user_id)
            total_cost = product.price * quantity
            
            if user.wallet_balance < total_cost:
                raise ValueError("Insufficient balance")
            
            # All rules validated, proceed with transaction
            
            # Update 1: Deduct stock
            product.stock -= quantity
            product.save()
            
            # Update 2: Deduct money
            user.wallet_balance -= total_cost
            user.save()
            
            # Update 3: Create order
            order = Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                total_amount=total_cost
            )
            
            # COMMIT: All updates together, all rules satisfied
            # Database in consistent state
            return {"success": True, "order_id": order.id}
    
    except IntegrityError as e:
        # Database constraint violated (integrity error)
        # Automatic rollback → Consistency preserved
        return {"success": False, "error": "Database constraint violated"}
    
    except Exception as e:
        # Business rule violation
        # Automatic rollback → Consistency preserved
        return {"success": False, "error": str(e)}

# Consistency ensures:
# - Stock never negative
# - Wallet never negative
# - Order only created if both stock and money sufficient
# - Database always in valid state
```

---

## Isolation

### What is Isolation?

**Definition:** Concurrent transactions execute as if they are running **serially** (one after another), even though they run simultaneously. Transactions don't interfere with each other.

**Analogy:**
```
Two people booking movie tickets at same time:

Without Isolation:
- User A sees Seat 5A available
- User B sees Seat 5A available
- Both click "Book"
- Both get confirmation
- Result: Double booking! 😱

With Isolation:
- User A's transaction locks Seat 5A
- User B's transaction waits
- User A completes booking
- User B sees Seat 5A unavailable
- Result: No double booking ✅
```

---

### Isolation Levels

Databases provide **4 standard isolation levels**, each with different trade-offs between consistency and performance.

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Performance |
|----------------|------------|---------------------|--------------|-------------|
| **Read Uncommitted** | ✅ Possible | ✅ Possible | ✅ Possible | Fastest |
| **Read Committed** | ❌ Prevented | ✅ Possible | ✅ Possible | Fast |
| **Repeatable Read** | ❌ Prevented | ❌ Prevented | ✅ Possible | Moderate |
| **Serializable** | ❌ Prevented | ❌ Prevented | ❌ Prevented | Slowest |

---

#### 1. Read Uncommitted (Lowest Isolation)

**What it allows:** Transaction can read **uncommitted changes** from other transactions.

**Problem: Dirty Read**
```sql
-- Transaction T1
BEGIN;
UPDATE accounts SET balance = 500 WHERE id = 1;  -- Not committed yet

-- Transaction T2 (Read Uncommitted)
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Reads 500 (uncommitted!)

-- Transaction T1
ROLLBACK;  -- Oops, change reverted

-- Transaction T2 read wrong data (500 instead of original value)
-- This is a DIRTY READ
```

**When to use:** Almost never in production (too risky). Maybe for analytics where exact numbers don't matter.

---

#### 2. Read Committed (Default in PostgreSQL)

**What it prevents:** Dirty reads (can only read committed data)

**Problem: Non-Repeatable Read**
```sql
-- Transaction T1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Reads 1000

-- Transaction T2
BEGIN;
UPDATE accounts SET balance = 500 WHERE id = 1;
COMMIT;  -- Committed

-- Transaction T1 (still running)
SELECT balance FROM accounts WHERE id = 1;  -- Reads 500 (changed!)

-- Same query, different result within same transaction
-- This is NON-REPEATABLE READ
```

**When to use:** Default for most applications. Good balance of consistency and performance.

---

#### 3. Repeatable Read (PostgreSQL Default for Transactions)

**What it prevents:** Dirty reads + Non-repeatable reads

**How it works:** Transaction sees snapshot of database at transaction start.
```sql
-- Transaction T1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Reads 1000

-- Transaction T2
BEGIN;
UPDATE accounts SET balance = 500 WHERE id = 1;
COMMIT;

-- Transaction T1 (still running)
SELECT balance FROM accounts WHERE id = 1;  -- Still reads 1000!
-- Sees snapshot from transaction start
COMMIT;

-- Now reads 500 (after commit)
```

**Problem: Phantom Read**
```sql
-- Transaction T1
BEGIN;
SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Returns 5

-- Transaction T2
BEGIN;
INSERT INTO orders (status) VALUES ('pending');
COMMIT;

-- Transaction T1 (Repeatable Read)
SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Still returns 5 (good)

-- But if using range query:
SELECT * FROM orders WHERE status = 'pending';
-- Might see new row (phantom) in some databases
```

**When to use:** Financial transactions, booking systems where consistency is critical.

---

#### 4. Serializable (Highest Isolation)

**What it prevents:** All anomalies (dirty read, non-repeatable read, phantom read)

**How it works:** Transactions execute as if one after another (serialized).
```sql
-- Transaction T1
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT SUM(balance) FROM accounts;  -- Total: 5000

-- Transaction T2
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
INSERT INTO accounts (balance) VALUES (1000);
COMMIT;

-- Transaction T1
SELECT SUM(balance) FROM accounts;  -- Still 5000 (no phantom)
COMMIT;

-- Now SUM is 6000 (after both transactions complete)
```

**When to use:** Critical operations where absolute consistency needed (rare). Very slow.

---

### When to Use Which Isolation Level?
```
┌─────────────────────────────────────────────────────┐
│              ISOLATION LEVEL DECISION                │
├─────────────────────────────────────────────────────┤
│ Analytics, Reporting (approx data)                  │
│   → Read Uncommitted (fastest, inconsistent)        │
├─────────────────────────────────────────────────────┤
│ Most Web Apps, APIs, CRUD operations                │
│   → Read Committed (default, balanced)              │
├─────────────────────────────────────────────────────┤
│ Banking, Payments, Booking Systems                  │
│   → Repeatable Read (consistent snapshot)           │
├─────────────────────────────────────────────────────┤
│ Stock Trading, Critical Financial (rare)            │
│   → Serializable (slowest, fully consistent)        │
└─────────────────────────────────────────────────────┘
```

**Performance Impact:**
```
Read Uncommitted    → 100% throughput (no locks)
Read Committed      → 90% throughput  (short locks)
Repeatable Read     → 70% throughput  (longer locks, snapshot overhead)
Serializable        → 40% throughput  (full serialization, highest overhead)

As isolation increases:
✅ Consistency increases
❌ Performance decreases
```

---

### Code Examples - Isolation

#### Example: Setting Isolation Level in Django
```python
from django.db import transaction

# Default: Read Committed
def transfer_default(from_id, to_id, amount):
    with transaction.atomic():
        # Uses database default isolation (Read Committed)
        from_account = Account.objects.select_for_update().get(id=from_id)
        from_account.balance -= amount
        from_account.save()
        
        to_account = Account.objects.select_for_update().get(id=to_id)
        to_account.balance += amount
        to_account.save()

# Explicit: Repeatable Read (PostgreSQL)
def transfer_repeatable_read(from_id, to_id, amount):
    from django.db import connection
    
    with transaction.atomic():
        # Set isolation level
        with connection.cursor() as cursor:
            cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
        
        from_account = Account.objects.select_for_update().get(id=from_id)
        from_account.balance -= amount
        from_account.save()
        
        to_account = Account.objects.select_for_update().get(id=to_id)
        to_account.balance += amount
        to_account.save()

# Explicit: Serializable (Highest Isolation)
def transfer_serializable(from_id, to_id, amount):
    from django.db import connection
    
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        
        from_account = Account.objects.select_for_update().get(id=from_id)
        from_account.balance -= amount
        from_account.save()
        
        to_account = Account.objects.select_for_update().get(id=to_id)
        to_account.balance += amount
        to_account.save()
```

---

#### Example: Isolation in Movie Booking
```python
from django.db import transaction

def book_seat_with_isolation(user_id, seat_id):
    """
    Book seat with appropriate isolation to prevent double booking
    """
    try:
        with transaction.atomic():
            # Repeatable Read: Ensures consistent snapshot
            # No other transaction can modify this seat until we commit
            
            seat = Seat.objects.select_for_update().get(
                id=seat_id,
                is_booked=False  # Check availability
            )
            
            # If we reach here, seat is available and locked
            seat.is_booked = True
            seat.booked_by = user_id
            seat.save()
            
            # Create booking
            booking = Booking.objects.create(
                user_id=user_id,
                seat=seat,
                amount=100
            )
            
            # COMMIT: Seat booked, lock released
            return {"success": True, "booking_id": booking.id}
    
    except Seat.DoesNotExist:
        # Seat already booked by another transaction
        return {"success": False, "error": "Seat already booked"}

# Two users trying to book same seat:
# User 1: book_seat_with_isolation(user_id=1, seat_id=5)
# User 2: book_seat_with_isolation(user_id=2, seat_id=5)

# With proper isolation:
# User 1's transaction locks seat
# User 2's transaction waits (or gets DoesNotExist if User 1 commits first)
# Only ONE booking succeeds (no double booking)
```

---

## Durability

### What is Durability?

**Definition:** Once a transaction is **committed**, the changes are **permanent**, even if the system crashes immediately after.

**Analogy:**
```
Online Payment:
1. You click "Pay Now"
2. Screen shows "Payment Successful" (transaction committed)
3. Server crashes immediately after

Durability ensures:
✅ Your payment is recorded (money deducted, order created)
❌ NOT: Payment lost due to crash

Even if server crashes, database restarts, or power fails,
committed transaction persists.
```

---

### How Databases Ensure Durability

Databases use multiple mechanisms to ensure durability:

#### 1. Write-Ahead Logging (WAL)

**Concept:** Write changes to **log file first** (on disk), then update actual database files.
```
Normal Write (Without WAL):
1. UPDATE accounts SET balance = 500 WHERE id = 1
2. Write directly to database file (accounts.db)
3. [CRASH] → Data lost if not yet written to disk

With WAL (Safe):
1. UPDATE accounts SET balance = 500 WHERE id = 1
2. Write to LOG FILE first: "account_id=1, old_balance=1000, new_balance=500"
3. Flush log to disk (fsync - force write)
4. COMMIT (mark in log)
5. Later, apply to actual database file (can be delayed)

If crash happens:
- Log already on disk (durable)
- On restart, database replays log (REDO)
- Data recovered ✅
```

**Why WAL is Fast:**
- Log writes are **sequential** (fast disk I/O)
- Database file writes are **random** (slow disk I/O)
- WAL allows batching database file updates

---

#### 2. COMMIT Guarantees

**What happens when you COMMIT:**
```
Application:
COMMIT;

Database Internally:
1. Write all transaction changes to WAL (log file)
2. Call fsync() → Force OS to write log to physical disk
3. Wait for disk to confirm write (durable)
4. Return "COMMIT SUCCESS" to application

Only after step 4 does application see success.
```

**Question: What if OS crashes before disk write?**

**Answer:** Database **blocks COMMIT** until disk confirms write.
```python
# PostgreSQL ensures this:
def commit_transaction():
    # 1. Write to WAL buffer (in memory)
    write_to_wal_buffer(transaction_data)
    
    # 2. Flush WAL buffer to disk (CRITICAL)
    fsync(wal_file)  # Blocks until disk confirms
    
    # 3. Only now, return success
    return "COMMIT SUCCESS"

# User sees "Payment Successful" ONLY after data is on disk
```

---

#### 3. OS Cache and Disk Write

**Problem:** OS has write cache (buffer). Writes go to cache first, then disk later.
```
Application → Database → OS Write Cache → Physical Disk
                            ↑
                         (in RAM, volatile!)

If power fails here, data lost!
```

**Solution: fsync() System Call**
```python
# Database forces OS to write to disk immediately
import os

file = open("wal.log", "a")
file.write("TRANSACTION DATA")
file.flush()  # Flush to OS cache

os.fsync(file.fileno())  # Force OS to write to physical disk
# Only returns after disk write confirmed

# Now data is DURABLE (survives power failure)
```

---

#### 4. Modern SSDs and Capacitors

**Question:** What if power fails while SSD is writing?

**Answer:** Modern enterprise SSDs have **supercapacitors**.
```
Power Failure Detection:
1. SSD detects voltage drop (power failing)
2. Supercapacitor activates (provides power for ~1 second)
3. SSD quickly writes all cached data to NAND flash
4. Ensures no data loss

Consumer SSDs: May not have capacitors (risk of data loss on power failure)
Enterprise SSDs: Have capacitors (safe for databases)
```

**Battery-Backed RAID Controllers:**
```
RAID Controller has battery backup
↓
Cache contents written to flash on power loss
↓
On restore power, cache restored
↓
Writes completed
```

---

### WAL and Crash Recovery

#### Scenario: Database Crashes Mid-Transaction

**Without WAL:**
```
Transaction:
1. UPDATE account SET balance = 500 WHERE id = 1  ✅ Written to disk
2. UPDATE account SET balance = 1500 WHERE id = 2 ❌ CRASH before write

Result: Inconsistent state (partial transaction)
```

**With WAL:**
```
Transaction:
1. Write to WAL: "UPDATE account 1: balance=500"
2. Write to WAL: "UPDATE account 2: balance=1500"
3. Write to WAL: "COMMIT"
4. Flush WAL to disk (durable)
5. [CRASH before applying to database files]

Recovery:
1. Database restarts
2. Reads WAL log
3. Finds: "COMMIT" entry exists
4. REDO: Apply both updates from WAL to database
5. Database consistent ✅

If no COMMIT in WAL:
→ UNDO: Discard transaction (atomicity)
```

---

#### Example: 900/1000 Operations Crash

**Scenario:** Inserting 1000 rows, crash at row 900.
```
Transaction:
BEGIN;
INSERT INTO orders VALUES (1, ...);
INSERT INTO orders VALUES (2, ...);
...
INSERT INTO orders VALUES (900, ...);  ← CRASH
INSERT INTO orders VALUES (901, ...);  ← Never reached
...

WAL Log:
"BEGIN TRANSACTION"
"INSERT row 1"
"INSERT row 2"
...
"INSERT row 900"
[No COMMIT entry]

Recovery:
1. Database restarts
2. Reads WAL
3. Finds: No COMMIT → Transaction incomplete
4. UNDO: Rollback all 900 inserts using UNDO log
5. Database back to state before transaction

Result: Atomicity + Durability preserved
```

**Key Point:** Even though 900 operations were logged, absence of COMMIT means entire transaction rolled back.

---

### Code Examples - Durability

Durability is mostly handled by database engine, but here's how you ensure it:
```python
from django.db import transaction, connection

def ensure_durability():
    """
    Ensure transaction is durable before returning success
    """
    with transaction.atomic():
        # Perform updates
        account = Account.objects.get(id=1)
        account.balance = 500
        account.save()
        
        # Django/PostgreSQL ensures:
        # 1. Changes written to WAL
        # 2. WAL flushed to disk (fsync)
        # 3. COMMIT only after disk confirmation
        
        # When this block exits, COMMIT is durable
    
    # If code reaches here, transaction is DURABLE
    # Survives server crash, power failure
    return "Transaction committed and durable"

# Database configuration for durability
# In PostgreSQL settings:
# synchronous_commit = on  (default - ensures fsync before COMMIT)
# fsync = on                (forces disk writes)
# wal_sync_method = fsync   (how to force writes)

# Trade-off:
# synchronous_commit = off  → Faster (but may lose last few transactions on crash)
# synchronous_commit = on   → Slower (but fully durable)
```

---

## ACID in Real-World Applications

### Example: E-commerce Order Processing
```python
from django.db import transaction

def process_order_with_acid(user_id, product_id, quantity):
    """
    Demonstrates all ACID properties in one transaction
    """
    try:
        with transaction.atomic():  # ATOMICITY: All or nothing
            
            # CONSISTENCY: Enforce business rules
            product = Product.objects.select_for_update().get(id=product_id)
            if product.stock < quantity:
                raise ValueError("Insufficient stock")
            
            user = User.objects.select_for_update().get(id=user_id)
            total_cost = product.price * quantity
            if user.wallet < total_cost:
                raise ValueError("Insufficient balance")
            
            # ISOLATION: Locks prevent concurrent modifications
            # Other transactions wait until this completes
            
            # Update 1: Deduct stock
            product.stock -= quantity
            product.save()
            
            # Update 2: Deduct money
            user.wallet -= total_cost
            user.save()
            
            # Update 3: Create order
            order = Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                total=total_cost
            )
            
            # COMMIT: DURABILITY ensured
            # After this, even if server crashes, order persists
            
            return {"success": True, "order_id": order.id}
    
    except Exception as e:
        # ATOMICITY: Automatic rollback on error
        # All changes reversed
        return {"success": False, "error": str(e)}

# ACID Properties in Action:
# A - All 3 updates happen together or none
# C - Stock/wallet constraints enforced
# I - No other transaction can modify product/user during this
# D - Once success returned, order survives any crash
```

---

## ACID vs BASE (NoSQL)

| Property | ACID (SQL) | BASE (NoSQL) |
|----------|-----------|--------------|
| **A - Atomicity** | Strict (all-or-nothing) | Eventual (may see partial updates) |
| **C - Consistency** | Immediate (always consistent) | Eventual (eventually consistent) |
| **I - Isolation** | Strong (full isolation levels) | Weak (limited isolation) |
| **D - Durability** | Guaranteed (WAL, fsync) | Configurable (may trade for speed) |
| **Use Case** | Banking, payments, bookings | Social media, analytics, caching |
| **Example** | PostgreSQL, MySQL | MongoDB, Cassandra, DynamoDB |

**When to Use ACID:**
- Money transactions
- Booking systems
- Any critical data that must be accurate

**When to Use BASE:**
- Social media feeds (eventual consistency okay)
- Analytics (approximate data acceptable)
- High-throughput systems (speed > strict consistency)

---

## Interview Questions

### Q1: What are ACID properties? Explain each briefly.

**Answer:**
- **Atomicity:** Transaction is all-or-nothing (either complete or no effect)
- **Consistency:** Database moves from one valid state to another (rules enforced)
- **Isolation:** Concurrent transactions don't interfere (appear serial)
- **Durability:** Committed data survives crashes (permanent)

---

### Q2: How does a database ensure atomicity?

**Answer:**
Databases use **Write-Ahead Logging (WAL)**:
1. Write transaction changes to log file first
2. Mark COMMIT in log
3. Flush log to disk
4. Apply changes to database files

On crash:
- If COMMIT in log → REDO (complete transaction)
- If no COMMIT → UNDO (rollback transaction)

---

### Q3: What happens if database crashes at 900th operation out of 1000?

**Answer:**
Database uses **transaction log**:
1. On restart, check log for COMMIT entry
2. If no COMMIT → Transaction incomplete
3. **ROLLBACK all 900 operations** using UNDO log
4. Database back to state before transaction started

**Key:** Even 900 operations are reversed (atomicity preserved)

---

### Q4: Difference between consistency and integrity?

**Answer:**
- **Integrity:** Database rules/constraints (foreign keys, check constraints, data types)
- **Consistency:** Transactions respect integrity rules and move DB from valid state to valid state

**Example:**
- Integrity: `CHECK (balance >= 0)` constraint
- Consistency: Transaction ensures balance never goes negative

---

### Q5: What are the 4 isolation levels? When to use each?

**Answer:**

| Level | Anomalies Prevented | Use Case |
|-------|-------------------|----------|
| Read Uncommitted | None | Analytics (approx data) |
| Read Committed | Dirty reads | Most web apps (default) |
| Repeatable Read | Dirty + Non-repeatable reads | Banking, bookings |
| Serializable | All anomalies | Critical financial (rare) |

---

### Q6: What is dirty read? Give example.

**Answer:**
**Dirty read:** Reading **uncommitted** data from another transaction.

**Example:**
```sql
T1: UPDATE balance = 500;  -- Not committed
T2: SELECT balance;  -- Reads 500 (dirty!)
T1: ROLLBACK;  -- Reverted to original

T2 read wrong data (500 instead of original value)
```

**Solution:** Use Read Committed or higher isolation.

---

### Q7: How does database ensure durability?

**Answer:**
Databases use multiple techniques:
1. **WAL (Write-Ahead Logging):** Write to log first, then database
2. **fsync():** Force OS to write to physical disk (not just cache)
3. **COMMIT blocking:** Don't return success until disk confirms write
4. **Modern SSDs:** Supercapacitors ensure data written even on power failure

**COMMIT only succeeds after data is on disk (durable).**

---

### Q8: What is fsync and why is it important?

**Answer:**
**fsync()** is a system call that forces OS to write cached data to physical disk.

**Without fsync:**
```
Write → OS Cache (in RAM) → [POWER FAILURE] → Data lost
```

**With fsync:**
```
Write → OS Cache → fsync() → Physical Disk → Data safe
```

Databases call fsync before COMMIT to ensure durability.

---

### Q9: In a movie booking system, how do ACID properties prevent double booking?

**Answer:**

**Atomicity:** Either seat booked + payment deducted, or neither.

**Consistency:** Seat can't be `is_booked=True` for two users (violates business rule).

**Isolation:** When User 1 books seat, lock prevents User 2 from seeing it as available until User 1 commits.

**Durability:** After "Booking Successful", even if server crashes, booking persists.

**Code:**
```python
with transaction.atomic():  # Atomicity
    seat = Seat.objects.select_for_update().get(id=5, is_booked=False)  # Isolation (lock)
    seat.is_booked = True
    seat.save()  # Consistency (constraint checked)
    # COMMIT → Durability
```

---

### Q10: What is the trade-off between isolation levels?

**Answer:**
```
Higher Isolation:
✅ More consistency
✅ Fewer anomalies
❌ Lower performance (more locking)
❌ Lower concurrency

Lower Isolation:
✅ Higher performance
✅ More concurrency
❌ More anomalies
❌ Risk of inconsistent data
```

**Rule of Thumb:**
- Use **lowest isolation that maintains correctness** for your use case
- Most apps: Read Committed (default)
- Critical apps: Repeatable Read or Serializable

---

### Q11: Can you have atomicity without durability?

**Answer:**
**Theoretically yes, practically no.**

**Example:**
```
Transaction commits atomically (all-or-nothing)
But data only in memory (not disk)
→ Power failure → Data lost

Atomicity preserved (transaction completed fully)
But durability violated (data not permanent)
```

**In practice:** Databases ensure both together. COMMIT doesn't return until data is durable.

---

### Q12: What is WAL and why is it faster than direct writes?

**Answer:**
**WAL (Write-Ahead Log):** Write changes to sequential log file before updating database files.

**Why faster:**
- Log writes are **sequential** (disk head doesn't move much)
- Database writes are **random** (disk head jumps around)
- Sequential I/O is 100x faster than random I/O on HDDs

**Example:**
```
Direct write: 100 random disk seeks (slow)
WAL: 1 sequential log write + delayed database update (fast)
```

---

### Q13: How does PostgreSQL handle transaction isolation?

**Answer:**
PostgreSQL uses **MVCC (Multi-Version Concurrency Control)**:

1. Each transaction sees a **snapshot** of database at transaction start
2. Updates create **new row versions** (old version kept)
3. Each transaction reads its snapshot version
4. No locks needed for reads (high concurrency)
5. On COMMIT, old versions garbage collected

**Benefit:** Readers don't block writers, writers don't block readers.

---

### Q14: What is phantom read? How to prevent it?

**Answer:**
**Phantom read:** Same query returns different number of rows within same transaction.

**Example:**
```sql
T1: SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Returns 5
T2: INSERT INTO orders (status) VALUES ('pending');
T2: COMMIT;
T1: SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Returns 6 (phantom!)
```

**Prevention:** Use **Repeatable Read** or **Serializable** isolation.

---

### Q15: In Django, how do you ensure ACID properties for a money transfer?

**Answer:**
```python
from django.db import transaction

def transfer_money(from_id, to_id, amount):
    try:
        with transaction.atomic():  # Atomicity + Consistency
            # Isolation: select_for_update locks rows
            from_acc = Account.objects.select_for_update().get(id=from_id)
            to_acc = Account.objects.select_for_update().get(id=to_id)
            
            # Consistency check
            if from_acc.balance < amount:
                raise ValueError("Insufficient balance")
            
            from_acc.balance -= amount
            to_acc.balance += amount
            
            from_acc.save()
            to_acc.save()
            
            # COMMIT → Durability (PostgreSQL fsync to disk)
            return "Success"
    
    except Exception:
        # Atomicity: Auto rollback
        return "Failed"
```

**ACID:**
- A: Both updates or neither
- C: Balance constraint checked
- I: Locks prevent concurrent modifications
- D: After commit, survives crash

---

## Resources

### Official Documentation
- [PostgreSQL ACID Documentation](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [MySQL InnoDB ACID](https://dev.mysql.com/doc/refman/8.0/en/mysql-acid.html)
- [Django Transactions](https://docs.djangoproject.com/en/stable/topics/db/transactions/)

### Books
- **Database System Concepts** by Silberschatz (Chapter on Transactions)
- **Designing Data-Intensive Applications** by Martin Kleppmann (Chapter 7: Transactions)

### Articles
- [Understanding Database ACID Properties](https://vladmihalcea.com/a-beginners-guide-to-acid-and-database-transactions/)
- [PostgreSQL MVCC Explained](https://www.postgresql.org/docs/current/mvcc-intro.html)


---

**Summary Cheatsheet**
```
┌─────────────────────────────────────────────────────┐
│                 ACID QUICK REFERENCE                │
├─────────────────────────────────────────────────────┤
│ A - Atomicity                                       │
│   → All or nothing (no partial transactions)        │
│   → Ensured by: WAL, UNDO/REDO logs                 │
├─────────────────────────────────────────────────────┤
│ C - Consistency                                     │
│   → Valid state to valid state                      │
│   → Ensured by: Constraints + Transaction logic     │
├─────────────────────────────────────────────────────┤
│ I - Isolation                                       │
│   → Concurrent txns don't interfere                 │
│   → Levels: Read Uncommitted < Read Committed <     │
│              Repeatable Read < Serializable         │
│   → Trade-off: Consistency vs Performance           │
├─────────────────────────────────────────────────────┤
│ D - Durability                                      │
│   → Committed data survives crashes                 │
│   → Ensured by: WAL, fsync, disk writes             │
├─────────────────────────────────────────────────────┤
│ Production Best Practices:                          │
│   → Use transactions for multi-step operations      │
│   → Use appropriate isolation level                 │
│   → Trust database to handle durability             │
│   → Monitor transaction logs for issues             │
└─────────────────────────────────────────────────────┘
```

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** March 2026