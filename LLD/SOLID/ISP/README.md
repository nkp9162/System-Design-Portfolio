# Interface Segregation Principle (ISP) — Python

## Overview

The **Interface Segregation Principle (ISP)** states that:

> No client should be forced to depend on methods it does not use.

In simple terms, it's better to have **many small, specific interfaces** rather than one large, "fat" interface. Classes should only implement the methods they actually need.

---

## Problem Context

In our **Invoice system**, we have various operations that can be performed on invoices:

- **Calculate total** (with tax calculation)
- **Save to database** (persistence)
- **Send email** (email notifications)
- **Generate PDF** (report generation)
- **Send SMS** (SMS notifications)

Different services need different combinations of these operations:
- **Full Service** - Needs all operations
- **ReadOnly Service** - Only needs calculation
- **Email Service** - Only needs email sending
- **Notification Service** - Needs email and SMS
- **Report Service** - Needs calculation and PDF generation

The challenge is: How do we design interfaces so classes implement only what they need?

---

## ❌ ISP Violated Design

### Description

In this design, we have a single "fat interface" `InvoiceOperations` that contains **all possible methods**:
```python
class InvoiceOperations(ABC):
    def calculate_total(self, invoice): pass
    def save_to_database(self, invoice): pass
    def send_email(self, invoice): pass
    def generate_pdf(self, invoice): pass
    def send_sms(self, invoice): pass
```

**Problem:** Every class implementing this interface must implement **ALL methods**, even if it doesn't need them!

### Why is this problematic?

- **ReadOnlyInvoiceService** only needs `calculate_total()` but is forced to implement 4 other methods
- **EmailOnlyInvoiceService** only needs `send_email()` but is forced to implement 4 other methods
- Unused methods throw `NotImplementedError`, which crashes at runtime
- Violates the principle of "no forced dependencies"

### Code Reference

**File:** `isp_violated.py`

### Problems with this approach:

- **Forced implementations** - Classes implement methods they don't use
- **Runtime errors** - Calling unneeded methods raises exceptions
- **Bloated classes** - Classes contain unnecessary code
- **Difficult maintenance** - Adding new operations affects all implementations
- **Poor design signals** - NotImplementedError indicates design flaw
- **Confusing API** - Users don't know which methods are safe to call

---

## ✅ ISP Followed Design

### Description

We refactor by creating **small, focused interfaces**:

1. **`InvoiceCalculator`** → Only calculation methods
2. **`InvoicePersistence`** → Only database methods
3. **`InvoiceEmailNotification`** → Only email methods
4. **`InvoicePDFGenerator`** → Only PDF methods
5. **`InvoiceSMSNotification`** → Only SMS methods

Now classes implement **only the interfaces they need** using multiple inheritance.

### Architecture Diagram
```
┌──────────────────────────────────────────────────────────┐
│              Segregated Interfaces                       │
├──────────────────────────────────────────────────────────┤
│  InvoiceCalculator        → calculate_total()            │
│  InvoicePersistence       → save_to_database()           │
│  InvoiceEmailNotification → send_email()                 │
│  InvoicePDFGenerator      → generate_pdf()               │
│  InvoiceSMSNotification   → send_sms()                   │
└──────────────────────────────────────────────────────────┘
                          ▲
                          │ implements only what's needed
        ┌─────────────────┼──────────────┬─────────────┐
        │                 │              │             │
┌───────────────┐  ┌──────────────┐  ┌─────────┐  ┌──────────┐
│FullInvoice    │  │ReadOnly      │  │EmailOnly│  │Report    │
│Service        │  │InvoiceService│  │Invoice  │  │Service   │
│               │  │              │  │Service  │  │          │
│Implements     │  │Implements    │  │Implem-  │  │Implements│
│ALL interfaces │  │Calculator    │  │ents     │  │Calculator│
│               │  │only          │  │Email    │  │+ PDF     │
└───────────────┘  └──────────────┘  │only     │  └──────────┘
                                     └─────────┘
```

### Code Reference

**File:** `isp_followed.py`

### Benefits of this approach:

- **Clean implementations** - No forced methods, no NotImplementedError
- **Flexible composition** - Combine interfaces as needed
- **Clear intent** - Interface names show exactly what class does
- **Easy testing** - Test only implemented functionality
- **Better maintainability** - Changes to one interface don't affect others

---

## Comparison: Before vs After

| Aspect | Without ISP ❌ | With ISP ✅ |
|--------|---------------|-------------|
| **Interface size** | One fat interface (5 methods) | Five focused interfaces (1 method each) |
| **Forced methods** | Must implement all methods | Implement only needed methods |
| **Runtime errors** | NotImplementedError exceptions | No exceptions, clean code |
| **Class clarity** | Unclear what class actually does | Clear from implemented interfaces |
| **Maintenance** | Changes affect all classes | Changes isolated to relevant classes |
| **Flexibility** | Limited, all-or-nothing | High, mix and match interfaces |

---

## Benefits of Following ISP

### 1. **No Forced Dependencies**
Classes implement only the methods they actually use, keeping code clean and focused.

### 2. **Better Code Organization**
Each interface represents a single cohesive responsibility.

### 3. **Easier Testing**
Test only the interfaces a class implements, not a bloated set of methods.
```python
# Test only what the class actually implements
def test_readonly_service():
    service = ReadOnlyInvoiceService()
    assert service.calculate_total(invoice) > 0
    # No need to test save, email, PDF, SMS
```

### 4. **Reduced Side Effects**
Changes to one interface don't cascade to unrelated classes.

### 5. **Clearer API**
Users know exactly what a class can do by looking at its interfaces.

### 6. **Better Composition**
Mix and match interfaces to create exactly the functionality you need.
```python
# Combine only what you need
class MyService(InvoiceCalculator, InvoiceEmailNotification):
    # Implements only calculation and email
```

---

## How to Follow ISP

### 1. **Keep Interfaces Small**
Each interface should have a single, focused purpose.
```python
# Good: Focused interface
class Saveable(ABC):
    @abstractmethod
    def save(self): pass

# Bad: Fat interface
class DataOperations(ABC):
    @abstractmethod
    def save(self): pass
    @abstractmethod
    def load(self): pass
    @abstractmethod
    def export(self): pass
    @abstractmethod
    def import_(self): pass
```

### 2. **Use Role Interfaces**
Design interfaces around roles or capabilities, not around classes.
```python
# Interfaces based on capabilities
class Printable(ABC): pass
class Emailable(ABC): pass
class Exportable(ABC): pass
```

### 3. **Prefer Composition**
Use multiple small interfaces rather than inheritance from one large interface.

### 4. **Avoid Stub Implementations**
If you're writing empty methods or raising NotImplementedError, you're violating ISP.
```python
# Bad: Stub implementation indicates ISP violation
def send_email(self):
    raise NotImplementedError("This class doesn't send emails")
```

---

## When to Apply ISP

### Signs your interface is too fat:

- Implementations have many empty or stub methods
- Implementations raise NotImplementedError frequently
- Interface has methods from different, unrelated concerns
- Different clients need different subsets of methods
- Documentation warns "not all methods are supported"
- Hard to name the interface because it does too many things

### Golden Rule:

> If a class is forced to implement methods it doesn't use,
> your interface is too large. Split it!

---

## Real-World Example

Think of a **multi-function printer**:

### Without ISP (Bad Design)
```python
class Machine(ABC):
    def print(self): pass
    def scan(self): pass
    def fax(self): pass

class SimplePrinter(Machine):
    def print(self):
        print("Printing...")
    
    def scan(self):
        raise NotImplementedError("Can't scan!")  # ❌ Forced method
    
    def fax(self):
        raise NotImplementedError("Can't fax!")   # ❌ Forced method
```

### With ISP (Good Design)
```python
class Printer(ABC):
    def print(self): pass

class Scanner(ABC):
    def scan(self): pass

class FaxMachine(ABC):
    def fax(self): pass

class SimplePrinter(Printer):
    def print(self):
        print("Printing...")  # ✅ Only implements what it can do

class MultiFunctionPrinter(Printer, Scanner, FaxMachine):
    def print(self): print("Printing...")
    def scan(self): print("Scanning...")
    def fax(self): print("Faxing...")
```

---

## Key Takeaways

1. **Many small interfaces > One large interface** - Keep interfaces focused
2. **No forced methods** - Classes should implement only what they use
3. **Role-based design** - Design around capabilities, not classes
4. **Composition friendly** - Small interfaces enable flexible composition
5. **Client-focused** - Think about who uses the interface and what they need

---

## ISP vs SRP

While related, these principles are different:

| Principle | Focus | Question |
|-----------|-------|----------|
| **SRP** | Class responsibility | "Why should this class change?" |
| **ISP** | Interface segregation | "Why should clients depend on methods they don't use?" |

**Example:**
- SRP: An `InvoiceService` class should only handle invoice logic
- ISP: `InvoiceService` should implement only relevant interfaces, not all operations

---

## Common Mistakes

### ❌ **Implementing Empty Methods**
```python
def send_sms(self):
    pass  # Does nothing - violates ISP
```

### ❌ **Raising NotImplementedError**
```python
def generate_pdf(self):
    raise NotImplementedError()  # Indicates interface is too fat
```

### ❌ **One Interface for Everything**
```python
class IEverything(ABC):
    # 20+ methods here
    # This is a god interface - violates ISP
```

---

## Conclusion

The Interface Segregation Principle promotes designing **lean, focused interfaces** that don't burden implementers with unnecessary methods. By following ISP, you create:

- Cleaner, more maintainable code
- Flexible, composable designs
- Easier-to-test implementations
- Better separation of concerns

Remember: When designing interfaces, think about the clients that will use them. Give them only what they need, nothing more.

---

## Next Steps

Continue exploring SOLID principles:
- **S** - Single Responsibility Principle (SRP) ✅
- **O** - Open/Closed Principle (OCP) ✅
- **L** - Liskov Substitution Principle (LSP) ✅
- **I** - Interface Segregation Principle (ISP) ✅
- **D** - Dependency Inversion Principle (DIP)

---

**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026