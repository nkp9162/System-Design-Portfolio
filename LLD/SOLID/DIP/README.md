# Dependency Inversion Principle (DIP) — Python

## Overview

The **Dependency Inversion Principle (DIP)** states that:

> High-level modules should not depend on low-level modules. Both should depend on abstractions.
> 
> Abstractions should not depend on details. Details should depend on abstractions.

In simple terms:
- **Don't depend on concrete classes** - Depend on interfaces/abstractions
- **Inject dependencies** - Pass dependencies from outside rather than creating them internally
- **Invert the dependency flow** - Make low-level modules conform to interfaces defined by high-level modules

---

## Problem Context

In our **Invoice system**, we have:

**High-level module:**
- `InvoiceProcessor` - Business logic for processing invoices

**Low-level modules:**
- Database implementations (MySQL, MongoDB, PostgreSQL)
- Notification services (Email, SMS, Slack)

The challenge is: How do we design the system so that `InvoiceProcessor` can work with **any** database or notification service without being tightly coupled to specific implementations?

---

## ❌ DIP Violated Design

### Description

In this design, `InvoiceProcessor` (high-level module) **directly depends on** concrete implementations:
```python
class InvoiceProcessor:
    def __init__(self):
        self.database = MySQLDatabase()      # Direct dependency!
        self.email_service = EmailService()   # Direct dependency!
```

This creates **tight coupling** between high-level and low-level modules.

### Why is this problematic?

**Dependency Flow:**
```
┌─────────────────────┐
│ InvoiceProcessor    │  (High-level)
│ (Business Logic)    │
└─────────────────────┘
          │
          │ depends on (BAD!)
          ▼
┌─────────────────────┐
│ MySQLDatabase       │  (Low-level)
│ EmailService        │
└─────────────────────┘
```

**Problems:**
- Cannot switch from MySQL to MongoDB without modifying `InvoiceProcessor`
- Cannot switch from Email to SMS without modifying `InvoiceProcessor`
- Hard to test - cannot mock database or email service
- High-level module is polluted with low-level implementation details
- Changes in low-level modules force changes in high-level module

### Code Reference

**File:** `dip_violated.py`

### Problems with this approach:

- **Tight coupling** - High-level depends on concrete low-level classes
- **Hard to test** - Cannot inject mock dependencies
- **Inflexible** - Cannot switch implementations easily
- **Violates OCP** - Must modify code to change dependencies
- **Poor reusability** - InvoiceProcessor locked to specific implementations
- **Difficult maintenance** - Changes cascade through the system

---

## ✅ DIP Followed Design

### Description

We refactor by introducing **abstractions** and using **dependency injection**:

1. Create **abstract interfaces**:
   - `InvoiceRepository` (for database operations)
   - `NotificationService` (for notifications)

2. Make **low-level modules implement** these abstractions:
   - `MySQLRepository`, `MongoDBRepository`, `PostgreSQLRepository`
   - `EmailNotificationService`, `SMSNotificationService`, `SlackNotificationService`

3. Make **high-level module depend on abstractions**:
   - `InvoiceProcessor` accepts abstractions via constructor injection

### Inverted Dependency Flow
```
                  ┌──────────────────────┐
                  │   InvoiceProcessor   │  (High-level)
                  │   (Business Logic)   │
                  └──────────────────────┘
                            │
                            │ depends on
                            ▼
        ┌────────────────────────────────────────┐
        │         ABSTRACTIONS                   │
        │  InvoiceRepository                     │
        │  NotificationService                   │
        └────────────────────────────────────────┘
                            ▲
                            │ implement
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────────────┐  ┌────────────────┐  ┌───────────────┐
│ MySQLRepo     │  │ MongoDBRepo    │  │ EmailService  │
│ PostgreSQLRepo│  │                │  │ SMSService    │
└───────────────┘  └────────────────┘  └───────────────┘
    (Low-level implementations)
```

Now:
- High-level module depends on **abstractions**
- Low-level modules depend on **same abstractions**
- Dependencies are **inverted** (hence "Dependency Inversion")

### Code Reference

**File:** `dip_followed.py`

### Benefits of this approach:

- **Loose coupling** - High-level doesn't know about low-level implementations
- **Easy testing** - Inject mock objects for unit tests
- **Flexible** - Switch implementations by injecting different objects
- **Follows OCP** - Add new implementations without modifying existing code
- **Better reusability** - Components can be reused in different contexts
- **Clear contracts** - Abstractions define clear interfaces

---

## Comparison: Before vs After

| Aspect | Without DIP ❌ | With DIP ✅ |
|--------|---------------|-------------|
| **Coupling** | High (direct dependencies) | Low (depends on abstractions) |
| **Flexibility** | Cannot switch implementations | Easy to switch implementations |
| **Testing** | Hard (cannot mock) | Easy (inject mocks) |
| **Dependency flow** | High → Low (bad) | High ← Abstraction → Low (good) |
| **Code changes** | Modify high-level for new implementations | No changes needed |
| **Reusability** | Low (locked to specific implementations) | High (works with any implementation) |

---

## Benefits of Following DIP

### 1. **Decoupling**
High-level and low-level modules are independent. Changes in one don't affect the other.

### 2. **Testability**
Inject mock implementations for unit testing without touching production code.
```python
class MockRepository(InvoiceRepository):
    def save(self, invoice):
        # Mock implementation for testing
        pass

# Easy testing
processor = InvoiceProcessor(MockRepository(), MockNotification())
```

### 3. **Flexibility**
Switch implementations at runtime by injecting different objects.
```python
# Development: Use test database
dev_processor = InvoiceProcessor(TestDBRepository(), ConsoleNotification())

# Production: Use real database
prod_processor = InvoiceProcessor(MySQLRepository(), EmailNotification())
```

### 4. **Parallel Development**
Teams can work on high-level and low-level modules independently using agreed interfaces.

### 5. **Easy Maintenance**
Add new implementations without touching existing code.
```python
# Add new notification without modifying InvoiceProcessor
class WhatsAppNotification(NotificationService):
    def notify(self, invoice):
        # WhatsApp implementation
```

### 6. **Follows Other SOLID Principles**
DIP naturally leads to following OCP and ISP.

---

## How to Achieve DIP

### 1. **Define Abstractions**
Create abstract base classes or interfaces that define contracts.
```python
class InvoiceRepository(ABC):
    @abstractmethod
    def save(self, invoice): pass
```

### 2. **Use Dependency Injection**
Pass dependencies via constructor, method parameters, or property setters.
```python
# Constructor injection (most common)
def __init__(self, repository: InvoiceRepository):
    self.repository = repository
```

### 3. **Program to Interfaces**
High-level code should reference abstractions, not concrete classes.
```python
# Good: Depends on abstraction
def process(repository: InvoiceRepository):
    repository.save(invoice)

# Bad: Depends on concrete class
def process(repository: MySQLRepository):
    repository.save(invoice)
```

### 4. **Invert Control**
Let external code (often a DI container) create and inject dependencies.

---

## Dependency Injection Patterns

### 1. **Constructor Injection** (Recommended)
```python
class InvoiceProcessor:
    def __init__(self, repo: InvoiceRepository, notif: NotificationService):
        self.repo = repo
        self.notif = notif
```

**Pros:** Dependencies are required and immutable

### 2. **Method Injection**
```python
class InvoiceProcessor:
    def process(self, invoice: Invoice, repo: InvoiceRepository):
        repo.save(invoice)
```

**Pros:** Different dependencies per method call

### 3. **Property Injection**
```python
class InvoiceProcessor:
    @property
    def repository(self): return self._repo
    
    @repository.setter
    def repository(self, repo: InvoiceRepository):
        self._repo = repo
```

**Pros:** Optional dependencies, can be changed

---

## When to Apply DIP

### Signs you're violating DIP:

- High-level classes create (`new`) low-level objects directly
- Import statements bring in concrete classes instead of interfaces
- Hard to write unit tests without touching database/network
- Cannot swap implementations without code changes
- Changes in low-level modules break high-level modules
- Tight coupling between business logic and infrastructure

### Golden Rule:

> If you're creating dependencies with `new` or direct instantiation
> inside a class, you're probably violating DIP.
>
> Use dependency injection instead!

---

## Real-World Example

Think of a **smartphone and charger**:

### Without DIP (Bad Design)
```python
class iPhone:
    def __init__(self):
        # iPhone creates its own specific charger
        self.charger = AppleCharger()  # Tight coupling!
    
    def charge(self):
        self.charger.charge()

# Problem: iPhone can only use AppleCharger
# Cannot use USB-C or wireless charging
```

### With DIP (Good Design)
```python
class Charger(ABC):
    @abstractmethod
    def charge(self): pass

class iPhone:
    def __init__(self, charger: Charger):
        # iPhone accepts any charger through abstraction
        self.charger = charger
    
    def charge(self):
        self.charger.charge()

# Now iPhone can use ANY charger implementation!
iphone = iPhone(AppleCharger())
iphone = iPhone(USBCCharger())
iphone = iPhone(WirelessCharger())
```

---

## DIP and Other SOLID Principles

### DIP + OCP
DIP enables OCP by allowing new implementations without modifying existing code.

### DIP + LSP
Abstractions in DIP must follow LSP - all implementations must be substitutable.

### DIP + ISP
DIP works better with small, focused interfaces (ISP) rather than fat interfaces.

### DIP + SRP
Separating concerns (SRP) makes it easier to identify what should be abstracted.

---

## Key Takeaways

1. **Depend on abstractions** - Not on concrete implementations
2. **Use dependency injection** - Pass dependencies from outside
3. **Invert the flow** - Make low-level depend on high-level abstractions
4. **Program to interfaces** - Reference abstractions in high-level code
5. **Think about contracts** - Define clear interfaces between modules

---

## Common Mistakes

### ❌ **Creating Dependencies Internally**
```python
class Service:
    def __init__(self):
        self.db = MySQLDatabase()  # BAD: Creates dependency
```

### ❌ **Depending on Concrete Classes**
```python
def process(db: MySQLDatabase):  # BAD: Depends on concrete class
    db.save()
```

### ❌ **Leaky Abstractions**
```python
class Repository(ABC):
    @abstractmethod
    def execute_sql(self, query):  # BAD: SQL-specific abstraction
        pass
```

---

## Conclusion

The Dependency Inversion Principle is the cornerstone of flexible, maintainable architecture. By depending on abstractions and using dependency injection, you create systems that are:

- Loosely coupled and highly cohesive
- Easy to test and maintain
- Flexible and adaptable to change
- Reusable across different contexts

Remember: **High-level policy should not depend on low-level details.** Both should depend on abstractions that define clear contracts between them.

---

## Congratulations! 🎉

You've completed all five SOLID principles:

- **S** - Single Responsibility Principle (SRP) ✅
- **O** - Open/Closed Principle (OCP) ✅
- **L** - Liskov Substitution Principle (LSP) ✅
- **I** - Interface Segregation Principle (ISP) ✅
- **D** - Dependency Inversion Principle (DIP) ✅

These principles work together to create clean, maintainable, and scalable software. Keep practicing and applying them in your projects!

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026