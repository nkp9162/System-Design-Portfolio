# Single Responsibility Principle (SRP) — Python

## Overview

The **Single Responsibility Principle (SRP)** states that:

> A class should have only one reason to change.

In simple terms, a class should focus on **one responsibility** and avoid handling multiple unrelated concerns.

---

## Problem Context

We are designing a simple **Invoice system** with the following requirements:

- Store invoice data (customer name, amount)
- Calculate total amount (including tax)
- Persist invoice data to database
- Send invoice notifications via email

A common mistake is to implement all these responsibilities inside a single `Invoice` class, which leads to tight coupling and maintenance nightmares.

---

## ❌ SRP Violated Design

### Description

In this design, the `Invoice` class is responsible for:

1. **Holding invoice data** (customer name, amount)
2. **Performing business calculations** (tax calculation)
3. **Managing database persistence** (saving to database)
4. **Sending notifications** (email communication)

This results in **multiple reasons for the class to change**, which directly violates SRP.

### Why is this problematic?

- If tax calculation logic changes → `Invoice` class must change
- If database technology changes → `Invoice` class must change
- If email provider changes → `Invoice` class must change
- If invoice data structure changes → `Invoice` class must change

**Result:** The class has **4 reasons to change** instead of 1.

### Code Reference

**File:** `srp_violated.py`

### Problems with this approach:

- **Testing is difficult** - Cannot test calculation without database dependencies
- **Tight coupling** - Changes in one area affect the entire class
- **Hard to maintain** - Mixed concerns make code harder to understand
- **No reusability** - Cannot reuse calculation or email logic elsewhere

---

## ✅ SRP Followed Design

### Description

We refactor the code by separating each responsibility into its own class:

1. **`Invoice`** → Only holds invoice data
2. **`InvoiceCalculator`** → Only handles tax calculations
3. **`InvoiceRepository`** → Only manages database operations
4. **`InvoiceEmailService`** → Only handles email notifications

Now each class has **exactly one reason to change**.

### Architecture Diagram
```
┌─────────────────────────────────────────────┐
│            Invoice System                   │
├─────────────────────────────────────────────┤
│  Invoice              → Data representation │
│  InvoiceCalculator    → Business logic      │
│  InvoiceRepository    → Persistence         │
│  InvoiceEmailService  → Communication       │
└─────────────────────────────────────────────┘
```

### Code Reference

**File:** `srp_followed.py`

### Benefits of this approach:

- **Single Responsibility** - Each class does one thing well
- **Easy to test** - Can test each component independently
- **Loosely coupled** - Changes in one class don't affect others
- **Highly reusable** - Components can be used in different contexts
- **Easy to extend** - Can add new features without modifying existing code

---

## Comparison: Before vs After

| Aspect | Without SRP ❌ | With SRP ✅ |
|--------|---------------|-------------|
| **Reasons to change** | 4 (data, calculation, database, email) | 1 per class |
| **Testing complexity** | High (coupled dependencies) | Low (isolated components) |
| **Code maintainability** | Difficult (mixed concerns) | Easy (clear separation) |
| **Reusability** | Low (tightly coupled) | High (independent components) |
| **Team collaboration** | Difficult (merge conflicts) | Easy (parallel development) |
| **Bug isolation** | Hard (cascading failures) | Easy (contained failures) |

---

## Benefits of Following SRP

### 1. **Improved Maintainability**
Each class is focused on a single concern, making it easier to understand and modify.

### 2. **Enhanced Testability**
You can write unit tests for each class independently without worrying about external dependencies.

### 3. **Better Code Organization**
Clear separation of concerns makes the codebase more organized and navigable.

### 4. **Increased Reusability**
Components can be reused across different parts of the application:
- Use `InvoiceCalculator` for quotes, orders, invoices
- Use `InvoiceEmailService` for different notification types

### 5. **Easier Debugging**
When a bug occurs, you know exactly which class to look at based on the type of issue.

### 6. **Parallel Development**
Multiple developers can work on different classes simultaneously without conflicts.

---

## When to Apply SRP

### Signs your class is violating SRP:

- Class has methods doing unrelated things
- Class name contains "and" or "or" (e.g., `InvoiceAndEmailManager`)
- You find yourself saying "This class does X, Y, and Z"
- Changes in one feature require modifying the class
- Hard to name the class because it does too many things

### Golden Rule:

> Ask yourself: "How many reasons does this class have to change?"
> 
> If the answer is more than **one**, it's time to refactor.

---

## Key Takeaways

1. **One class, one responsibility** - Each class should have a single, well-defined purpose
2. **One reason to change** - A class should only change when its responsibility changes
3. **Separation of concerns** - Keep different aspects of the system isolated
4. **Maintainability first** - Write code that's easy to understand and modify
5. **Think long-term** - SRP makes your codebase more scalable and robust

---

## Conclusion

The Single Responsibility Principle is fundamental to writing clean, maintainable code. By ensuring each class has only one reason to change, we create systems that are:

- Easier to understand
- Simpler to test
- Less prone to bugs
- More adaptable to change

Start applying SRP in your projects today, and you'll see immediate improvements in code quality and developer productivity.

---

## Next Steps

Continue exploring SOLID principles:
- **O** - Open/Closed Principle (OCP)
- **L** - Liskov Substitution Principle (LSP)
- **I** - Interface Segregation Principle (ISP)
- **D** - Dependency Inversion Principle (DIP)

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026