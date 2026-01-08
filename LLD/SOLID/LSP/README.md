# Liskov Substitution Principle (LSP) — Python

## Overview

The **Liskov Substitution Principle (LSP)** states that:

> Objects of a superclass should be replaceable with objects of a subclass without breaking the application.

In simple terms, if class B is a subtype of class A, then we should be able to replace A with B without disrupting the behavior of our program. Child classes must honor the contracts established by parent classes.

---

## Problem Context

In our **Invoice system**, we have different types of invoice processors:

- **Regular Invoice Processor** - Handles standard invoices with tax calculation
- **Final Invoice Processor** - Handles locked/finalized invoices that cannot be modified
- **Zero Amount Invoice Processor** - Handles invoices with zero or minimal amounts

The challenge is: How do we ensure all processor types can be used interchangeably without breaking the system?

---

## ❌ LSP Violated Design

### Description

In this design, we have an `InvoiceProcessor` base class and several subclasses. However, some subclasses violate LSP by:

1. **`FinalInvoiceProcessor`** - Throws an exception instead of processing
2. **`ZeroAmountInvoiceProcessor`** - Returns `None` instead of a number

These violations break the contract established by the base class.

### Why is this problematic?

When using these processors in a function that expects any `InvoiceProcessor`:
```python
def generate_report(processor: InvoiceProcessor, invoices: list):
    total_revenue = 0
    for invoice in invoices:
        total = processor.process(invoice)  # Expects a number
        total_revenue += total  # Crashes if None or exception!
```

**Problems:**
- `FinalInvoiceProcessor` raises exception → crashes the program
- `ZeroAmountInvoiceProcessor` returns `None` → causes TypeError when adding
- Cannot safely substitute child classes for parent class
- Violates the "substitutability" principle

### Code Reference

**File:** `lsp_violated.py`

### Problems with this approach:

- **Breaks substitutability** - Child classes cannot replace parent class
- **Unexpected behavior** - Exceptions and None values surprise callers
- **Requires special handling** - Need try-catch blocks and None checks everywhere
- **Fragile code** - Adding new processor types risks breaking existing code
- **Contract violation** - Subclasses don't honor parent's promises

---

## ✅ LSP Followed Design

### Description

We refactor the code to ensure all subclasses maintain the contract:

1. **Consistent return type** - All processors return `float` (never `None` or exception)
2. **Behavioral consistency** - All processors handle their cases gracefully
3. **Pre-condition checking** - Use `can_process()` method to validate before processing
4. **Graceful degradation** - Return `0.0` for non-processable invoices instead of crashing

### Key Changes:

- Add `can_process()` method to check if invoice is valid
- Always return `float` from `process()` method
- Handle special cases internally without breaking contract
- Return `0.0` for invoices that cannot be processed

### Architecture Diagram
```
┌─────────────────────────────────────────────┐
│       InvoiceProcessor (Base Class)         │
│---------------------------------------------|                        
|       + can_process(invoice): bool          │
│       + process(invoice): float             │
│                                             │
│  Contract:                                  │
│  - Must always return float                 │
│  - Must never raise exceptions              │
│  - Must handle all valid inputs             │
└─────────────────────────────────────────────┘
                    ▲
                    │ follows contract
      ┌─────────────┼─────────────┬──────────────┐
      │             │             │              │
┌─────────────┐ ┌─────────┐ ┌──────────┐ ┌─────────────┐
│ Regular     │ │ Final   │ │ ZeroAmt  │ │ (Future     │
│ Invoice     │ │ Invoice │ │ Invoice  │ │  Processors │
│ Processor   │ │ Process │ │ Process  │ │  can be     │
│             │ │         │ │          │ │  added)     │
└─────────────┘ └─────────┘ └──────────┘ └─────────────┘
   Returns        Returns     Returns        Returns
   float          float       float          float
```

### Code Reference

**File:** `lsp_followed.py`

### Benefits of this approach:

- **True substitutability** - Any processor can replace base class
- **Predictable behavior** - All processors follow same contract
- **No surprises** - Callers don't need special error handling
- **Easy testing** - Each processor tested independently with same tests
- **Extensible** - New processors can be added without risk

---

## Comparison: Before vs After

| Aspect | Without LSP ❌ | With LSP ✅ |
|--------|---------------|-------------|
| **Return type consistency** | Mixed (float, None, exception) | Always float |
| **Substitutability** | Cannot replace parent safely | Full substitutability |
| **Error handling** | try-catch everywhere | Clean, no exceptions |
| **Code predictability** | Unpredictable behavior | Consistent behavior |
| **Caller complexity** | Must handle special cases | Simple, uniform usage |
| **Testing difficulty** | Hard to test uniformly | Easy to test with same suite |

---

## Benefits of Following LSP

### 1. **True Polymorphism**
You can use any subclass wherever parent class is expected, enabling true object-oriented design.

### 2. **Simplified Client Code**
Functions using base class don't need special handling for different subclasses.
```python
# Works with ANY processor
def generate_report(processor: InvoiceProcessor, invoices):
    total = sum(processor.process(inv) for inv in invoices)
    return total
```

### 3. **Reduced Bug Surface**
No unexpected exceptions or None values means fewer edge cases to handle.

### 4. **Better Testability**
All subclasses can be tested with the same test suite, ensuring consistent behavior.

### 5. **Easier Maintenance**
Adding new subclasses doesn't require changes to existing code that uses the base class.

### 6. **Stronger Type Safety**
Type hints and static analysis tools work better when LSP is followed.

---

## How to Follow LSP

### 1. **Honor Parent Contracts**
If parent method returns type T, all children must return type T (no None, no exceptions).

### 2. **Don't Strengthen Preconditions**
Child classes should accept at least the same inputs as parent class.
```python
# Bad: Child is more restrictive
class Parent:
    def process(self, value: int): pass

class Child(Parent):
    def process(self, value: int):
        if value < 0:
            raise ValueError("Only positive!")  # ❌ Strengthens precondition
```

### 3. **Don't Weaken Postconditions**
Child classes must provide at least what parent promises.
```python
# Bad: Child provides less
class Parent:
    def calculate(self) -> float: pass

class Child(Parent):
    def calculate(self) -> float:
        return None  # ❌ Weakens postcondition
```

### 4. **Maintain Behavioral Consistency**
Child behavior should be a logical extension of parent behavior, not a contradiction.

### 5. **Use Composition When Needed**
If a class cannot logically substitute parent, consider composition instead of inheritance.

---

## When to Apply LSP

### Signs your code is violating LSP:

- Child class throws exceptions parent doesn't
- Child returns different type than parent
- Need `isinstance()` checks to handle different subclasses
- Special if-else logic for specific subclass types
- Documentation warns about substitution limitations
- Unit tests fail when swapping subclasses

### Golden Rule:

> If you need to check the specific type of a subclass before using it,
> you're probably violating LSP.

---

## Key Takeaways

1. **Substitutability is key** - Child classes must work wherever parent works
2. **Honor contracts** - Return types, exceptions, and behavior must match
3. **No surprises** - Subclasses shouldn't behave unexpectedly
4. **Think before inheriting** - Not all "is-a" relationships should use inheritance
5. **Test uniformly** - Same tests should work for all subclasses

---

## Common Mistakes

### ❌ **The Rectangle-Square Problem**
```python
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h

class Square(Rectangle):  # Violates LSP!
    def set_width(self, w):
        self.width = self.height = w  # Unexpected behavior
```

### ❌ **The Empty Implementation**
```python
class Bird:
    def fly(self): pass

class Penguin(Bird):
    def fly(self):
        pass  # Does nothing - violates expected behavior
```

### ❌ **The NotImplementedError**
```python
class Base:
    def operation(self): pass

class Child(Base):
    def operation(self):
        raise NotImplementedError()  # Forces caller to handle exception
```

---

## Conclusion

The Liskov Substitution Principle ensures that inheritance hierarchies are logical and reliable. By maintaining behavioral consistency and honoring contracts, you create systems where:

- Any subclass can safely replace its parent
- Code is more predictable and maintainable
- Polymorphism works as intended
- Testing is simpler and more effective

Remember: Inheritance is not just about code reuse—it's about creating substitutable components that maintain behavioral consistency.

---

## Next Steps

Continue exploring SOLID principles:
- **S** - Single Responsibility Principle (SRP) ✅
- **O** - Open/Closed Principle (OCP) ✅
- **L** - Liskov Substitution Principle (LSP) ✅
- **I** - Interface Segregation Principle (ISP)
- **D** - Dependency Inversion Principle (DIP)

---

**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026