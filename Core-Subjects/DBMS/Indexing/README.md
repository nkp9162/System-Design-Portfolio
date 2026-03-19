# Database Indexing - Complete Guide

## Table of Contents
1. [Introduction](#introduction)
2. [What is an Index?](#what-is-an-index)
3. [Types of Indexes](#types-of-indexes)
   - [B-Tree Index](#b-tree-index)
   - [B+ Tree Index](#b-tree-index)
   - [Hash Index](#hash-index)
   - [Bitmap Index](#bitmap-index)
4. [B-Tree vs B+ Tree](#b-tree-vs-b-tree)
5. [Composite Index](#composite-index)
6. [Covering Index](#covering-index)
7. [Clustered vs Non-Clustered Index](#clustered-vs-non-clustered-index)
8. [When to Use Indexes](#when-to-use-indexes)
9. [When Indexes Don't Help](#when-indexes-dont-help)
10. [Index on Different Data Types](#index-on-different-data-types)
11. [Query Optimizer and Index Selection](#query-optimizer-and-index-selection)
12. [Prefix Rules and Index Usage](#prefix-rules-and-index-usage)
13. [Code Examples - Django](#code-examples---django)
14. [Interview Questions](#interview-questions)
15. [Resources](#resources)

---

## Introduction

**Index** is a database structure that improves the speed of data retrieval operations. Think of it like a book's index - instead of reading every page to find a topic, you check the index and jump directly to the page.

**Without Index:**
```sql
SELECT * FROM users WHERE email = 'john@example.com';
-- Database scans ALL rows (Full Table Scan)
-- 1 million rows → Check all 1 million
```

**With Index on email:**
```sql
-- Database uses index (Binary Search)
-- 1 million rows → Check only ~20 rows (log₂ 1M ≈ 20)
-- 50,000x faster!
```

---

## What is an Index?

### Analogy: Phone Book
```
Phone Book WITHOUT Index:
- Names randomly scattered
- To find "John Smith", read EVERY page
- 1000 pages → Check all 1000 pages

Phone Book WITH Index (Alphabetical):
- Names sorted: A, B, C... Z
- To find "John Smith", jump to 'S' section
- 1000 pages → Check only ~10 pages (binary search)
```

### How Index Works

**Table without Index:**
```
users table (unsorted):
| id | name  | email           | age |
|----|-------|-----------------|-----|
| 5  | Alice | alice@mail.com  | 25  |
| 2  | Bob   | bob@mail.com    | 30  |
| 8  | John  | john@mail.com   | 28  |
| 1  | Jane  | jane@mail.com   | 22  |

Query: SELECT * FROM users WHERE email = 'john@mail.com';
Scan: Check row 1 → row 2 → row 3 ✅ Found → row 4 (wasted)
```

**Table with Index on email:**
```
Index (B-Tree on email):
        [ jane@mail.com (id=1) ]
           /                   \
 [ alice@mail.com (id=5) ]    [ john@mail.com (id=8) ]
          \                          /
  [ bob@mail.com (id=2) ]   

Query: SELECT * FROM users WHERE email = 'john@mail.com';
Lookup: Root → Right subtree → Found (id=8)
Fetch: Jump directly to row with id=8
Result: 1 lookup instead of full scan
```

---

## Types of Indexes

### B-Tree Index

**Most Common Index Type** (Default in PostgreSQL, MySQL InnoDB)

**Structure:**
```
B-Tree (Balanced Tree):

                    [50]
                   /    \
              [25]        [75]
             /    \      /    \
         [10] [30] [60] [90]

- Each node stores keys and data pointers
- Keys sorted within each node
- Self-balancing (height remains log N)
```

**How Data is Stored in B-Tree:**
```
B-Tree stores data at ALL nodes (internal + leaf)

Internal Nodes: Store keys + data pointers + child pointers
Leaf Nodes: Store keys + data pointers (no children)

Example:
         [50→Data, 75→Data]  ← Internal node (HAS data pointers)
        /       |         \
    [25→Data] [60→Data] [90→Data]  ← Leaf nodes (also have data pointers)
       ↓         ↓         ↓
     Row25     Row60     Row90  ← Actual table rows on disk

Key Point: Data can be found at ANY level (not just leaves)
```

**Search Operation:**
```
Search for key = 50:
1. Start at root: [50→Data, 75→Data]
2. Found 50 in root itself!
3. Follow data pointer to Row50
4. Done! (Search stops at internal node)

Search for key = 60:
1. Start at root: [50, 75]
2. 60 > 50, 60 < 75 → Go to middle child
3. Found [60→Data] in internal node (not leaf!)
4. Follow pointer to Row60
5. Done!

Time Complexity: O(log N)
```

**Use Cases:**
- Range queries: `WHERE age BETWEEN 25 AND 35`
- Sorting: `ORDER BY created_at`
- Prefix matching: `WHERE name LIKE 'John%'`

---

### B+ Tree Index

**Optimized version of B-Tree** (Used in most modern databases)

**Structure:**
```
B+ Tree:

                    [50]  ← Internal nodes (only keys, no data)
                   /    \
              [25]        [75]
             /    \      /    \
         [10] [25] [50] [75] [90]  ← Leaf nodes (keys + data)
          ↓    ↓    ↓    ↓    ↓
        Data Data Data Data Data

Key Difference:
- Internal nodes: ONLY keys (no data pointers)
- Leaf nodes: Keys + Data pointers
- Leaf nodes linked (doubly linked list)
```

**How Data is Stored in B+ Tree:**
```
Internal Nodes:
[Key1, Key2, Key3, ...]
 ↓     ↓     ↓
Child1 Child2 Child3  ← Only pointers to children, NO data

Leaf Nodes:
[Key1→Data1, Key2→Data2, Key3→Data3, ...]
   ↓          ↓          ↓
 Row1       Row2       Row3  ← Pointers to actual rows

Linked List at Leaf Level:
[10→Data] ↔ [25→Data] ↔ [50→Data] ↔ [75→Data] ↔ [90→Data]
```

**Search Operation:**
```
Search for key = 50:
1. Start at root: [50]
2. 50 ≤ 50 → Go left child
3. Reach leaf node [50→Data]
4. Follow pointer to Row

Range Query (50 to 90):
1. Find 50 in leaf node
2. Traverse linked list: 50 → 75 → 90
3. No need to go back to root!
```

**Use Cases:**
- Range queries (better than B-Tree due to linked leaves)
- Full table scans in sorted order
- Most RDBMS use B+ Tree as default

---

### Hash Index

**Structure:**
```
Hash Index:
email → hash_function → bucket

Example:
'john@mail.com' → hash() → 12345 → Bucket[12345] → Row pointer

Hash Table:
Bucket[0]:    → NULL
Bucket[1]:    → alice@mail.com → Row5
Bucket[2]:    → bob@mail.com → Row2
...
Bucket[12345]: → john@mail.com → Row8
```

**Limitations:**
- ❌ No range queries (`WHERE age > 25` won't work)
- ❌ No sorting (`ORDER BY` won't use index)
- ❌ No prefix matching (`WHERE name LIKE 'John%'` won't work)
- ✅ Only equality: `WHERE email = 'john@mail.com'` (O(1) - instant!)

**Use Cases:**
- Exact match queries only
- In-memory databases (Redis)
- Rarely used in traditional RDBMS

---

### Bitmap Index

**Structure:**
```
Bitmap Index (for low-cardinality columns like gender, status):

Table:
| id | gender |
|----|--------|
| 1  | M      |
| 2  | F      |
| 3  | M      |
| 4  | F      |

Bitmap for 'gender':
M: 1010 (rows 1, 3)
F: 0101 (rows 2, 4)

Query: WHERE gender = 'M'
→ Read bitmap for 'M': 1010
→ Fetch rows 1 and 3
```

**Use Cases:**
- Low-cardinality columns (few distinct values)
- Data warehousing, analytics
- Not common in OLTP databases

---

## B-Tree vs B+ Tree

| Feature | B-Tree | B+ Tree |
|---------|--------|---------|
| **Data Storage** | Internal nodes + Leaf nodes | Only leaf nodes |
| **Internal Nodes** | Store keys + data pointers | Store keys only (no data) |
| **Leaf Nodes** | Store keys + data | Store keys + data + linked list |
| **Leaf Linking** | No linking | Doubly linked list |
| **Range Query** | Must traverse tree multiple times | Traverse linked list once |
| **Space Efficiency** | Less efficient (data in all nodes) | More efficient (data only in leaves) |
| **Height** | Same for both (balanced) | Same for both (balanced) |
| **Use Case** | General purpose | Range queries, scans (Better!) |

**Visual Comparison:**
```
B-Tree:
         [50→Data50]
        /           \
   [25→Data25]    [75→Data75]
   ↓                ↓
  Row25           Row75

Range query (25 to 75):
1. Find 25 → Fetch Row25
2. Go back to root
3. Find 75 → Fetch Row75
(Must traverse tree twice)


B+ Tree:
         [50]  (No data, only key)
        /    \
   [25→Data25] ↔ [50→Data50] ↔ [75→Data75]
    ↓              ↓              ↓
  Row25          Row50          Row75

Range query (25 to 75):
1. Find 25 in leaf
2. Traverse linked list: 25 → 50 → 75
3. Done!
(Single traversal through linked list)
```

**Why B+ Tree is Better for Databases:**
1. **More keys per internal node** (no data, only keys → more fan-out)
2. **Faster range queries** (linked list at leaf level)
3. **Sequential scans faster** (just traverse leaf linked list)
4. **Better caching** (internal nodes smaller, fit in memory)

---

## Composite Index

**Definition:** Index on **multiple columns** together.

### How it Works
```sql
CREATE INDEX idx_name_age ON users (name, age);

Index Structure (B+ Tree):
            ['Alice', 25]
           /              \
    ['Alice', 20]        ['Bob', 30]
         \                  /
    ['Alice', 22]      ['Bob', 28]

Sorted Order:
1. First by name (alphabetical)
2. Then by age (within same name)

Data:
('Alice', 20) → Row1
('Alice', 22) → Row2
('Alice', 25) → Row3
('Bob', 28)   → Row4
('Bob', 30)   → Row5
```

### Prefix Rule (IMPORTANT!)

**Index on (name, age) can be used for:**
```sql
✅ WHERE name = 'Alice'  (Uses index - matches prefix)
✅ WHERE name = 'Alice' AND age = 25  (Uses index - full match)
✅ WHERE name = 'Alice' AND age > 20  (Uses index - prefix + range)

❌ WHERE age = 25  (CANNOT use index - doesn't start with name)
❌ WHERE age = 25 AND name = 'Alice'  (CANNOT use index - wrong order)
```

**Why?**
```
Index sorted by: (name, age)

Query: WHERE age = 25
→ Index organized by name first
→ Age = 25 scattered across different name sections
→ Can't use index efficiently
→ Falls back to full table scan

Index visualization:
('Alice', 20) ← age=20
('Alice', 25) ← age=25 (found one)
('Bob', 30)   ← age=30
('Bob', 25)   ← age=25 (found another, but far apart!)
('Charlie', 25) ← age=25 (found another, even farther!)

Can't traverse index sequentially for age=25
```

**Solution:** Create separate index on age if needed.
```sql
CREATE INDEX idx_age ON users (age);  -- For queries filtering by age alone
```

---

### Column Order Matters
```sql
Index: (name, age)
vs
Index: (age, name)

These are DIFFERENT indexes!

Query: WHERE name = 'Alice' AND age = 25
→ Index (name, age) ✅ Optimal
→ Index (age, name) ✅ Works but less efficient

Query: WHERE age = 25
→ Index (name, age) ❌ Won't use
→ Index (age, name) ✅ Will use
```

**Rule of Thumb for Column Order:**
1. Put columns with **higher selectivity** first (fewer duplicates)
2. Put columns used in **equality** conditions before **range** conditions
```sql
-- GOOD: High selectivity first
CREATE INDEX idx_email_status ON users (email, status);
-- email is unique → High selectivity
-- status has few values ('active', 'inactive') → Low selectivity

-- BAD: Low selectivity first
CREATE INDEX idx_status_email ON users (status, email);
-- Less efficient
```

---

## Covering Index

**Definition:** Index that contains **all columns** needed by a query (no need to access table).

### Example
```sql
Table: users (id, name, email, age, city)

Query:
SELECT name, email FROM users WHERE age = 25;

-- Non-Covering Index
CREATE INDEX idx_age ON users (age);

Execution:
1. Use index to find rows where age=25 → Get row IDs: [1, 5, 9]
2. Access table 3 times (disk lookups) to fetch (name, email)
3. Return results

-- Covering Index
CREATE INDEX idx_age_name_email ON users (age, name, email);

Execution:
1. Use index to find rows where age=25
2. Index already has (name, email) → No table access needed!
3. Return results directly from index

Result: 3 disk lookups saved (faster!)
```

### Benefits
```
Without Covering Index:
Query → Index (find matching rows) → Table (fetch columns) → Result
        ↓                              ↓
    Index Scan                     Disk Lookups (SLOW!)

With Covering Index:
Query → Index (find matching rows + columns) → Result
        ↓
    Index Scan only (FAST!)
```

**Trade-off:**
- ✅ Faster queries (no table access)
- ❌ Larger index size (more columns stored)
- ❌ Slower writes (more data to update in index)

**When to Use:**
- Frequently run queries that need specific columns
- Read-heavy applications
- Columns that rarely change

---

## Clustered vs Non-Clustered Index

### Clustered Index

**Definition:** Index that determines the **physical order** of data in the table.

**Key Points:**
- ✅ **Only ONE per table** (table can be sorted in only one order)
- ✅ Leaf nodes **contain actual data** (not pointers)
- ✅ Faster for range queries (data physically contiguous)

**Structure:**
```
Clustered Index on Primary Key (id):

          [id=50]
         /       \
    [id=25]     [id=75]
       ↓           ↓
 [Actual Row]  [Actual Row]
 (id=25, name=Alice, age=22)

Leaf nodes = Actual table rows
```

**Example:**
```sql
-- PostgreSQL: Primary key automatically gets clustered index
CREATE TABLE users (
    id SERIAL PRIMARY KEY,  -- Clustered index on id
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Data physically stored in order of id:
Disk Page 1: [id=1, id=2, id=3, ...]
Disk Page 2: [id=100, id=101, id=102, ...]

Query: SELECT * FROM users WHERE id BETWEEN 1 AND 100;
→ Read contiguous disk pages (fast!)
```

---

### Non-Clustered Index

**Definition:** Index that is **separate from table data**. Leaf nodes contain **pointers** to table rows.

**Key Points:**
- ✅ **Multiple per table** (many different orderings)
- ✅ Leaf nodes **contain pointers** to actual data (not data itself)
- ❌ Slower than clustered (extra lookup to fetch data)

**Structure:**
```
Non-Clustered Index on email:

          [email=jane@mail.com]
         /                     \
 [email=alice@mail.com]    [email=john@mail.com]
        ↓                          ↓
    Pointer to Row5            Pointer to Row8
        ↓                          ↓
[Actual Row on Disk]        [Actual Row on Disk]

Leaf nodes = Pointers (not actual data)
```

**Example:**
```sql
CREATE INDEX idx_email ON users (email);  -- Non-clustered

Query: SELECT * FROM users WHERE email = 'john@mail.com';

Steps:
1. Traverse index to find 'john@mail.com' → Get pointer (Row ID: 8)
2. Use pointer to locate row on disk
3. Fetch row data from disk
4. Return result

(2 disk accesses: index + table)
```

---

### Comparison

| Feature | Clustered Index | Non-Clustered Index |
|---------|----------------|---------------------|
| **Count per Table** | Only 1 | Multiple (unlimited) |
| **Data Storage** | Leaf nodes = Actual data | Leaf nodes = Pointers to data |
| **Physical Order** | Determines table order | Does not affect table order |
| **Speed** | Faster (no extra lookup) | Slower (index + table lookup) |
| **Range Queries** | Very fast (contiguous data) | Slower (scattered data) |
| **Default** | Primary key (usually) | Any other indexed column |
| **Example** | `PRIMARY KEY (id)` | `INDEX (email)` |

**Visual Summary:**
```
Clustered Index:
Index → Data (same structure)

Non-Clustered Index:
Index → Pointers → Data (separate structures)
```

---

## When to Use Indexes

### Good Candidates for Indexing
```sql
✅ Primary Keys (automatic clustered index)
   CREATE TABLE users (id SERIAL PRIMARY KEY);

✅ Foreign Keys (for JOIN performance)
   CREATE INDEX idx_user_id ON orders (user_id);

✅ Columns in WHERE clauses (frequent filters)
   CREATE INDEX idx_email ON users (email);
   -- Query: WHERE email = 'john@mail.com'

✅ Columns in ORDER BY (sorting)
   CREATE INDEX idx_created_at ON posts (created_at);
   -- Query: ORDER BY created_at DESC

✅ Columns in GROUP BY (aggregations)
   CREATE INDEX idx_category ON products (category);
   -- Query: GROUP BY category

✅ Columns in JOIN conditions
   CREATE INDEX idx_product_id ON order_items (product_id);
   -- Query: JOIN products ON order_items.product_id = products.id
```

### Bad Candidates (Avoid Indexing)
```sql
❌ Small tables (< 1000 rows)
   -- Full table scan faster than index lookup overhead

❌ Columns with low selectivity (few distinct values)
   -- Example: gender (only 'M', 'F')
   -- Index won't help much (still scans ~50% of data)

❌ Columns frequently updated
   -- Every UPDATE must also update index (slow writes)

❌ Columns with large data (TEXT, BLOB)
   -- Index size huge, inefficient

❌ Too many indexes on one table
   -- Slows down INSERT/UPDATE/DELETE
   -- Diminishing returns
```

---

### Over-Engineering: When Indexes Hurt

**Problem:** Too many indexes slow down writes.
```sql
Table: users
Indexes:
1. PRIMARY KEY (id)
2. INDEX (email)
3. INDEX (name)
4. INDEX (created_at)
5. INDEX (updated_at)
6. INDEX (status)
7. INDEX (city)

INSERT INTO users VALUES (...);

Database must:
1. Insert row into table
2. Update index 1 (id)
3. Update index 2 (email)
4. Update index 3 (name)
5. Update index 4 (created_at)
6. Update index 5 (updated_at)
7. Update index 6 (status)
8. Update index 7 (city)

Result: 8x slower writes!
```

**Rule of Thumb:**
- **Read-heavy app:** More indexes okay (optimize reads)
- **Write-heavy app:** Fewer indexes (optimize writes)
- **Balanced app:** Index only frequently queried columns

**Example:**
```python
# Read-heavy (Analytics Dashboard)
# Users rarely add data, mostly query
# → Many indexes okay

# Write-heavy (Real-time Chat)
# Messages inserted constantly, rarely queried by filters
# → Minimal indexes (only essentials like user_id, timestamp)
```

---

## When Indexes Don't Help

### 1. Using Functions on Indexed Column
```sql
-- Index on email
CREATE INDEX idx_email ON users (email);

❌ SELECT * FROM users WHERE LOWER(email) = 'john@mail.com';
-- Function LOWER() applied to column
-- Index cannot be used (index doesn't store LOWER(email))
-- Falls back to full table scan

✅ SELECT * FROM users WHERE email = 'john@mail.com';
-- Direct column comparison
-- Index used!

-- Solution: Functional Index
CREATE INDEX idx_email_lower ON users (LOWER(email));
-- Now first query can use this index
```

---

### 2. Leading Wildcards in LIKE
```sql
-- Index on name
CREATE INDEX idx_name ON users (name);

❌ SELECT * FROM users WHERE name LIKE '%John%';
-- Leading wildcard (%) → Index can't be used
-- Full table scan

❌ SELECT * FROM users WHERE name LIKE '%John';
-- Ending search → Index can't be used

✅ SELECT * FROM users WHERE name LIKE 'John%';
-- Prefix search → Index used!
-- Index can efficiently find all names starting with 'John'
```

**Why?**
```
Index stores: Alice, Bob, Charlie, John, Johnny, ...
                                   ↑
Query: LIKE 'John%' → Start here, scan forward ✅

Query: LIKE '%John%' → Must check Alice, Bob, Charlie, ... (all rows) ❌
```

---

### 3. OR Conditions on Different Columns
```sql
-- Indexes on email and name
CREATE INDEX idx_email ON users (email);
CREATE INDEX idx_name ON users (name);

❌ SELECT * FROM users WHERE email = 'john@mail.com' OR name = 'Alice';
-- Must scan both indexes, then merge results
-- Often slower than full table scan!

✅ SELECT * FROM users WHERE email = 'john@mail.com'
   UNION
   SELECT * FROM users WHERE name = 'Alice';
-- Optimizer can use indexes separately, then combine
```

---

### 4. Small Tables
```sql
Table: countries (195 rows)

CREATE INDEX idx_name ON countries (name);

SELECT * FROM countries WHERE name = 'India';

-- Index overhead:
1. Read index B-Tree (disk I/O)
2. Find 'India' in index
3. Follow pointer to table row
4. Read table row (disk I/O)

-- Full table scan:
1. Read all 195 rows (sequential scan, very fast)

Result: Full table scan FASTER than index!
```

**Threshold:** Tables < 1000-10000 rows often don't benefit from indexes.

---

### 5. Type Mismatch
```sql
-- Index on id (integer)
CREATE INDEX idx_id ON users (id);

❌ SELECT * FROM users WHERE id = '123';  -- String '123'
-- Type mismatch → Index might not be used (depends on database)
-- Database may need to convert types

✅ SELECT * FROM users WHERE id = 123;  -- Integer 123
-- Exact type match → Index used
```

---

### 6. Negative Conditions
```sql
-- Index on status
CREATE INDEX idx_status ON users (status);

❌ SELECT * FROM users WHERE status != 'active';
-- Excludes one value, might match 99% of rows
-- Index less helpful (still scans most rows)

✅ SELECT * FROM users WHERE status = 'active';
-- Positive condition → Index efficient
```

---

## Index on Different Data Types

### Can You Index Any Data Type?

**Short Answer:** Most data types can be indexed, but efficiency varies.

| Data Type | Indexable? | Index Type | Notes |
|-----------|-----------|------------|-------|
| **INTEGER** | ✅ Yes | B-Tree, Hash | Best performance |
| **VARCHAR/TEXT** | ✅ Yes | B-Tree | Slower than integers |
| **DATE/TIMESTAMP** | ✅ Yes | B-Tree | Good for range queries |
| **BOOLEAN** | ⚠️ Yes but inefficient | B-Tree | Low selectivity (2 values) |
| **UUID** | ✅ Yes | B-Tree, Hash | Good for distributed systems |
| **JSON** | ⚠️ Partial | GIN/GiST | Can index specific keys |
| **ARRAY** | ⚠️ Partial | GIN | Can index array elements |
| **TEXT (large)** | ❌ Not recommended | Full-text index | Use full-text search instead |
| **BLOB/Binary** | ❌ No | N/A | Not searchable |

---

### Examples
```sql
-- Integer (Best)
CREATE INDEX idx_id ON users (id);
-- Fastest lookups, smallest index size

-- String (Good)
CREATE INDEX idx_email ON users (email);
-- Slower than integer, larger index size

-- Date/Timestamp (Good)
CREATE INDEX idx_created_at ON posts (created_at);
-- Great for range queries: WHERE created_at > '2024-01-01'

-- Boolean (Bad - Low Selectivity)
CREATE INDEX idx_is_active ON users (is_active);
-- Only 2 values (true/false)
-- Index not helpful (scans ~50% of rows anyway)

-- UUID (Good)
CREATE INDEX idx_uuid ON sessions (session_id);
-- Unique, good distribution

-- JSON (Partial - PostgreSQL GIN Index)
CREATE INDEX idx_metadata ON products USING GIN (metadata);
-- Query: WHERE metadata @> '{"color": "red"}'
-- Can index specific JSON keys

-- Large Text (Use Full-Text Search Instead)
CREATE INDEX idx_description_fts ON articles 
USING GIN (to_tsvector('english', description));
-- Full-text search index (not regular B-Tree)

```

---

### Best Practices
```sql
✅ Index integers, UUIDs, dates (high performance)
✅ Index strings for exact matches or prefixes
⚠️  Avoid indexing low-selectivity columns (boolean, enum with few values)
❌ Don't index large text fields (use full-text search)
❌ Don't index binary data (BLOB, images)
```

---

## Query Optimizer and Index Selection

### How Query Optimizer Works

**Database Query Optimizer** decides whether to use an index or do a full table scan.

**Process:**
```
1. Parse query
2. Identify available indexes
3. Estimate cost of each execution plan:
   - Option A: Use index X
   - Option B: Use index Y
   - Option C: Full table scan
4. Choose lowest-cost plan
5. Execute
```

**Cost Estimation Factors:**
```
- Table size (row count)
- Index selectivity (how many rows match)
- Disk I/O cost (random vs sequential)
- Memory available (can index fit in cache?)
- Statistics (distribution of data)
```

---

### Example: Optimizer Choosing Between Index and Full Scan
```sql
Table: users (1 million rows)
Index: idx_status ON users (status)

Query: SELECT * FROM users WHERE status = 'active';

Scenario 1: 95% of users are 'active'
→ Index would return 950,000 rows
→ Optimizer: "Index not helpful, too many rows"
→ Decision: Full table scan (faster!)

Scenario 2: 5% of users are 'active'
→ Index would return 50,000 rows
→ Optimizer: "Index very selective"
→ Decision: Use index (faster!)
```

**Explain Plan:**
```sql
EXPLAIN SELECT * FROM users WHERE status = 'active';

-- Output (Scenario 1 - 95% match):
Seq Scan on users  (cost=0.00..18334.00 rows=950000)
-- Full table scan chosen

-- Output (Scenario 2 - 5% match):
Index Scan using idx_status on users  (cost=0.43..2345.67 rows=50000)
-- Index scan chosen
```

---

### Disk Lookup (Random I/O)

**What is Disk Lookup?**

When using non-clustered index, database must:
1. Read index (find row pointer)
2. **Jump to disk location** to fetch actual row (random I/O)

**Problem:** Random I/O is slow on HDDs (disk head must physically move).
```
Index Scan with 1000 matching rows:
1. Read index → 1 disk read (sequential)
2. Fetch row 1 → Random I/O (disk seek)
3. Fetch row 2 → Random I/O (disk seek)
...
1000. Fetch row 1000 → Random I/O (disk seek)

Total: 1000 random disk seeks (SLOW on HDD!)

Full Table Scan:
1. Read all rows sequentially → 1 large sequential read (FAST!)

Result: Full scan FASTER than index when many rows match!
```

**When Full Scan is Faster:**
```
Rule of Thumb:
If query matches > 5-10% of table rows
→ Full table scan faster than index scan

Why?
- Sequential I/O (full scan) >> Random I/O (index lookups)
- Especially true for HDDs (not SSDs)
```

**SSDs Change the Game:**
```
SSDs: No mechanical parts, random I/O almost as fast as sequential
→ Indexes more beneficial even for larger result sets
→ Modern databases optimize for SSDs
```

---

### Statistics and ANALYZE

**Database maintains statistics** about data distribution.
```sql
-- Update statistics (PostgreSQL)
ANALYZE users;

-- Database collects:
- Row count
- Distinct values per column
- Most common values
- Data distribution (histogram)

Optimizer uses these stats to estimate query cost.
```

**Example:**
```sql
-- Before ANALYZE: Optimizer doesn't know data distribution
-- Might choose wrong index

-- After ANALYZE: Optimizer knows:
status = 'active': 95% of rows
status = 'inactive': 5% of rows

-- Now makes better decision:
WHERE status = 'active' → Full scan (95% of data)
WHERE status = 'inactive' → Index scan (5% of data)
```

---

## Prefix Rules and Index Usage

### Composite Index Prefix Rule

**Key Rule:** For composite index `(col1, col2, col3)`, index can be used if query filters on:
- `col1` alone ✅
- `col1, col2` ✅
- `col1, col2, col3` ✅

**But NOT:**
- `col2` alone ❌
- `col3` alone ❌
- `col2, col3` ❌

---

### Examples
```sql
CREATE INDEX idx_name_age_city ON users (name, age, city);

-- ✅ Can use index (matches prefix)
SELECT * FROM users WHERE name = 'Alice';

SELECT * FROM users WHERE name = 'Alice' AND age = 25;

SELECT * FROM users WHERE name = 'Alice' AND age = 25 AND city = 'NYC';

SELECT * FROM users WHERE name = 'Alice' AND city = 'NYC';
-- Uses index for name, ignores city (partial use)

-- ❌ Cannot use index (doesn't start with name)
SELECT * FROM users WHERE age = 25;

SELECT * FROM users WHERE city = 'NYC';

SELECT * FROM users WHERE age = 25 AND city = 'NYC';
```

---

### Equality vs Range
```sql
Index: (name, age, city)

-- ✅ Full index usage (all equality)
WHERE name = 'Alice' AND age = 25 AND city = 'NYC'

-- ⚠️ Partial index usage (range stops further index use)
WHERE name = 'Alice' AND age > 25 AND city = 'NYC'
--                         ↑ Range condition
-- Index used for: name = 'Alice' AND age > 25
-- Index NOT used for: city (after range, index can't continue)

-- Solution: Put range columns last
CREATE INDEX idx_name_city_age ON users (name, city, age);
WHERE name = 'Alice' AND city = 'NYC' AND age > 25
-- Now all columns use index efficiently
```

---

### String Prefix Matching
```sql
Index: idx_name ON users (name);

-- ✅ Uses index (prefix match)
WHERE name LIKE 'John%'  -- Starts with 'John'

-- ❌ Cannot use index (no prefix)
WHERE name LIKE '%John'  -- Ends with 'John'
WHERE name LIKE '%John%' -- Contains 'John'

-- Reason:
-- Index stores: Alice, Bob, Charlie, John, Johnny, ...
-- LIKE 'John%' → Jump to 'J', scan forward ✅
-- LIKE '%John' → Must check every entry ❌
```

---

## Code Examples - Django

### Creating Indexes in Django
```python
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)  # Automatic unique index
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            # Simple index
            models.Index(fields=['email'], name='idx_email'),
            
            # Composite index
            models.Index(fields=['name', 'age'], name='idx_name_age'),
            
            # Index with ordering
            models.Index(fields=['-created_at'], name='idx_created_desc'),
        ]
        
        # Unique constraint (creates unique index)
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]
```

---

### Using Indexes in Queries
```python
# ✅ Uses index on email
users = User.objects.filter(email='john@example.com')

# ✅ Uses composite index (name, age)
users = User.objects.filter(name='Alice', age=25)

# ✅ Uses index on created_at (ordering)
recent_users = User.objects.order_by('-created_at')[:10]

# ❌ Cannot use index (function on column)
users = User.objects.filter(email__iexact='JOHN@EXAMPLE.COM')
# Solution: Create functional index (PostgreSQL)

# ❌ Cannot use composite index (doesn't start with name)
users = User.objects.filter(age=25)

# ❌ Leading wildcard (cannot use index)
users = User.objects.filter(name__contains='John')  # LIKE '%John%'
```

---

### Covering Index Example
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    
    class Meta:
        indexes = [
            # Covering index: includes all columns needed by query
            models.Index(
                fields=['category', 'name', 'price'],
                name='idx_category_name_price'
            ),
        ]

# Query that uses covering index
products = Product.objects.filter(category='Electronics').values('name', 'price')

# Database execution:
# 1. Uses index to find category='Electronics'
# 2. Index already has (name, price) → No table access needed!
# 3. Returns data directly from index (fast!)
```

---

### Checking Query Plans
```python
from django.db import connection

# Get query execution plan
users = User.objects.filter(email='john@example.com')

# Execute query
list(users)

# Print SQL and execution plan
print(connection.queries[-1]['sql'])

# Or use Django Debug Toolbar in development
# Shows which indexes are used
```

**Manual EXPLAIN:**
```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        EXPLAIN ANALYZE 
        SELECT * FROM myapp_user WHERE email = 'john@example.com'
    """)
    print(cursor.fetchall())

# Output shows index usage:
# Index Scan using idx_email on myapp_user  (cost=0.42..8.44 rows=1)
```

---

### Composite Index Strategy
```python
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # 'pending', 'completed', 'cancelled'
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        indexes = [
            # Common query: user's pending orders
            models.Index(fields=['user', 'status'], name='idx_user_status'),
            
            # Common query: user's recent orders
            models.Index(fields=['user', '-created_at'], name='idx_user_created'),
            
            # Don't create: (status) alone - low selectivity
            # Don't create: (status, user) - wrong order for common queries
        ]

# ✅ Efficient queries
# Uses idx_user_status
Order.objects.filter(user_id=1, status='pending')

# Uses idx_user_created
Order.objects.filter(user_id=1).order_by('-created_at')

# ❌ Less efficient (no good index)
Order.objects.filter(status='pending')  # Low selectivity, might do full scan
```

---

## Interview Questions

### Q1: What is a database index and why is it needed?

**Answer:**
An index is a data structure that improves query speed by allowing fast lookups. Without an index, the database must scan every row (full table scan). With an index, it can jump directly to matching rows using binary search.

**Example:** Finding "John" in 1M rows: Full scan = 1M checks, Index (B-Tree) = ~20 checks.

---

### Q2: What is the difference between B-Tree and B+ Tree?

**Answer:**

| Feature | B-Tree | B+ Tree |
|---------|--------|---------|
| Data storage | Internal + Leaf nodes | Only leaf nodes |
| Leaf linking | No | Yes (doubly linked) |
| Range queries | Multiple tree traversals | Single linked list traversal |
| Use case | General | Better for databases (range queries) |

**B+ Tree is used by most databases** because range queries are common in SQL.

---

### Q3: What is a composite index? How does the prefix rule work?

**Answer:**
A composite index is an index on multiple columns: `INDEX(col1, col2, col3)`.

**Prefix Rule:** Index can be used if query filters on:
- `col1` ✅
- `col1, col2` ✅
- `col1, col2, col3` ✅

**Cannot be used for:**
- `col2` alone ❌
- `col3` alone ❌

**Example:**
```sql
INDEX(name, age, city)

WHERE name = 'Alice' ✅ Uses index
WHERE age = 25 ❌ Cannot use index
```

---

### Q4: What is a covering index?

**Answer:**
A covering index includes **all columns** needed by a query, so the database doesn't need to access the table.

**Example:**
```sql
Query: SELECT name, email FROM users WHERE age = 25;

Index: (age, name, email)  -- Covering index

Execution:
- Index has age, name, email
- No table access needed
- Faster!
```

---

### Q5: What is the difference between clustered and non-clustered index?

**Answer:**

| Feature | Clustered | Non-Clustered |
|---------|-----------|---------------|
| Count per table | 1 | Multiple |
| Data storage | Leaf nodes = Actual data | Leaf nodes = Pointers |
| Physical order | Determines table order | Separate structure |
| Speed | Faster (no extra lookup) | Slower (index + table) |
| Default | Primary key | Other indexed columns |

**Example:** Primary key = clustered index, Index on email = non-clustered.

---

### Q6: When should you NOT use an index?

**Answer:**
- Small tables (< 1000 rows) - Full scan faster
- Low selectivity columns (gender, boolean) - Index not helpful
- Frequently updated columns - Slows down writes
- Columns with functions: `WHERE LOWER(email) = ...` - Index can't be used
- Leading wildcards: `LIKE '%John'` - Index can't be used

---

### Q7: Why doesn't `WHERE age = 25` use a composite index on `(name, age)`?

**Answer:**
Composite index `(name, age)` is sorted first by `name`, then by `age` within each name.
```
Index structure:
('Alice', 20)
('Alice', 25)
('Bob', 25)
('Charlie', 25)

Query: WHERE age = 25
→ Age values scattered across different names
→ Can't traverse index sequentially
→ Falls back to full table scan
```

**Solution:** Create separate index on `age`.

---

### Q8: What happens when you use `LIKE '%John%'` on an indexed column?

**Answer:**
Index **cannot be used**. Leading wildcard `%` means the database must check every value in the index, which is equivalent to a full table scan.

**Why?**
Index stores: Alice, Bob, Charlie, John, Johnny

- `LIKE 'John%'` → Jump to 'J', scan forward ✅
- `LIKE '%John'` → Must check Alice, Bob, Charlie... ❌

---

### Q9: How does the query optimizer decide whether to use an index?

**Answer:**
The optimizer estimates the **cost** of different execution plans:
1. Use index X
2. Use index Y
3. Full table scan

**Factors:**
- Table size
- Index selectivity (how many rows match)
- Disk I/O cost (random vs sequential)

**If index returns > 5-10% of rows, full scan might be faster** (sequential I/O faster than many random disk lookups).

---

### Q10: What is the difference between `INDEX(name, age)` and `INDEX(age, name)`?

**Answer:**
They are **different indexes** with different uses.
```sql
INDEX(name, age):
- Efficient for: WHERE name = 'Alice'
- Efficient for: WHERE name = 'Alice' AND age = 25
- NOT efficient for: WHERE age = 25

INDEX(age, name):
- Efficient for: WHERE age = 25
- Efficient for: WHERE age = 25 AND name = 'Alice'
- NOT efficient for: WHERE name = 'Alice'
```

**Column order matters!** Put most selective (unique) columns first.

---

### Q11: Can you create an index on a TEXT column?

**Answer:**
**Yes, but not recommended** for large text fields.
```sql
✅ Short VARCHAR (email, name): Good for indexing
⚠️  TEXT (descriptions): Use full-text search index instead
❌ BLOB (images, files): Cannot index
```

**For large text:**
```sql
-- Use full-text search index (PostgreSQL)
CREATE INDEX idx_fts ON articles USING GIN (to_tsvector('english', content));

-- Trigram Index (The "Postgres Special" Solution)
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_trgm_name ON users USING GIST (name gist_trgm_ops);

--to_tsvector convert the words into "Search-Ready" format.
-- its a powerfull funtion of postgresql
```

---

### Q12: What is a disk lookup and why is it expensive?

**Answer:**
**Disk lookup** is when the database must read data from a specific disk location (random I/O).

**With non-clustered index:**
```
1. Read index → Find row pointer
2. Jump to disk location (random I/O) ← EXPENSIVE on HDD
3. Read row data
```

**Problem:** If query matches 1000 rows, that's 1000 random disk seeks (slow on HDD).

**Solution:** If > 5-10% of rows match, full sequential scan faster.

---

### Q13: In a movie booking system, which columns should be indexed?

**Answer:**
```python
class Booking(models.Model):
    user = models.ForeignKey(User)  # ✅ Index (foreign key)
    movie = models.ForeignKey(Movie)  # ✅ Index (foreign key)
    seat = models.ForeignKey(Seat)  # ✅ Index (foreign key)
    booking_time = models.DateTimeField()  # ✅ Index (frequent filter/sort)
    status = models.CharField()  # ❌ Low selectivity (pending/confirmed)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'booking_time']),  # User's bookings
            models.Index(fields=['movie', 'booking_time']),  # Movie's bookings
        ]
```

**Reasoning:**
- Foreign keys: Frequent JOINs
- booking_time: Sorting, range queries
- NOT status: Low selectivity (few values)

---

### Q14: Why does adding many indexes slow down writes?

**Answer:**
Every `INSERT`/`UPDATE`/`DELETE` must update all indexes.

**Example:**
```sql
Table with 5 indexes

INSERT INTO users VALUES (...);

Database must:
1. Insert row into table
2. Update index 1
3. Update index 2
4. Update index 3
5. Update index 4
6. Update index 5

Result: 5x slower writes!
```

**Trade-off:** More indexes = Faster reads, Slower writes.

---

### Q15: How do you check if a query is using an index in Django?

**Answer:**
```python
# Method 1: Django Debug Toolbar (development)
# Shows indexes used visually

# Method 2: EXPLAIN
from django.db import connection

users = User.objects.filter(email='john@example.com')
list(users)  # Execute query

with connection.cursor() as cursor:
    cursor.execute("EXPLAIN SELECT * FROM myapp_user WHERE email = %s", ['john@example.com'])
    print(cursor.fetchall())

# Output:
# Index Scan using idx_email on myapp_user ✅

# Or:
# Seq Scan on myapp_user ❌ (no index used)
```

---

## Resources

### Official Documentation
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [MySQL Indexes](https://dev.mysql.com/doc/refman/8.0/en/mysql-indexes.html)
- [Django Database Indexes](https://docs.djangoproject.com/en/stable/ref/models/indexes/)

### Books
- **Database Internals** by Alex Petrov (Deep dive into B-Trees)


### Articles
- [How Database Indexes Work](https://use-the-index-luke.com/)
- [B-Tree vs B+ Tree](https://www.geeksforgeeks.org/difference-between-b-tree-and-b-tree/)


---

**Summary Cheatsheet**
```
┌─────────────────────────────────────────────────────┐
│            INDEXING QUICK REFERENCE                 │
├─────────────────────────────────────────────────────┤
│ Index Types:                                        │
│  - B-Tree: Default, general purpose                 │
│  - B+ Tree: Better for ranges (used by most DBs)    │
│  - Hash: Equality only, rare                        │
├─────────────────────────────────────────────────────┤
│ Composite Index Prefix Rule:                        │
│  INDEX(col1, col2, col3)                            │
│  ✅ WHERE col1 = ...                                │
│  ✅ WHERE col1 = ... AND col2 = ...                 │
│  ❌ WHERE col2 = ...                                │
├─────────────────────────────────────────────────────┤
│ When Index NOT Used:                                │
│  - Functions: WHERE LOWER(col) = ...                │
│  - Leading wildcards: LIKE '%value'                 │
│  - Type mismatch: WHERE id = '123' (id is int)      │
│  - OR on different columns                          │
├─────────────────────────────────────────────────────┤
│ Good Index Candidates:                              │
│  ✅ Primary keys, foreign keys                      │
│  ✅ WHERE, ORDER BY, GROUP BY columns               │
│  ✅ High selectivity (many distinct values)         │
├─────────────────────────────────────────────────────┤
│ Bad Index Candidates:                               │
│  ❌ Small tables (< 1000 rows)                     │
│  ❌ Low selectivity (gender, boolean)              │
│  ❌ Frequently updated columns                     │
└─────────────────────────────────────────────────────┘
```
---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** March 2026