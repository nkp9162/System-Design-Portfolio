# Open/Closed Principle (OCP) — Python

## Overview

The **Open/Closed Principle (OCP)** states that:

> Software entities (classes, modules, functions) should be open for extension but closed for modification.

In simple terms, you should be able to **add new functionality** without **changing existing code**. This reduces the risk of breaking existing features when adding new ones.

---

## Problem Context

Continuing with our **Invoice system**, we now focus on the persistence layer. Our system needs to support multiple database technologies:

- MySQL
- MongoDB
- PostgreSQL
- Redis (future requirement)

The challenge is: How do we support multiple databases without constantly modifying our repository class?

---

## ❌ OCP Violated Design

### Description

In this design, the `InvoiceRepository` class uses **if-elif conditions** to handle different database types:
```python
def save(self, invoice):
    if self.db_type == "mysql":
        # MySQL logic
    elif self.db_type == "mongodb":
        # MongoDB logic
    elif self.db_type == "postgresql":
        # PostgreSQL logic
```

This approach violates OCP because:
- Every new database requires **modifying** the `InvoiceRepository` class
- Adding conditions increases code complexity
- Risk of breaking existing database implementations
- Violates the "closed for modification" principle

### Code Reference

**File:** `ocp_violated.py`

### Problems with this approach:

- **Not extensible** - Must modify existing class for new databases
- **High risk** - Changes can break existing functionality
- **Code bloat** - if-elif chain grows with each new database
- **Testing overhead** - Must retest all databases after each change
- **Merge conflicts** - Multiple developers modifying same class

---

## ✅ OCP Followed Design

### Description

We refactor the code using **abstraction and inheritance**:

1. Create an **abstract base class** `InvoiceRepository` with a `save()` method
2. Each database gets its **own implementation class**:
   - `MySQLInvoiceRepository`
   - `MongoDBInvoiceRepository`
   - `PostgreSQLInvoiceRepository`
   - `RedisInvoiceRepository`

Now the system is:
- **Open for extension** - Add new database classes without touching existing code
- **Closed for modification** - Existing classes remain unchanged

### Architecture Diagram
```
                ┌────────────────────────────────┐
                │  InvoiceRepository (Abstract)  │
                ├────────────────────────────────┤
                │  + save(invoice: Invoice): void│
                └────────────────────────────────┘
                               ▲
                               │
         ┌─────────────┬───────┴───────┬──────────────┐
         │             │               │              │
┌────────────────┐ ┌───────────────┐ ┌────────────────┐ ┌────────────────┐
│   MySQLRepo    │ │  MongoDBRepo  │ │  PostgresRepo  │ │   RedisRepo    │
├────────────────┤ ├───────────────┤ ├────────────────┤ ├────────────────┤
│ + save(): void │ │ + save(): void│ │ + save(): void │ │ + save(): void │
└────────────────┘ └───────────────┘ └────────────────┘ └────────────────┘
```

### Code Reference

**File:** `ocp_followed.py`

### Benefits of this approach:

- **Easy extension** - Add new databases by creating new classes
- **Zero risk** - Existing code remains untouched
- **Clean code** - Each class has single responsibility
- **Parallel development** - Multiple developers work on different implementations
- **Easy testing** - Test new databases independently

---

## Comparison: Before vs After

| Aspect | Without OCP ❌ | With OCP ✅ |
|--------|---------------|-------------|
| **Adding new database** | Modify existing class | Create new class |
| **Risk of breaking code** | High (touches existing logic) | Low (existing code untouched) |
| **Code complexity** | Grows with if-elif chains | Stays clean and simple |
| **Testing effort** | Retest everything | Test only new implementation |
| **Code maintainability** | Decreases over time | Stays consistent |
| **Team collaboration** | Merge conflicts likely | Parallel work possible |

---

## Benefits of Following OCP

### 1. **Reduced Risk**
Existing, tested code remains unchanged. New features don't break old functionality.

### 2. **Easier Maintenance**
Each database implementation is isolated. Bug fixes are contained to specific classes.

### 3. **Better Scalability**
Adding support for 10 new databases doesn't make the codebase 10x more complex.

### 4. **Improved Testing**
New implementations can be tested independently without affecting existing tests.

### 5. **Parallel Development**
Multiple developers can add different database implementations simultaneously.

### 6. **Future-Proof**
System can grow without architectural changes. Just add new classes as needed.

---

## How to Achieve OCP

### 1. **Use Abstraction**
Define abstract base classes or interfaces that establish contracts.
```python
class InvoiceRepository(ABC):
    @abstractmethod
    def save(self, invoice):
        pass
```

### 2. **Program to Interface**
Depend on abstractions, not concrete implementations.
```python
# Good: Depends on abstraction
def process_invoice(invoice, repository: InvoiceRepository):
    repository.save(invoice)
```

### 3. **Favor Composition Over Inheritance**
When appropriate, use composition to extend behavior.

### 4. **Use Design Patterns**
Patterns like Strategy, Factory, and Template Method help achieve OCP.

---

## When to Apply OCP

### Signs your code is violating OCP:

- Multiple if-elif or switch statements checking types
- Every new feature requires modifying existing classes
- Fear of breaking existing functionality when adding features
- Code complexity grows linearly with features
- Frequent merge conflicts in the same files

### Golden Rule:

> When you need to add new functionality, ask:
> 
> "Can I do this by adding new code instead of changing existing code?"

---

## Real-World Example

Think of **plugin systems**:

### Without OCP (Bad Design)
```
Text Editor core code:
- if (plugin == "spellcheck") { ... }
- elif (plugin == "syntax") { ... }
- elif (plugin == "git") { ... }

Problem: Every new plugin requires modifying editor core!
```

### With OCP (Good Design)
```
Text Editor provides Plugin Interface:
- SpellCheckPlugin implements Plugin
- SyntaxHighlightPlugin implements Plugin
- GitPlugin implements Plugin

Benefit: Add unlimited plugins without touching editor core!
```

---

## Key Takeaways

1. **Open for extension** - Design systems that can grow with new features
2. **Closed for modification** - Protect existing, working code from changes
3. **Use abstractions** - Abstract base classes enable extensibility
4. **Reduce coupling** - Depend on interfaces, not concrete classes
5. **Think ahead** - Anticipate changes and design for flexibility

---


## Conclusion

The Open/Closed Principle helps create flexible, maintainable systems that can evolve without constant rewrites. By designing for extension rather than modification, you:

- Reduce bugs in existing functionality
- Speed up feature development
- Make code easier to test and maintain
- Enable team collaboration without conflicts

Start identifying variation points in your codebase and apply abstraction strategically. Your future self (and teammates) will thank you!

---

## Next Steps

Continue exploring SOLID principles:
- **S** - Single Responsibility Principle (SRP) ✅
- **O** - Open/Closed Principle (OCP) ✅
- **L** - Liskov Substitution Principle (LSP)
- **I** - Interface Segregation Principle (ISP)
- **D** - Dependency Inversion Principle (DIP)

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026