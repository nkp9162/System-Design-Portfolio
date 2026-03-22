# SQL Joins - Complete Guide

## Table of Contents
1. [Introduction](#introduction)
2. [What are SQL Joins?](#what-are-sql-joins)
3. [Types of Joins](#types-of-joins)
   - [INNER JOIN](#inner-join)
   - [LEFT JOIN (LEFT OUTER JOIN)](#left-join-left-outer-join)
   - [RIGHT JOIN (RIGHT OUTER JOIN)](#right-join-right-outer-join)
   - [FULL OUTER JOIN](#full-outer-join)
   - [CROSS JOIN](#cross-join)
   - [SELF JOIN](#self-join)
4. [How Joins Work Internally](#how-joins-work-internally)
   - [Nested Loop Join](#nested-loop-join)
   - [Hash Join](#hash-join)
   - [Merge Join](#merge-join)
5. [How Database Chooses Join Method](#how-database-chooses-join-method)
6. [Join Performance and Optimization](#join-performance-and-optimization)
7. [Code Examples - Django ORM](#code-examples---django-orm)
8. [Interview Questions](#interview-questions)
9. [Resources](#resources)

---

## Introduction

**SQL Joins** are used to combine rows from two or more tables based on a related column between them. Instead of storing all data in one giant table, we split it into multiple tables (normalization) and use joins to retrieve related data.

**Why Joins are Important:**
- Avoid data duplication (normalization)
- Maintain data integrity
- Flexible querying across related data
- Reduce storage space

**Real-World Example:**
```
Without Joins (Bad - Denormalized):
orders table:
| order_id | product_name | product_price | user_name | user_email |
|----------|--------------|---------------|-----------|------------|
| 1        | Laptop       | 1000          | Alice     | alice@m.com|
| 2        | Mouse        | 20            | Alice     | alice@m.com|
| 3        | Keyboard     | 50            | Bob       | bob@m.com  |
→ Alice's email repeated (data duplication)

With Joins (Good - Normalized):
users table:
| user_id | name  | email       |
|---------|-------|-------------|
| 1       | Alice | alice@m.com |
| 2       | Bob   | bob@m.com   |

orders table:
| order_id | user_id | product_name | price |
|----------|---------|--------------|-------|
| 1        | 1       | Laptop       | 1000  |
| 2        | 1       | Mouse        | 20    |
| 3        | 2       | Keyboard     | 50    |

Query with JOIN:
SELECT orders.*, users.name, users.email
FROM orders
INNER JOIN users ON orders.user_id = users.user_id;

→ No duplication, flexible, efficient
```

---

## What are SQL Joins?

**Definition:** A JOIN clause combines rows from two or more tables based on a related column (usually foreign key).

**Basic Syntax:**
```sql
SELECT columns
FROM table1
JOIN table2 ON table1.column = table2.column;
```

**Visual Representation:**
```
Table A (users):          Table B (orders):
| user_id | name  |       | order_id | user_id | product |
|---------|-------|       |----------|---------|---------|
| 1       | Alice |       | 101      | 1       | Laptop  |
| 2       | Bob   |       | 102      | 1       | Mouse   |
| 3       | Charlie|      | 103      | 2       | Keyboard|
                          | 104      | 4       | Monitor |

JOIN ON users.user_id = orders.user_id

Result:
| user_id | name  | order_id | product  |
|---------|-------|----------|----------|
| 1       | Alice | 101      | Laptop   |
| 1       | Alice | 102      | Mouse    |
| 2       | Bob   | 103      | Keyboard |
```

---

## Types of Joins

### INNER JOIN

**Definition:** Returns only the rows where there is a match in BOTH tables.

**Visual (Venn Diagram):**
```
    A       B
   ┌─┐     ┌─┐
   │ │  ■  │ │  ← Only shaded area (intersection)
   └─┘     └─┘
```

**SQL Example:**
```sql
-- Get all orders with user details (only users who have orders)
SELECT users.name, users.email, orders.product, orders.price
FROM users
INNER JOIN orders ON users.user_id = orders.user_id;
```

**Sample Data:**
```
users:
| user_id | name    | email           |
|---------|---------|-----------------|
| 1       | Alice   | alice@mail.com  |
| 2       | Bob     | bob@mail.com    |
| 3       | Charlie | charlie@mail.com|

orders:
| order_id | user_id | product  | price |
|----------|---------|----------|-------|
| 101      | 1       | Laptop   | 1000  |
| 102      | 1       | Mouse    | 20    |
| 103      | 2       | Keyboard | 50    |
| 104      | 5       | Monitor  | 300   | ← user_id=5 doesn't exist in users
```

**Result:**
```
| name  | email          | product  | price |
|-------|----------------|----------|-------|
| Alice | alice@mail.com | Laptop   | 1000  |
| Alice | alice@mail.com | Mouse    | 20    |
| Bob   | bob@mail.com   | Keyboard | 50    |

Note:
- Charlie (user_id=3) excluded (no orders)
- Monitor order (user_id=5) excluded (user doesn't exist)
```

**When to Use:**
- Get data that exists in both tables
- Most common join type
- Example: "Show me all orders with customer details"

---

### LEFT JOIN (LEFT OUTER JOIN)

**Definition:** Returns ALL rows from the LEFT table, and matching rows from the RIGHT table. If no match, NULL for right table columns.

**Visual (Venn Diagram):**
```
    A       B
   ┌─┐     ┌─┐
   │■│  ■  │ │  ← Left circle fully shaded + intersection
   └─┘     └─┘
```

**SQL Example:**
```sql
-- Get all users and their orders (include users with no orders)
SELECT users.name, users.email, orders.product, orders.price
FROM users
LEFT JOIN orders ON users.user_id = orders.user_id;
```

**Result:**
```
| name    | email            | product  | price |
|---------|------------------|----------|-------|
| Alice   | alice@mail.com   | Laptop   | 1000  |
| Alice   | alice@mail.com   | Mouse    | 20    |
| Bob     | bob@mail.com     | Keyboard | 50    |
| Charlie | charlie@mail.com | NULL     | NULL  | ← No orders, but still included
```

**Key Point:** ALL users shown, even Charlie who has no orders.

**When to Use:**
- Show all records from left table, even if no match
- Example: "Show all users, including those who haven't placed orders"
- Example: "Find users who have NOT placed any orders" (WHERE orders.order_id IS NULL)

**Find Users Without Orders:**
```sql
SELECT users.name, users.email
FROM users
LEFT JOIN orders ON users.user_id = orders.user_id
WHERE orders.order_id IS NULL;

Result:
| name    | email            |
|---------|------------------|
| Charlie | charlie@mail.com |
```

---

### RIGHT JOIN (RIGHT OUTER JOIN)

**Definition:** Returns ALL rows from the RIGHT table, and matching rows from the LEFT table. If no match, NULL for left table columns.

**Visual (Venn Diagram):**
```
    A       B
   ┌─┐     ┌─┐
   │ │  ■  │■│  ← Right circle fully shaded + intersection
   └─┘     └─┘
```

**SQL Example:**
```sql
-- Get all orders and their user details (include orders with no matching user)
SELECT users.name, users.email, orders.product, orders.price
FROM users
RIGHT JOIN orders ON users.user_id = orders.user_id;
```

**Result:**
```
| name  | email          | product  | price |
|-------|----------------|----------|-------|
| Alice | alice@mail.com | Laptop   | 1000  |
| Alice | alice@mail.com | Mouse    | 20    |
| Bob   | bob@mail.com   | Keyboard | 50    |
| NULL  | NULL           | Monitor  | 300   | ← Order exists but user doesn't
```

**Key Point:** ALL orders shown, even Monitor order with non-existent user_id=5.

**When to Use:**
- Less common than LEFT JOIN
- Example: "Show all orders, including orphaned orders"
- Note: `A RIGHT JOIN B` is same as `B LEFT JOIN A`

---

### FULL OUTER JOIN

**Definition:** Returns ALL rows from BOTH tables. If no match, NULL for missing side.

**Visual (Venn Diagram):**
```
    A       B
   ┌─┐     ┌─┐
   │■│  ■  │■│  ← Both circles fully shaded
   └─┘     └─┘
```

**SQL Example:**
```sql
-- Get all users and all orders (show everything)
SELECT users.name, users.email, orders.product, orders.price
FROM users
FULL OUTER JOIN orders ON users.user_id = orders.user_id;
```

**Result:**
```
| name    | email            | product  | price |
|---------|------------------|----------|-------|
| Alice   | alice@mail.com   | Laptop   | 1000  |
| Alice   | alice@mail.com   | Mouse    | 20    |
| Bob     | bob@mail.com     | Keyboard | 50    |
| Charlie | charlie@mail.com | NULL     | NULL  | ← User with no orders
| NULL    | NULL             | Monitor  | 300   | ← Order with no user
```

**Key Point:** Shows EVERYTHING - users without orders AND orders without users.

**When to Use:**
- Rare in practice
- Data reconciliation (find mismatches)
- Example: "Show all users and all orders, highlighting orphaned records"

**Note:** MySQL doesn't support FULL OUTER JOIN directly. Use UNION:
```sql
-- MySQL workaround
SELECT users.name, orders.product
FROM users LEFT JOIN orders ON users.user_id = orders.user_id
UNION
SELECT users.name, orders.product
FROM users RIGHT JOIN orders ON users.user_id = orders.user_id;
```

---

### CROSS JOIN

**Definition:** Returns the **Cartesian product** of two tables (every row from table A combined with every row from table B).

**SQL Example:**
```sql
SELECT users.name, products.product_name
FROM users
CROSS JOIN products;
```

**Sample Data:**
```
users:
| user_id | name  |
|---------|-------|
| 1       | Alice |
| 2       | Bob   |

products:
| product_id | product_name |
|------------|--------------|
| 101        | Laptop       |
| 102        | Mouse        |
```

**Result:**
```
| name  | product_name |
|-------|--------------|
| Alice | Laptop       |
| Alice | Mouse        |
| Bob   | Laptop       |
| Bob   | Mouse        |

Total rows: users (2) × products (2) = 4 rows
```

**When to Use:**
- Generate all possible combinations
- Example: "Show all possible user-product pairs"
- Rare in real applications (usually too many rows)

**Warning:** Can explode data size!
```
1000 users × 1000 products = 1,000,000 rows!
```

---

### SELF JOIN

**Definition:** Joining a table to itself (useful for hierarchical data).

**SQL Example:**
```sql
-- Find employees and their managers
SELECT e1.name AS employee, e2.name AS manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id;
```

**Sample Data:**
```
employees:
| employee_id | name    | manager_id |
|-------------|---------|------------|
| 1           | Alice   | NULL       | ← CEO (no manager)
| 2           | Bob     | 1          | ← Reports to Alice
| 3           | Charlie | 1          | ← Reports to Alice
| 4           | David   | 2          | ← Reports to Bob
```

**Result:**
```
| employee | manager |
|----------|---------|
| Alice    | NULL    | ← CEO
| Bob      | Alice   |
| Charlie  | Alice   |
| David    | Bob     |
```

**When to Use:**
- Hierarchical data (org charts, categories)
- Comparing rows within same table
- Example: "Find employees earning more than their manager"

---

## How Joins Work Internally

When you execute a JOIN, the database uses one of three methods to physically combine the data. The choice depends on table size, indexes, and available memory.

---

### Nested Loop Join

**How it Works:** Simple nested loop - for each row in table A, scan all rows in table B.

**Algorithm:**
```
For each row in Table A:
    For each row in Table B:
        If A.key == B.key:
            Output combined row
```

**Example:**
```sql
SELECT users.name, orders.product
FROM users
INNER JOIN orders ON users.user_id = orders.user_id;

users (3 rows):
| user_id | name    |
|---------|---------|
| 1       | Alice   |
| 2       | Bob     |
| 3       | Charlie |

orders (4 rows):
| order_id | user_id | product  |
|----------|---------|----------|
| 101      | 1       | Laptop   |
| 102      | 1       | Mouse    |
| 103      | 2       | Keyboard |
| 104      | 5       | Monitor  |

Execution (Nested Loop):
Row 1 (Alice, user_id=1):
  Check order 101 (user_id=1) → Match! Output: Alice, Laptop
  Check order 102 (user_id=1) → Match! Output: Alice, Mouse
  Check order 103 (user_id=2) → No match
  Check order 104 (user_id=5) → No match

Row 2 (Bob, user_id=2):
  Check order 101 (user_id=1) → No match
  Check order 102 (user_id=1) → No match
  Check order 103 (user_id=2) → Match! Output: Bob, Keyboard
  Check order 104 (user_id=5) → No match

Row 3 (Charlie, user_id=3):
  Check order 101 → No match
  Check order 102 → No match
  Check order 103 → No match
  Check order 104 → No match

Total comparisons: 3 users × 4 orders = 12 comparisons
```

**Time Complexity:** O(N × M) where N = rows in table A, M = rows in table B

**Optimization: Index Nested Loop**

If table B has an **index** on the join column, lookups are much faster.
```
For each row in Table A:
    Use index to find matching rows in Table B (O(log M))
    Output combined rows

Time Complexity: O(N × log M)  ← Much better!
```

**Example with Index:**
```
Row 1 (Alice, user_id=1):
  Index lookup for user_id=1 in orders (O(log 4) ≈ 2 comparisons)
  Found: order 101, order 102
  Output: Alice-Laptop, Alice-Mouse

Row 2 (Bob, user_id=2):
  Index lookup for user_id=2 (O(log 4) ≈ 2 comparisons)
  Found: order 103
  Output: Bob-Keyboard

Row 3 (Charlie, user_id=3):
  Index lookup for user_id=3
  Found: Nothing

Total comparisons: 3 users × log(4) ≈ 6 comparisons (vs 12 without index)
```

**When Used:**
- One table is small (outer table)
- Other table has index on join column (inner table)
- Default method for small tables

---

### Hash Join

**How it Works:** Build a hash table from smaller table, then probe with larger table.

**Algorithm:**
```
Phase 1 - Build Hash Table:
For each row in Table A (smaller table):
    Hash(A.key) → Store row in hash bucket

Phase 2 - Probe:
For each row in Table B (larger table):
    Hash(B.key) → Look up hash bucket
    If match found:
        Output combined row
```

**Example:**
```sql
SELECT users.name, orders.product
FROM users
INNER JOIN orders ON users.user_id = orders.user_id;

Phase 1 - Build Hash Table from users (smaller table):
Hash(user_id=1) → Bucket[hash_value_1] → {user_id=1, name=Alice}
Hash(user_id=2) → Bucket[hash_value_2] → {user_id=2, name=Bob}
Hash(user_id=3) → Bucket[hash_value_3] → {user_id=3, name=Charlie}

Hash Table:
Bucket[hash_value_1]: {1, Alice}
Bucket[hash_value_2]: {2, Bob}
Bucket[hash_value_3]: {3, Charlie}

Phase 2 - Probe with orders (larger table):
Order 101 (user_id=1):
  Hash(1) → Bucket[hash_value_1]
  Found: {1, Alice}
  Output: Alice, Laptop

Order 102 (user_id=1):
  Hash(1) → Bucket[hash_value_1]
  Found: {1, Alice}
  Output: Alice, Mouse

Order 103 (user_id=2):
  Hash(2) → Bucket[hash_value_2]
  Found: {2, Bob}
  Output: Bob, Keyboard

Order 104 (user_id=5):
  Hash(5) → Bucket[hash_value_5]
  Not found (no match)

Total operations: 3 (build) + 4 (probe) = 7 operations
```

**Time Complexity:** O(N + M) ← Linear! Very fast!

**Hash Function:**
```
Hash function converts join key to bucket number:

user_id → hash_function() → bucket_number

Example hash function (simple modulo):
hash(user_id) = user_id % 10

user_id=1 → hash(1) = 1 % 10 = 1 → Bucket 1
user_id=2 → hash(2) = 2 % 10 = 2 → Bucket 2
user_id=11 → hash(11) = 11 % 10 = 1 → Bucket 1 (collision!)
```

**Handling Hash Collisions:**
```
If two keys hash to same bucket, store them in a linked list:

Bucket 1: [user_id=1] → [user_id=11] → [user_id=21]
           ↓             ↓              ↓
         Alice         Kevin          Mike

Probe: Hash(user_id=11) → Bucket 1 → Check linked list → Found Kevin
```

**When Used:**
- Both tables are large
- No indexes available
- Sufficient memory to build hash table
- Equality joins only (user_id = user_id)

**Limitations:**
- Requires memory (hash table must fit in RAM)
- Cannot handle range joins (age > 25)
- Not good for inequality joins

---

### Merge Join

**How it Works:** Sort both tables by join key, then merge them (like merging two sorted arrays).

**Algorithm:**
```
Phase 1 - Sort both tables:
Sort Table A by join key
Sort Table B by join key

Phase 2 - Merge:
Pointer_A = first row of A
Pointer_B = first row of B

While not end of either table:
    If A.key == B.key:
        Output combined row
        Advance both pointers
    Else if A.key < B.key:
        Advance Pointer_A
    Else:
        Advance Pointer_B
```

**Example:**
```sql
SELECT users.name, orders.product
FROM users
INNER JOIN orders ON users.user_id = orders.user_id;

Phase 1 - Sort both tables by user_id:

users (sorted):
| user_id | name    |
|---------|---------|
| 1       | Alice   |
| 2       | Bob     |
| 3       | Charlie |

orders (sorted):
| user_id | product  |
|---------|----------|
| 1       | Laptop   |
| 1       | Mouse    |
| 2       | Keyboard |
| 5       | Monitor  |

Phase 2 - Merge:
Pointer_A → user_id=1 (Alice)
Pointer_B → user_id=1 (Laptop)
Match! Output: Alice, Laptop
Advance Pointer_B

Pointer_A → user_id=1 (Alice)
Pointer_B → user_id=1 (Mouse)
Match! Output: Alice, Mouse
Advance Pointer_B

Pointer_A → user_id=1 (Alice)
Pointer_B → user_id=2 (Keyboard)
1 < 2, Advance Pointer_A

Pointer_A → user_id=2 (Bob)
Pointer_B → user_id=2 (Keyboard)
Match! Output: Bob, Keyboard
Advance both

Pointer_A → user_id=3 (Charlie)
Pointer_B → user_id=5 (Monitor)
3 < 5, Advance Pointer_A

End of users table. Done!
```

**Time Complexity:** O(N log N + M log M) for sorting, then O(N + M) for merge

**Total:** O(N log N + M log M) ← Dominated by sorting

**When Used:**
- Both tables already sorted (or have indexes on join columns)
- Large tables where hash join doesn't fit in memory
- Range joins (age BETWEEN 25 AND 35)

**Optimization:**
If tables already sorted (or have clustered index on join column), skip sorting phase:
→ Time Complexity: O(N + M) ← As fast as hash join!

---

## How Database Chooses Join Method

The **query optimizer** analyzes the query and data to choose the best join method.

**Factors Considered:**
1. **Table sizes** (small vs large)
2. **Indexes available** (indexed join columns?)
3. **Memory available** (can hash table fit?)
4. **Data sorted?** (already ordered by join key?)
5. **Join type** (equality, range, inequality)

**Decision Tree:**
```
┌─────────────────────────────────────────────┐
│  Is one table very small (< 1000 rows)?     │
└────────────┬────────────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
     Yes           No
      │             │
      ▼             ▼
Nested Loop   ┌─────────────────────────────────┐
(with index   │  Is join key indexed on both?   │
if available) └────────────┬────────────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                   Yes           No
                    │             │
                    ▼             ▼
              Merge Join    ┌─────────────────────────┐
           (if sorted or    │  Enough memory for      │
            indexed)        │  hash table?            │
                            └────────┬────────────────┘
                                     │
                              ┌──────┴──────┐
                              │             │
                             Yes           No
                              │             │
                              ▼             ▼
                          Hash Join    Nested Loop
                         (fastest!)    (fallback)
```

**Example Query Plans:**
```sql
-- Small table join
EXPLAIN SELECT * FROM users JOIN orders ON users.user_id = orders.user_id;

-- PostgreSQL Output:
Hash Join  (cost=1.08..2.21 rows=4)
  Hash Cond: (orders.user_id = users.user_id)
  ->  Seq Scan on orders  (cost=0.00..1.04 rows=4)
  ->  Hash  (cost=1.03..1.03 rows=3)
        ->  Seq Scan on users  (cost=0.00..1.03 rows=3)

→ Optimizer chose Hash Join (both tables small)
```
```sql
-- Large table with index
EXPLAIN SELECT * FROM large_users JOIN orders ON large_users.user_id = orders.user_id;

-- PostgreSQL Output:
Nested Loop  (cost=0.57..1234.56 rows=10000)
  ->  Seq Scan on orders  (cost=0.00..100.00 rows=10000)
  ->  Index Scan using idx_user_id on large_users  (cost=0.57..1.13 rows=1)
        Index Cond: (user_id = orders.user_id)

→ Optimizer chose Index Nested Loop (index available)
```

**Statistics Matter:**

Database maintains statistics about tables:
- Row count
- Data distribution
- Index availability
- Cardinality (distinct values)

**Update statistics regularly:**
```sql
-- PostgreSQL
ANALYZE users;
ANALYZE orders;

-- MySQL
ANALYZE TABLE users;
ANALYZE TABLE orders;
```

Without up-to-date statistics, optimizer may choose wrong join method!

---

## Join Performance and Optimization

### Best Practices

**1. Index Foreign Keys**
```sql
-- Always index join columns!
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- JOIN will use index (much faster)
SELECT * FROM users JOIN orders ON users.user_id = orders.user_id;
```

**2. Join Order Matters (for multiple joins)**
```sql
-- BAD: Large table first
SELECT *
FROM large_table_1M
JOIN medium_table_100K ON ...
JOIN small_table_100 ON ...;

-- GOOD: Small table first (optimizer usually handles this)
SELECT *
FROM small_table_100
JOIN medium_table_100K ON ...
JOIN large_table_1M ON ...;
```

**3. Filter Before Joining (WHERE before JOIN)**
```sql
-- BAD: Join first, filter later
SELECT *
FROM orders
JOIN users ON orders.user_id = users.user_id
WHERE orders.status = 'completed';

-- GOOD: Filter first (smaller join)
SELECT *
FROM (SELECT * FROM orders WHERE status = 'completed') filtered_orders
JOIN users ON filtered_orders.user_id = users.user_id;

-- Even better: Let optimizer handle it (use WHERE, not subquery)
SELECT *
FROM orders
JOIN users ON orders.user_id = users.user_id
WHERE orders.status = 'completed';
-- Modern optimizers push WHERE condition before join automatically
```

**4. Use Appropriate Join Type**
```sql
-- Don't use LEFT JOIN if you need INNER JOIN
-- LEFT JOIN is slower (must keep unmatched rows)

-- BAD: Using LEFT JOIN when INNER JOIN is sufficient
SELECT *
FROM users
LEFT JOIN orders ON users.user_id = orders.user_id
WHERE orders.order_id IS NOT NULL;  ← This makes it INNER JOIN anyway!

-- GOOD: Use INNER JOIN directly
SELECT *
FROM users
INNER JOIN orders ON users.user_id = orders.user_id;
```

**5. Limit Result Set**
```sql
-- Fetch only needed columns
SELECT users.name, orders.product  ← Specific columns
FROM users JOIN orders ON users.user_id = orders.user_id;

-- Not:
SELECT *  ← Fetches all columns (slower)
FROM users JOIN orders ON users.user_id = orders.user_id;
```

---

## Code Examples - Django ORM

### Models Setup
```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    class Meta:
        db_table = 'users'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['user']),  # Index for JOIN performance
        ]

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'products'
```

---

### INNER JOIN in Django
```python
# SQL:
# SELECT users.name, orders.product, orders.price
# FROM orders
# INNER JOIN users ON orders.user_id = users.user_id;

# Django ORM (Method 1 - select_related):
orders = Order.objects.select_related('user').all()

for order in orders:
    print(f"{order.user.name} ordered {order.product} for ${order.price}")

# Generates single query with JOIN:
# SELECT orders.*, users.name, users.email
# FROM orders INNER JOIN users ON orders.user_id = users.user_id

# Django ORM (Method 2 - values with join):
orders = Order.objects.select_related('user').values(
    'user__name',
    'product',
    'price'
)

for order in orders:
    print(order)
# Output: {'user__name': 'Alice', 'product': 'Laptop', 'price': 1000}
```

---

### LEFT JOIN in Django
```python
# SQL:
# SELECT users.name, orders.product
# FROM users
# LEFT JOIN orders ON users.user_id = orders.user_id;

# Django ORM:
from django.db.models import Count

users_with_orders = User.objects.prefetch_related('order_set').all()

for user in users_with_orders:
    print(f"{user.name}:")
    for order in user.order_set.all():
        print(f"  - {order.product}")
    if not user.order_set.exists():
        print("  - No orders")

# Alternative: Using values with LEFT JOIN
users_orders = User.objects.values(
    'name',
    'email',
    'order__product',
    'order__price'
)

# Note: Django automatically does LEFT JOIN when accessing related fields
# that might not exist
```

**Find Users Without Orders:**
```python
# SQL:
# SELECT users.name
# FROM users
# LEFT JOIN orders ON users.user_id = orders.user_id
# WHERE orders.order_id IS NULL;

# Django ORM:
users_without_orders = User.objects.filter(order__isnull=True)

for user in users_without_orders:
    print(f"{user.name} has no orders")

# Or using Count:
users_without_orders = User.objects.annotate(
    order_count=Count('order')
).filter(order_count=0)
```

---

### Multiple JOINs
```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

# SQL:
# SELECT users.name, orders.product, products.category
# FROM order_items
# JOIN orders ON order_items.order_id = orders.order_id
# JOIN users ON orders.user_id = users.user_id
# JOIN products ON order_items.product_id = products.product_id;

# Django ORM:
order_items = OrderItem.objects.select_related(
    'order__user',  # JOIN orders, then JOIN users
    'product'        # JOIN products
).all()

for item in order_items:
    print(f"{item.order.user.name} ordered {item.quantity}x {item.product.name} ({item.product.category})")

# Single query with 3 JOINs!
```

---

### Optimizing JOINs in Django
```python
# ❌ BAD: N+1 Query Problem
orders = Order.objects.all()
for order in orders:
    print(order.user.name)  # Each iteration hits database!

# 1 query for orders + N queries for users = N+1 queries!

# ✅ GOOD: Use select_related
orders = Order.objects.select_related('user').all()
for order in orders:
    print(order.user.name)  # No additional queries!

# 1 query with JOIN!

# ✅ GOOD: Prefetch for reverse relations
users = User.objects.prefetch_related('order_set').all()
for user in users:
    for order in user.order_set.all():
        print(order.product)

# 2 queries total (1 for users, 1 for all orders)
```

---

### CROSS JOIN in Django
```python
# SQL:
# SELECT users.name, products.name
# FROM users
# CROSS JOIN products;

# Django ORM (not directly supported, use raw SQL):
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT users.name, products.name
        FROM users
        CROSS JOIN products
    """)
    results = cursor.fetchall()
    
for user_name, product_name in results:
    print(f"{user_name} - {product_name}")

# Or simulate with .extra():
# (Not recommended, use raw SQL instead)
```

---

### SELF JOIN in Django
```python
class Employee(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

# SQL:
# SELECT e1.name AS employee, e2.name AS manager
# FROM employees e1
# LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id;

# Django ORM:
employees = Employee.objects.select_related('manager').all()

for emp in employees:
    if emp.manager:
        print(f"{emp.name} reports to {emp.manager.name}")
    else:
        print(f"{emp.name} is a top-level manager")
```

---

## Interview Questions

### Q1: What is the difference between INNER JOIN and LEFT JOIN?

**Answer:**
- **INNER JOIN:** Returns only matching rows from both tables
- **LEFT JOIN:** Returns all rows from left table + matching rows from right table (NULLs for non-matches)

**Example:**
```sql
users (3 rows): Alice, Bob, Charlie
orders (2 rows): Alice-Laptop, Bob-Mouse

INNER JOIN: 2 rows (Alice, Bob)
LEFT JOIN: 3 rows (Alice, Bob, Charlie with NULL order)
```

---

### Q2: Explain how a Hash Join works internally.

**Answer:**
Hash Join has two phases:
1. **Build Phase:** Create hash table from smaller table using join key
2. **Probe Phase:** For each row in larger table, hash join key and look up in hash table

**Time Complexity:** O(N + M) - Linear time

**Example:**
```
Build: Hash(user_id) → {1: Alice, 2: Bob}
Probe: Order(user_id=1) → Hash(1) → Found Alice → Output
```

**Used when:** Both tables large, no indexes, sufficient memory.

---

### Q3: What are the three join algorithms databases use?

**Answer:**
1. **Nested Loop Join**
   - Simple double loop
   - O(N × M) without index, O(N × log M) with index
   - Good for small tables or indexed joins

2. **Hash Join**
   - Build hash table, then probe
   - O(N + M) - Fastest for large tables
   - Requires memory, equality joins only

3. **Merge Join**
   - Sort both tables, then merge
   - O(N log N + M log M) for sort, O(N + M) for merge
   - Good if already sorted or for range joins

---

### Q4: When would you use LEFT JOIN instead of INNER JOIN?

**Answer:**
Use LEFT JOIN when you need **all rows from left table**, even if no match in right table.

**Common use cases:**
1. Find records without matches: "Users who haven't placed orders"
2. Optional relationships: "Employees and their managers (some have no manager)"
3. Reporting: "Show all products, including those with no sales"

**Example:**
```sql
-- Find users without orders
SELECT users.name
FROM users
LEFT JOIN orders ON users.user_id = orders.user_id
WHERE orders.order_id IS NULL;
```

---

### Q5: How does the database decide which join method to use?

**Answer:**
The **query optimizer** considers:
1. **Table sizes** (small tables → Nested Loop)
2. **Indexes** (indexed join columns → Index Nested Loop)
3. **Memory** (enough RAM → Hash Join)
4. **Sorted data** (already sorted → Merge Join)
5. **Statistics** (row count, data distribution)

**Example:**
```
Small table (100 rows) + Large table (1M rows) with index
→ Optimizer chooses Index Nested Loop

Both tables large (1M rows each), no index, enough memory
→ Optimizer chooses Hash Join
```

---

### Q6: What is the N+1 query problem in ORMs?

**Answer:**
**N+1 problem:** Fetching N records, then making 1 query per record to get related data.

**Example (Django):**
```python
# ❌ BAD: N+1 queries
orders = Order.objects.all()  # 1 query
for order in orders:
    print(order.user.name)  # N queries (one per order)

# Total: 1 + N queries

# ✅ GOOD: Use select_related
orders = Order.objects.select_related('user').all()  # 1 query with JOIN
for order in orders:
    print(order.user.name)  # No additional queries

# Total: 1 query
```

---

### Q7: What is a CROSS JOIN and when would you use it?

**Answer:**
**CROSS JOIN** returns Cartesian product (every row from A combined with every row from B).

**Example:**
```
users (3 rows) CROSS JOIN products (2 rows) = 6 rows

Output: All possible user-product combinations
```

**Use cases:**
- Generate all possible combinations
- Rare in practice (usually too many rows)

**Warning:** Result size = N × M (can explode!)

---

### Q8: How do you optimize a slow JOIN query?

**Answer:**
1. **Add indexes on join columns**
```sql
   CREATE INDEX idx_user_id ON orders (user_id);
```

2. **Use appropriate join type** (INNER instead of LEFT if possible)

3. **Filter before joining** (reduce rows early)
```sql
   WHERE status = 'active'  -- Before JOIN
```

4. **Select only needed columns** (not SELECT *)

5. **Update statistics**
```sql
   ANALYZE users;
   ANALYZE orders;
```

6. **Check query plan**
```sql
   EXPLAIN SELECT ...
```

---

### Q9: Can you join on columns with different data types?

**Answer:**
**Yes, but avoid it** - database must convert types (slow, might not use index).

**Example:**
```sql
-- BAD: Type mismatch
SELECT *
FROM users
JOIN orders ON users.user_id = orders.user_id_varchar;
-- user_id is INT, user_id_varchar is VARCHAR
-- Database converts VARCHAR to INT on every row (slow!)

-- GOOD: Same types
SELECT *
FROM users
JOIN orders ON users.user_id = orders.user_id;
-- Both INT (fast, can use index)
```

**Best practice:** Ensure join columns have same data type.

---

### Q10: What is the difference between WHERE and ON in joins?

**Answer:**

**ON:** Specifies join condition (which rows to match)

**WHERE:** Filters final result after join

**Example:**
```sql
-- LEFT JOIN with ON
SELECT users.name, orders.product
FROM users
LEFT JOIN orders ON users.user_id = orders.user_id AND orders.price > 100;

-- Returns all users, but only joins orders with price > 100
-- Users without expensive orders get NULL

-- LEFT JOIN with WHERE
SELECT users.name, orders.product
FROM users
LEFT JOIN orders ON users.user_id = orders.user_id
WHERE orders.price > 100;

-- Returns only users with orders > 100
-- Effectively becomes INNER JOIN (WHERE filters out NULLs)
```

**Rule:** For LEFT/RIGHT joins, put **join conditions in ON**, **filters in WHERE**.

---

### Q11: In Django, what's the difference between select_related and prefetch_related?

**Answer:**

| Feature | select_related | prefetch_related |
|---------|---------------|------------------|
| **Relationship** | Foreign Key, One-to-One | Many-to-Many, Reverse Foreign Key |
| **SQL** | Single query with JOIN | Multiple queries (1 + N) |
| **When to use** | User → Orders (FK) | User → Orders (reverse) |

**Example:**
```python
# select_related (for FK)
orders = Order.objects.select_related('user').all()
# SQL: SELECT * FROM orders JOIN users ...

# prefetch_related (for reverse FK)
users = User.objects.prefetch_related('order_set').all()
# SQL: SELECT * FROM users; SELECT * FROM orders WHERE user_id IN (...)
```

---

### Q12: How do you perform a SELF JOIN?

**Answer:**
Join a table to itself (use aliases to distinguish).

**Example:**
```sql
-- Find employees and their managers
SELECT e1.name AS employee, e2.name AS manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id;

-- e1 and e2 are aliases for same table
```

**Django:**
```python
class Employee(models.Model):
    manager = models.ForeignKey('self', null=True)

employees = Employee.objects.select_related('manager').all()
```

---

### Q13: What happens if you JOIN two large tables without indexes?

**Answer:**
Database likely uses **Hash Join** (if enough memory) or **Nested Loop Join** (fallback).

**Without indexes:**
- Nested Loop: O(N × M) - Very slow!
- Hash Join: O(N + M) - Better, but needs memory

**With indexes:**
- Index Nested Loop: O(N × log M) - Much faster!

**Recommendation:** Always index join columns for large tables.

---

### Q14: In a booking system, which columns should be indexed for efficient joins?

**Answer:**
```python
class Booking(models.Model):
    user = models.ForeignKey(User)  # ✅ Index (foreign key)
    movie = models.ForeignKey(Movie)  # ✅ Index (foreign key)
    seat = models.ForeignKey(Seat)  # ✅ Index (foreign key)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),  # For user's bookings
            models.Index(fields=['movie']),  # For movie's bookings
            models.Index(fields=['seat']),  # For seat availability
        ]

# Django auto-creates indexes on ForeignKey fields
```

**JOIN queries:**
```sql
-- Uses index on user_id
SELECT * FROM bookings JOIN users ON bookings.user_id = users.user_id;

-- Uses index on movie_id
SELECT * FROM bookings JOIN movies ON bookings.movie_id = movies.movie_id;
```

---

### Q15: How do you debug slow JOIN queries?

**Answer:**
1. **Use EXPLAIN to see query plan**
```sql
   EXPLAIN ANALYZE
   SELECT * FROM orders JOIN users ON orders.user_id = users.user_id;
```

2. **Check if indexes are used**
```
   Output shows:
   - Seq Scan (bad - no index used)
   - Index Scan (good - index used)
   - Hash Join (okay - no index, but efficient)
```

3. **Verify indexes exist**
```sql
   -- PostgreSQL
   SELECT * FROM pg_indexes WHERE tablename = 'orders';
```

4. **Update statistics**
```sql
   ANALYZE users;
   ANALYZE orders;
```

5. **Monitor query time**
```python
   # Django
   from django.db import connection
   
   orders = Order.objects.select_related('user').all()
   list(orders)
   
   print(connection.queries[-1]['time'])  # Query execution time
```

---

## Resources

### Official Documentation
- [PostgreSQL JOIN Documentation](https://www.postgresql.org/docs/current/tutorial-join.html)
- [MySQL JOIN Documentation](https://dev.mysql.com/doc/refman/8.0/en/join.html)
- [Django select_related](https://docs.djangoproject.com/en/stable/ref/models/querysets/#select-related)
- [Django prefetch_related](https://docs.djangoproject.com/en/stable/ref/models/querysets/#prefetch-related)

### Articles

- [Understanding Join Algorithms](https://bertwagner.com/posts/visualizing-nested-loops-joins-and-understanding-their-implications/)

---


**Summary Cheatsheet**
```
┌─────────────────────────────────────────────────────┐
│              SQL JOINS QUICK REFERENCE              │
├─────────────────────────────────────────────────────┤
│ INNER JOIN: Only matching rows from both tables     │
│ LEFT JOIN:  All from left + matching from right     │
│ RIGHT JOIN: All from right + matching from left     │
│ FULL OUTER: All from both (union of left + right)   │
│ CROSS JOIN: Cartesian product (A × B)               │
│ SELF JOIN:  Table joined to itself                  │
├─────────────────────────────────────────────────────┤
│ Join Algorithms:                                    │
│  - Nested Loop: O(N×M) or O(N×logM) with index      │
│  - Hash Join:   O(N+M) - Fastest for large tables   │
│  - Merge Join:  O(NlogN+MlogM) - Good if sorted     │
├─────────────────────────────────────────────────────┤
│ Optimization:                                       │
│  ✅ Index foreign keys                             │
│  ✅ Use select_related (Django)                    │
│  ✅ Filter before joining                          │
│  ✅ Select only needed columns                     │
│  ✅ Update statistics (ANALYZE)                    │
└─────────────────────────────────────────────────────┘
```

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** March 2026