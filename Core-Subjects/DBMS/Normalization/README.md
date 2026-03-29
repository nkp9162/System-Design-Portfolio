# Database Normalization - Complete Guide

## Table of Contents
1. [Introduction](#introduction)
2. [What is Normalization?](#what-is-normalization)
3. [Why Normalization?](#why-normalization)
4. [Functional Dependency](#functional-dependency)
5. [Normal Forms](#normal-forms)
   - [First Normal Form (1NF)](#first-normal-form-1nf)
   - [Second Normal Form (2NF)](#second-normal-form-2nf)
   - [Third Normal Form (3NF)](#third-normal-form-3nf)
   - [Boyce-Codd Normal Form (BCNF)](#boyce-codd-normal-form-bcnf)
6. [Complete Example - Library System](#complete-example---library-system)
7. [Disadvantages of Normalization](#disadvantages-of-normalization)
8. [Denormalization](#denormalization)
9. [When to Normalize vs Denormalize](#when-to-normalize-vs-denormalize)
10. [Interview Questions](#interview-questions)
11. [Resources](#resources)

---

## Introduction

**Normalization** is the process of organizing database tables to minimize redundancy and dependency. It involves dividing large tables into smaller, related tables and defining relationships between them.

**Goal:** Eliminate data anomalies and ensure data integrity.

---

## What is Normalization?

**Definition:** Normalization is a systematic approach to decomposing tables to eliminate data redundancy and undesirable characteristics like insertion, update, and deletion anomalies.

**Simple Analogy:**
```
Messy Closet (Unnormalized):
- Clothes mixed with books
- Duplicates everywhere
- Hard to find anything

Organized Closet (Normalized):
- Shirts in one drawer
- Pants in another
- Books on shelf
- Easy to find, no duplicates
```

---

## Why Normalization?

### Problems with Unnormalized Data

**Example: Unnormalized Student Enrollment Table**
```
student_enrollments:
| student_id | student_name | student_email    | courses              | instructors          | departments      |
|------------|--------------|------------------|----------------------|----------------------|------------------|
| 1          | Alice        | alice@mail.com   | Math, Physics        | Dr. Smith, Dr. Lee   | Science, Science |
| 2          | Bob          | bob@mail.com     | Math, Chemistry      | Dr. Smith, Dr. Khan  | Science, Science |
| 3          | Alice        | alice@mail.com   | Biology              | Dr. Park             | Science          |
```

**Problems:**

**1. Data Redundancy (Duplication)**
```
Alice's name and email repeated in rows 1 and 3
Dr. Smith appears multiple times
Science department repeated
→ Wastes storage space
```

**2. Update Anomaly**
```
Alice changes email to alice.new@mail.com
Must update MULTIPLE rows (row 1 and 3)
If we miss one → Inconsistent data!
```

**3. Insertion Anomaly**
```
New instructor Dr. Wilson hired (teaches Chemistry)
But no students enrolled yet
Cannot insert instructor data!
→ Incomplete information
```

**4. Deletion Anomaly**
```
Bob graduates, delete his enrollment (row 2)
Dr. Khan's information lost!
→ Unintended data loss
```

**Solution:** Normalization!

---

## Functional Dependency

**Definition:** A functional dependency (FD) is a relationship between two attributes, typically between a primary key and other attributes.

**Notation:** `X → Y` (X determines Y)

**Meaning:** "If we know X, we can uniquely determine Y"

### Understanding Functional Dependency

**Example:**
```
students table:
| student_id | student_name | student_email    | date_of_birth |
|------------|--------------|------------------|---------------|
| 1          | Alice        | alice@mail.com   | 2000-05-15    |
| 2          | Bob          | bob@mail.com     | 1999-08-22    |

Functional Dependencies:
student_id → student_name       (Given ID, we can find name)
student_id → student_email      (Given ID, we can find email)
student_id → date_of_birth      (Given ID, we can find DOB)

student_email → student_id      (Email is unique, determines ID)
student_email → student_name    (Email determines name)
```

**Key Points:**
- Left side (X) is called **determinant**
- Right side (Y) is **dependent** on X
- If X is unique, it determines all other attributes

### How to Identify Functional Dependencies

**Step 1:** Identify the primary key (unique identifier)
```
student_id is primary key
→ student_id → ALL other columns
```

**Step 2:** Look for other unique columns
```
student_email is unique
→ student_email → ALL other columns
```

**Step 3:** Find relationships between non-key attributes
```
Does student_name → student_email? NO (two students can have same name)
Does date_of_birth → student_name? NO (multiple students born on same day)
```

**Types of Functional Dependencies:**

**1. Full Functional Dependency**
```
In table with composite key (student_id, course_id):

(student_id, course_id) → grade  ✅ FULL dependency
- Need BOTH to determine grade

student_id → grade  ❌ NOT full (need course_id too)
```

**2. Partial Functional Dependency**
```
In table with composite key (student_id, course_id):

(student_id, course_id) → student_name

But:
student_id → student_name  ← PARTIAL dependency
- Don't need course_id to find student_name
- Depends on part of key only
```

**3. Transitive Functional Dependency**
```
student_id → department_id
department_id → department_name

Therefore:
student_id → department_name  ← TRANSITIVE dependency
- Indirect dependency through department_id
```

---

## Normal Forms

Each normal form has specific rules. Higher normal forms include rules of lower forms.
```
Unnormalized → 1NF → 2NF → 3NF → BCNF

Each step eliminates specific types of anomalies
```

---

## Complete Example - Library System

We'll use a Library Book Lending system and normalize it from scratch to BCNF.

### Unnormalized Table
```
book_lendings (Unnormalized):

| lending_id | book_titles                    | book_authors                  | member_name | member_email   | member_phone | librarian_name | due_dates                 |
|------------|--------------------------------|-------------------------------|-------------|----------------|--------------|----------------|---------------------------|
| 1          | Clean Code, Design Patterns    | Robert Martin, Gang of Four   | Alice       | alice@mail.com | 555-0001     | John Smith     | 2024-02-01, 2024-02-05    |
| 2          | Clean Code                     | Robert Martin                 | Bob         | bob@mail.com   | 555-0002     | John Smith     | 2024-02-03                |
| 3          | Refactoring                    | Martin Fowler                 | Alice       | alice@mail.com | 555-0001     | Sarah Lee      | 2024-02-10                |
```

**Problems:**
- Multiple values in single cell (book_titles, book_authors, due_dates)
- Repeated data (Alice's info in rows 1 and 3)
- Update anomalies, insertion anomalies, deletion anomalies

---

## First Normal Form (1NF)

**Rules:**
1. Each cell must contain only **atomic (single) values**
2. Each column must contain values of **same data type**
3. Each column must have a **unique name**
4. Order of rows/columns doesn't matter

**Simple:** No repeating groups, no multi-valued attributes.

### Converting to 1NF

**Break down multi-valued cells:**
```
book_lendings (1NF):
| lending_id | book_title       | book_author    | member_name | member_email    | member_phone | librarian_name | due_date    |
|------------|------------------|----------------|-------------|-----------------|--------------|----------------|-------------|
| 1          | Clean Code       | Robert Martin  | Alice       | alice@mail.com  | 555-0001     | John Smith     | 2024-02-01  |
| 1          | Design Patterns  | Gang of Four   | Alice       | alice@mail.com  | 555-0001     | John Smith     | 2024-02-05  |
| 2          | Clean Code       | Robert Martin  | Bob         | bob@mail.com    | 555-0002     | John Smith     | 2024-02-03  |
| 3          | Refactoring      | Martin Fowler  | Alice       | alice@mail.com  | 555-0001     | Sarah Lee      | 2024-02-10  |
```

**Changes:**
- ✅ Each cell now has single value
- ✅ No comma-separated lists
- Row 1 split into two rows (one per book)

**Primary Key:** `(lending_id, book_title)` - Composite key

**Remaining Issues:**
- Alice's info repeated (rows 1, 2, 4)
- Book author depends only on book_title, not lending_id
- Still has redundancy

---

## Second Normal Form (2NF)

**Rules:**
1. Must be in **1NF**
2. No **partial dependencies** (all non-key attributes must depend on ENTIRE primary key, not just part of it)

**Simple:** If composite key exists, every non-key column must depend on the WHOLE key.

### Identifying Partial Dependencies
```
Primary Key: (lending_id, book_title)

Check each non-key attribute:

book_author → Depends on book_title only ❌ PARTIAL DEPENDENCY
  - Don't need lending_id to find author
  
member_name → Depends on lending_id only ❌ PARTIAL DEPENDENCY
  - Don't need book_title to find member name
  
member_email → Depends on lending_id only ❌ PARTIAL DEPENDENCY
member_phone → Depends on lending_id only ❌ PARTIAL DEPENDENCY

librarian_name → Depends on lending_id only ❌ PARTIAL DEPENDENCY

due_date → Depends on BOTH (lending_id, book_title) ✅ FULL DEPENDENCY
  - Need both to find specific book's due date in a lending
```

### Converting to 2NF

**Split table to remove partial dependencies:**
```
books (2NF):
| book_id | book_title       | book_author    |
|---------|------------------|----------------|
| 101     | Clean Code       | Robert Martin  |
| 102     | Design Patterns  | Gang of Four   |
| 103     | Refactoring      | Martin Fowler  |

Primary Key: book_id
FD: book_id → book_title, book_author


members (2NF):
| member_id | member_name | member_email    | member_phone |
|-----------|-------------|-----------------|--------------|
| 201       | Alice       | alice@mail.com  | 555-0001     |
| 202       | Bob         | bob@mail.com    | 555-0002     |

Primary Key: member_id
FD: member_id → member_name, member_email, member_phone


librarians (2NF):
| librarian_id | librarian_name |
|--------------|----------------|
| 301          | John Smith     |
| 302          | Sarah Lee      |

Primary Key: librarian_id
FD: librarian_id → librarian_name


lendings (2NF):
| lending_id | book_id | member_id | librarian_id | due_date    |
|------------|---------|-----------|--------------|-------------|
| 1          | 101     | 201       | 301          | 2024-02-01  |
| 1          | 102     | 201       | 301          | 2024-02-05  |
| 2          | 101     | 202       | 301          | 2024-02-03  |
| 3          | 103     | 201       | 302          | 2024-02-10  |

Primary Key: (lending_id, book_id)
FD: (lending_id, book_id) → member_id, librarian_id, due_date
```

**Changes:**
- ✅ No partial dependencies
- ✅ Data split into logical entities (books, members, librarians, lendings)
- ✅ Less redundancy

**Remaining Issue:**
- Transitive dependencies might exist

---

## Third Normal Form (3NF)

**Rules:**
1. Must be in **2NF**
2. No **transitive dependencies** (non-key attributes should not depend on other non-key attributes)

**Simple:** Non-key columns should depend ONLY on primary key, not on other non-key columns.

### Identifying Transitive Dependencies

Let's add more data to demonstrate:
```
members (before 3NF):
| member_id | member_name | member_email    | member_phone | membership_type | membership_fee |
|-----------|-------------|-----------------|--------------|-----------------|----------------|
| 201       | Alice       | alice@mail.com  | 555-0001     | Premium         | 50             |
| 202       | Bob         | bob@mail.com    | 555-0002     | Basic           | 20             |
| 203       | Charlie     | charlie@mail.com| 555-0003     | Premium         | 50             |

Primary Key: member_id

Functional Dependencies:
member_id → membership_type
membership_type → membership_fee  ← TRANSITIVE DEPENDENCY

Therefore:
member_id → membership_fee (indirect, through membership_type)
```

**Problem:** `membership_fee` depends on `membership_type` (non-key), not directly on `member_id`.

### Converting to 3NF

**Remove transitive dependencies:**
```
membership_types (3NF):
| membership_type | membership_fee | max_books | benefits        |
|-----------------|----------------|-----------|-----------------|
| Basic           | 20             | 3         | Standard access |
| Premium         | 50             | 10        | Priority access |
| VIP             | 100            | 20        | Premium support |

Primary Key: membership_type
FD: membership_type → membership_fee, max_books, benefits


members (3NF):
| member_id | member_name | member_email    | member_phone | membership_type |
|-----------|-------------|-----------------|--------------|-----------------|
| 201       | Alice       | alice@mail.com  | 555-0001     | Premium         |
| 202       | Bob         | bob@mail.com    | 555-0002     | Basic           |
| 203       | Charlie     | charlie@mail.com| 555-0003     | Premium         |

Primary Key: member_id
FD: member_id → member_name, member_email, member_phone, membership_type
Foreign Key: membership_type → membership_types.membership_type
```

**Changes:**
- ✅ No transitive dependencies
- ✅ `membership_fee` moved to separate table
- ✅ Can change fee for all Premium members in one place

---

## Boyce-Codd Normal Form (BCNF)

**Rules:**
1. Must be in **3NF**
2. For every functional dependency `X → Y`, X must be a **superkey** (candidate key)

**Simple:** Every determinant must be a candidate key.

**Note:** BCNF is stricter than 3NF. Most 3NF tables are also in BCNF, but not always.

### When 3NF is NOT BCNF

**Example: Course Instructors**
```
course_instructors (3NF but NOT BCNF):

| student_id | course_id | instructor_name |
|------------|-----------|-----------------|
| 1          | CS101     | Dr. Smith       |
| 1          | CS102     | Dr. Lee         |
| 2          | CS101     | Dr. Smith       |
| 2          | CS102     | Dr. Khan        |

Primary Key: (student_id, course_id)

Functional Dependencies:
(student_id, course_id) → instructor_name  ✅
instructor_name → course_id  ← Problem!
  - Dr. Smith teaches only CS101
  - Dr. Lee teaches only CS102
  - Dr. Khan teaches only CS102

instructor_name is NOT a superkey, but determines course_id
→ Violates BCNF!
```

**Problem:**
```
Update Anomaly:
- Dr. Smith now teaches CS103
- Must update ALL rows where Dr. Smith appears
- If instructor_name determines course_id, it should be a key!
```

### Converting to BCNF

**Split based on functional dependencies:**
```
instructors (BCNF):
| instructor_id | instructor_name | course_id |
|---------------|-----------------|-----------|
| 501           | Dr. Smith       | CS101     |
| 502           | Dr. Lee         | CS102     |
| 503           | Dr. Khan        | CS102     |

Primary Key: instructor_id
FD: instructor_id → instructor_name, course_id
Also: instructor_name → course_id (now instructor_name is part of candidate key)


enrollments (BCNF):
| student_id | instructor_id |
|------------|---------------|
| 1          | 501           |
| 1          | 502           |
| 2          | 501           |
| 2          | 503           |

Primary Key: (student_id, instructor_id)
FD: (student_id, instructor_id) → (nothing, join table)
```

**Changes:**
- ✅ Every determinant is now a superkey
- ✅ No update anomalies
- ✅ Instructor-course relationship managed separately

---

## Summary - Normalization Progression

### Complete Library System (BCNF)

**Final Schema:**
```sql
-- Books
CREATE TABLE books (
    book_id INT PRIMARY KEY,
    book_title VARCHAR(200),
    book_author VARCHAR(100),
    isbn VARCHAR(20),
    publication_year INT
);

-- Membership Types
CREATE TABLE membership_types (
    membership_type VARCHAR(20) PRIMARY KEY,
    membership_fee DECIMAL(10,2),
    max_books INT,
    benefits TEXT
);

-- Members
CREATE TABLE members (
    member_id INT PRIMARY KEY,
    member_name VARCHAR(100),
    member_email VARCHAR(100) UNIQUE,
    member_phone VARCHAR(15),
    membership_type VARCHAR(20),
    FOREIGN KEY (membership_type) REFERENCES membership_types(membership_type)
);

-- Librarians
CREATE TABLE librarians (
    librarian_id INT PRIMARY KEY,
    librarian_name VARCHAR(100),
    librarian_email VARCHAR(100) UNIQUE
);

-- Lendings
CREATE TABLE lendings (
    lending_id INT,
    book_id INT,
    member_id INT,
    librarian_id INT,
    checkout_date DATE,
    due_date DATE,
    return_date DATE,
    PRIMARY KEY (lending_id, book_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (librarian_id) REFERENCES librarians(librarian_id)
);
```

**Benefits:**
- ✅ No redundancy
- ✅ No update/insertion/deletion anomalies
- ✅ Data integrity maintained
- ✅ Flexible and scalable

---

## Disadvantages of Normalization

While normalization solves many problems, it has trade-offs:

### 1. Increased Number of Tables
```
Unnormalized: 1 table
Normalized: 5+ tables

More tables = More complex queries
```

### 2. Complex Queries (Multiple JOINs)

**Example: Get all lendings with full details**
```sql
-- Unnormalized (Simple):
SELECT * FROM book_lendings WHERE member_name = 'Alice';

-- Normalized (Complex):
SELECT 
    l.lending_id,
    b.book_title,
    b.book_author,
    m.member_name,
    m.member_email,
    lib.librarian_name,
    l.due_date
FROM lendings l
JOIN books b ON l.book_id = b.book_id
JOIN members m ON l.member_id = m.member_id
JOIN librarians lib ON l.librarian_id = lib.librarian_id
WHERE m.member_name = 'Alice';

→ 4 JOINs vs 0 JOINs!
```

### 3. Slower Query Performance
```
Multiple JOINs = More disk I/O
Especially slow for:
- Large tables
- No proper indexes
- Complex aggregations
```

**Example:**
```sql
-- Report: Books borrowed per member type
SELECT 
    mt.membership_type,
    COUNT(*) as total_books
FROM lendings l
JOIN members m ON l.member_id = m.member_id
JOIN membership_types mt ON m.membership_type = mt.membership_type
GROUP BY mt.membership_type;

→ 3 JOINs for simple report
→ Slower than denormalized table
```

### 4. Difficult for Analytics/Reporting
```
Business Intelligence queries often need:
- Aggregations across many tables
- Historical data analysis
- Complex calculations

Normalized schema = Many JOINs = Slow BI queries
```

### 5. More Storage for Keys
```
Foreign keys in every table:
- member_id in lendings
- book_id in lendings
- librarian_id in lendings

→ Additional storage overhead
```

### 6. Application Complexity
```python
# Django ORM - Normalized (Complex):
lendings = Lending.objects.select_related(
    'book',
    'member',
    'librarian'
).all()

for lending in lendings:
    print(lending.book.title)  # Multiple joins
    print(lending.member.name)
    print(lending.librarian.name)

# Unnormalized (Simple):
lendings = BookLending.objects.all()
for lending in lendings:
    print(lending.book_title)  # Direct access
    print(lending.member_name)
    print(lending.librarian_name)
```

---

## Denormalization

**Definition:** Intentionally introducing redundancy by combining tables or adding redundant data to improve read performance.

**When to Denormalize:**
- Read-heavy applications (analytics, reporting)
- Performance-critical queries
- Avoid complex JOINs
- Reduce query latency

### Denormalization Techniques

#### 1. Adding Redundant Columns
```sql
-- Normalized:
lendings: (lending_id, book_id, member_id, ...)
books: (book_id, book_title, ...)

-- Denormalized:
lendings: (lending_id, book_id, book_title, member_id, ...)
         ↑                      ↑
         Foreign key         Redundant column (copied from books)

Benefit: No JOIN needed to get book_title
Cost: Must update book_title in lendings when changed in books
```

**Example:**
```sql
-- Before denormalization:
SELECT l.lending_id, b.book_title
FROM lendings l
JOIN books b ON l.book_id = b.book_id;

-- After denormalization:
SELECT lending_id, book_title
FROM lendings;

→ No JOIN needed!
```

#### 2. Materialized Views (Pre-computed JOINs)
```sql
-- Create materialized view (PostgreSQL):
CREATE MATERIALIZED VIEW lending_details AS
SELECT 
    l.lending_id,
    b.book_title,
    b.book_author,
    m.member_name,
    m.member_email,
    lib.librarian_name,
    l.due_date
FROM lendings l
JOIN books b ON l.book_id = b.book_id
JOIN members m ON l.member_id = m.member_id
JOIN librarians lib ON l.librarian_id = lib.librarian_id;

-- Query materialized view (fast!):
SELECT * FROM lending_details WHERE member_name = 'Alice';

-- Refresh periodically:
REFRESH MATERIALIZED VIEW lending_details;
```

**Benefits:**
- ✅ Fast queries (no JOINs at query time)
- ✅ Complex calculations pre-computed
- ✅ Original normalized tables unchanged

**Costs:**
- ❌ Stale data (must refresh periodically)
- ❌ Extra storage
- ❌ Refresh overhead

#### 3. Summary Tables (Aggregated Data)
```sql
-- Normalized: Calculate on every query
SELECT membership_type, COUNT(*) 
FROM members 
GROUP BY membership_type;

-- Denormalized: Pre-computed summary table
CREATE TABLE membership_stats (
    membership_type VARCHAR(20),
    member_count INT,
    last_updated TIMESTAMP
);

-- Update periodically (trigger or cron job):
INSERT INTO membership_stats
SELECT membership_type, COUNT(*), NOW()
FROM members
GROUP BY membership_type;

-- Query summary (instant!):
SELECT * FROM membership_stats;
```

#### 4. Combining Tables
```sql
-- Normalized: Separate tables
members: (member_id, name, email, membership_type)
membership_types: (membership_type, fee, max_books)

-- Denormalized: Combined table
members: (member_id, name, email, membership_type, membership_fee, max_books)
         ↑                                          ↑               ↑
         Primary data                           Redundant data from membership_types

Benefit: Single table query
Cost: Update anomaly (change fee, update all members)
```

---

## When to Normalize vs Denormalize

### Use Normalization When:
```
✅ Transactional systems (OLTP)
  - E-commerce orders
  - Banking transactions
  - Booking systems
  
✅ Data integrity critical
  - No redundancy allowed
  - Frequent updates
  
✅ Write-heavy applications
  - Inserts, updates, deletes common
  
Example: Movie ticket booking (seat availability must be accurate)
```

### Use Denormalization When:
```
✅ Analytics/Reporting (OLAP)
  - Business intelligence dashboards
  - Data warehouses
  
✅ Read-heavy applications
  - Social media feeds
  - News websites
  - Product catalogs
  
✅ Performance critical
  - High-traffic queries
  - Real-time dashboards
  
Example: Netflix recommendations (can tolerate slightly stale data)
```

### Hybrid Approach (Most Common in Production)
```
Strategy: Normalize transactional data, denormalize for reporting

1. OLTP Database (Normalized):
   - Handle live transactions
   - Maintain data integrity
   
2. OLAP Database (Denormalized):
   - Copy data periodically (ETL)
   - Pre-compute aggregations
   - Optimize for reporting
   
Example:
- Amazon orders: Normalized (transactions)
- Amazon analytics: Denormalized (sales reports)
```

**Real-World Example:**
```python
# Django Models (Normalized for OLTP)
class Order(models.Model):
    user = models.ForeignKey(User)
    total_amount = models.DecimalField()
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()

# Denormalized for Reporting (nightly job)
class DailySalesReport(models.Model):
    date = models.DateField()
    total_orders = models.IntegerField()
    total_revenue = models.DecimalField()
    top_product = models.CharField()
    # Pre-computed, read-only
```

---

## Interview Questions

### Q1: What is the difference between 2NF and 3NF?

**Answer:**
- **2NF:** No partial dependencies (all non-key attributes depend on entire primary key)
- **3NF:** No transitive dependencies (non-key attributes depend only on primary key, not on other non-key attributes)

**Example:**
```
Table: (student_id, course_id, student_name, instructor_name)
Primary Key: (student_id, course_id)

2NF violation:
student_id → student_name (partial dependency, doesn't need course_id)

3NF violation:
student_id → department_id → department_name (transitive dependency)
```

---

### Q2: A table has columns: employee_id, project_id, employee_name, project_name, hours_worked. What normal form violations exist?

**Answer:**
**Primary Key:** `(employee_id, project_id)`

**Violations:**
1. **2NF Violation (Partial Dependency):**
   - `employee_id → employee_name` (doesn't need project_id)
   - `project_id → project_name` (doesn't need employee_id)

**Solution:**
```sql
employees: (employee_id, employee_name)
projects: (project_id, project_name)
assignments: (employee_id, project_id, hours_worked)
```

---

### Q3: Explain the difference between 3NF and BCNF with an example.

**Answer:**
**3NF:** No transitive dependencies
**BCNF:** Every determinant must be a superkey (stricter)

**Example where 3NF ≠ BCNF:**
```
course_schedule: (student_id, time_slot, room, instructor)
Primary Key: (student_id, time_slot)

Functional Dependencies:
(student_id, time_slot) → room, instructor  ✅ 3NF
room → instructor (room determines instructor, but room is not a superkey)  ❌ BCNF

Problem: Changing instructor for a room requires updating multiple rows
```

**BCNF Solution:**
```
rooms: (room, instructor)
schedules: (student_id, time_slot, room)
```

---

### Q4: What are the trade-offs of normalization?

**Answer:**

| Pros | Cons |
|------|------|
| ✅ No redundancy | ❌ More tables (complexity) |
| ✅ Data consistency | ❌ Multiple JOINs (slower reads) |
| ✅ Easy updates | ❌ Complex queries |
| ✅ Storage efficiency | ❌ Application complexity |

**When to normalize:** Transactional systems (OLTP), write-heavy apps
**When to denormalize:** Analytics (OLAP), read-heavy apps

---

### Q5: When would you denormalize a database?

**Answer:**
Denormalize when **read performance** is more important than **data consistency**.

**Use cases:**
1. **Analytics/Reporting:** Pre-compute aggregations (dashboards)
2. **Caching:** Redundant columns to avoid JOINs (social media feeds)
3. **Historical data:** Archive old data in denormalized format
4. **Read-heavy apps:** Product catalogs, news sites

**Example:**
```sql
-- Normalized: JOIN every time
SELECT products.name, categories.category_name
FROM products JOIN categories ON products.category_id = categories.category_id;

-- Denormalized: Add category_name to products (no JOIN)
SELECT name, category_name FROM products;
```

---

### Q6: How do you identify functional dependencies in a table?

**Answer:**
**Steps:**
1. **Identify primary key** (unique identifier)
   - Primary key → All other columns

2. **Find other unique columns** (candidate keys)
   - Each unique column → All columns it determines

3. **Check non-key relationships**
   - Does column A determine column B? (A → B)
   - Test: If two rows have same A, must they have same B?

**Example:**
```
Table: (order_id, customer_id, customer_name, customer_email)

order_id → customer_id (primary key)
customer_id → customer_name, customer_email
customer_email → customer_id, customer_name (email is unique)

Transitive: order_id → customer_id → customer_name
```

---

### Q7: In a movie booking system, you have a table with booking_id, user_id, user_name, user_email, movie_id, movie_title, seat_number, booking_date. Normalize to 3NF.

**Answer:**

**Unnormalized:**
```
bookings: (booking_id, user_id, user_name, user_email, movie_id, movie_title, seat_number, booking_date)
```

**Functional Dependencies:**
- `booking_id → user_id, movie_id, seat_number, booking_date`
- `user_id → user_name, user_email` (partial)
- `movie_id → movie_title` (partial)

**1NF:** Already satisfied (atomic values)

**2NF:** Remove partial dependencies
```sql
users: (user_id, user_name, user_email)
movies: (movie_id, movie_title)
bookings: (booking_id, user_id, movie_id, seat_number, booking_date)
```

**3NF:** Check transitive dependencies
- No transitive dependencies exist
- Already in 3NF ✅

**Final Schema:**
```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(100),
    user_email VARCHAR(100) UNIQUE
);

CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    movie_title VARCHAR(200),
    duration INT,
    genre VARCHAR(50)
);

CREATE TABLE bookings (
    booking_id INT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    seat_number VARCHAR(10),
    booking_date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);
```

---

### Q8: What is a materialized view and when would you use it?

**Answer:**
**Materialized View:** Pre-computed query result stored as a table (denormalization technique).

**vs Regular View:**
- Regular view: Query executed every time (virtual table)
- Materialized view: Result stored, refreshed periodically (physical table)

**When to use:**
- Complex JOIN queries executed frequently
- Aggregations (SUM, COUNT, AVG) on large tables
- Reporting dashboards (slight staleness acceptable)

**Example:**
```sql
-- Expensive query (multiple JOINs):
SELECT 
    m.membership_type,
    COUNT(*) as total_members,
    SUM(l.total_amount) as total_revenue
FROM members m
JOIN lendings l ON m.member_id = l.member_id
GROUP BY m.membership_type;

-- Create materialized view:
CREATE MATERIALIZED VIEW membership_revenue AS
SELECT /* query above */;

-- Query materialized view (instant!):
SELECT * FROM membership_revenue;

-- Refresh daily:
REFRESH MATERIALIZED VIEW membership_revenue;
```

---

### Q9: Can a table be in 3NF but not in BCNF? Give an example.

**Answer:**
**Yes**, when a non-superkey determinant exists.

**Example:**
```
student_advisor: (student_id, advisor_id, advisor_name, department)
Primary Key: (student_id)

Assumptions:
- One student has one advisor
- One advisor works in one department
- Advisor name is unique

Functional Dependencies:
student_id → advisor_id, advisor_name, department
advisor_name → department (advisor_name is not a superkey!)

3NF: ✅ (no transitive dependency via non-key attributes)
BCNF: ❌ (advisor_name determines department, but advisor_name is not a superkey)
```

**BCNF Solution:**
```sql
advisors: (advisor_id, advisor_name, department)
students: (student_id, advisor_id)
```

---

### Q10: How does denormalization improve performance? What are the risks?

**Answer:**

**Performance Benefits:**
1. **Fewer JOINs:** Direct column access (faster)
2. **Pre-computed aggregations:** No GROUP BY at query time
3. **Reduced disk I/O:** Single table scan vs multiple

**Risks:**
1. **Data inconsistency:** Redundant data can diverge
2. **Update anomalies:** Must update multiple places
3. **Storage overhead:** Duplicate data
4. **Complex write logic:** Application must maintain redundancy

**Example:**
```sql
-- Normalized: JOIN on every query
SELECT orders.total, customers.name
FROM orders JOIN customers ON orders.customer_id = customers.customer_id;

-- Denormalized: Add customer_name to orders (no JOIN)
orders: (order_id, customer_id, customer_name, total)
                                 ↑ Redundant

Query: SELECT total, customer_name FROM orders;  ← Fast!

Risk: Customer changes name → Update orders table too (consistency)
```

**Mitigation:**
- Triggers to sync redundant data
- Application-level validation
- Periodic data reconciliation

---

## Resources

### Official Documentation
- [Database Normalization - Wikipedia](https://en.wikipedia.org/wiki/Database_normalization)
- [PostgreSQL Table Design Best Practices](https://www.postgresql.org/docs/current/ddl.html)

### Books
- **Database System Concepts** by Silberschatz (Chapter on Normalization)
- **Fundamentals of Database Systems** by Elmasri & Navathe

### Articles
- [Normalization in DBMS - GeeksforGeeks](https://www.geeksforgeeks.org/normal-forms-in-dbms/)


---

**Summary Cheatsheet**
```
┌─────────────────────────────────────────────────────┐
│         NORMALIZATION QUICK REFERENCE               │
├─────────────────────────────────────────────────────┤
│ 1NF: Atomic values (no repeating groups)            │
│ 2NF: 1NF + No partial dependencies                  │
│ 3NF: 2NF + No transitive dependencies               │
│ BCNF: 3NF + Every determinant is a superkey         │
├─────────────────────────────────────────────────────┤
│ Functional Dependency (FD):                         │
│  X → Y means "X determines Y"                       │
│  If we know X, we can find unique Y                 │
├─────────────────────────────────────────────────────┤
│ Normalization:                                      │
│  ✅ Eliminates redundancy                          │
│  ✅ Prevents anomalies                             │
│  ✅ Data integrity                                 │
│  ❌ More JOINs (slower reads)                      │
│  ❌ Complex queries                                │
├─────────────────────────────────────────────────────┤
│ Denormalization:                                    │
│  ✅ Faster reads (fewer JOINs)                     │
│  ✅ Simpler queries                                │
│  ❌ Redundancy                                     │
│  ❌ Update anomalies                               │
├─────────────────────────────────────────────────────┤
│ When to Use:                                        │
│  Normalize: OLTP (transactions, writes)             │
│  Denormalize: OLAP (analytics, reads)               │
└─────────────────────────────────────────────────────┘
```
---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** March 2026