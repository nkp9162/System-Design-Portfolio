# Strategy Design Pattern — Python

## Overview

The **Strategy Pattern** is a behavioral design pattern that:

> Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

In simple terms:
- **Extract different behaviors** into separate classes
- **Switch between behaviors** at runtime
- **Avoid if-elif chains** for handling variations

---

## Real-World Analogy

Think of **transportation methods** to reach a destination:

- You can **walk** (slow, free)
- You can take a **bus** (medium speed, cheap)
- You can take a **taxi** (fast, expensive)
- You can take a **flight** (very fast, very expensive)

The **destination** (goal) is the same, but the **strategy** (how you get there) varies. You can choose different strategies based on your needs (time, budget, distance).

Similarly, in software, Strategy Pattern lets you choose different algorithms/behaviors at runtime.

---

## Problem Statement

We're building a **Payment Processing System** for an e-commerce platform. The system needs to support multiple payment methods:

- **Credit Card** (3% transaction fee)
- **PayPal** (4% transaction fee)
- **Bank Transfer** (flat $2 fee)
- **Cryptocurrency** (1% transaction fee)
- **Google Pay** (2% transaction fee) - Added later

Each payment method has:
- Different processing steps
- Different fee structures
- Different validation logic

**Challenge:** How do we handle multiple payment methods without creating a mess of if-elif statements?

---

## ❌ Without Strategy Pattern

### Description

Without Strategy Pattern, we typically use **if-elif conditions** to handle different payment methods:
```python
def process_payment(self, amount):
    if self.payment_type == "credit_card":
        # Credit card logic
    elif self.payment_type == "paypal":
        # PayPal logic
    elif self.payment_type == "bank_transfer":
        # Bank transfer logic
    elif self.payment_type == "cryptocurrency":
        # Crypto logic
    else:
        # Error
```

### Code Reference

**File:** `strategy_violated.py`

### Problems with this approach:

- **Violates OCP** - Must modify class to add new payment methods
- **Violates SRP** - One class handles all payment logic
- **Hard to test** - Cannot test payment methods independently
- **Code bloat** - if-elif chain grows with each new payment method
- **Poor maintainability** - All logic mixed together
- **No runtime flexibility** - Cannot easily switch payment methods
- **Tight coupling** - Payment logic tightly coupled to main class

### Diagram: Without Strategy Pattern
```
┌─────────────────────────────────────────┐
│      PaymentProcessor                   │
│  (Contains all payment logic)           │
├─────────────────────────────────────────┤
│  process_payment(amount):               │
│    if payment_type == "credit_card":    │
│        // Credit card logic             │
│    elif payment_type == "paypal":       │
│        // PayPal logic                  │
│    elif payment_type == "bank":         │
│        // Bank transfer logic           │
│    elif payment_type == "crypto":       │
│        // Crypto logic                  │
│    else:                                │
│        // Error                         │
└─────────────────────────────────────────┘

Problem: All logic in one place!
Adding new payment = Modifying this class!
```

---

## ✅ With Strategy Pattern

### Description

With Strategy Pattern, we:

1. **Define a common interface** (`PaymentStrategy`)
2. **Create separate classes** for each payment method
3. **Use composition** instead of if-elif conditions
4. **Switch strategies** at runtime

### Architecture

The Strategy Pattern has three main components:

1. **Strategy Interface** - Defines common interface for all algorithms
2. **Concrete Strategies** - Implement specific algorithms
3. **Context** - Uses a strategy object and can switch between them

### Code Reference

**File:** `strategy_followed.py`

### Class Diagram
```
┌─────────────────────────────────────────┐
│     <<interface>>                       │
│     PaymentStrategy                     │
├─────────────────────────────────────────┤
│  + pay(amount): bool                    │
│  + get_payment_name(): str              │
└─────────────────────────────────────────┘
                  ▲
                  │ implements
    ┌─────────────┼─────────────┬──────────────┬──────────────┐
    │             │             │              │              │
┌───────────┐ ┌──────────┐ ┌─────────┐ ┌────────────┐ ┌──────────┐
│ CreditCard│ │ PayPal   │ │ Bank    │ │ Crypto     │ │ GooglePay│
│ Payment   │ │ Payment  │ │ Transfer│ │ Payment    │ │ Payment  │
└───────────┘ └──────────┘ └─────────┘ └────────────┘ └──────────┘


┌─────────────────────────────────────────┐
│     PaymentProcessor                    │
│     (Context)                           │
├─────────────────────────────────────────┤
│  - strategy: PaymentStrategy            │
├─────────────────────────────────────────┤
│  + set_strategy(strategy)               │
│  + process_payment(amount)              │
└─────────────────────────────────────────┘
```

### How It Works
```
1. Client creates PaymentProcessor with a strategy
   processor = PaymentProcessor(CreditCardPayment())

2. Processor delegates work to strategy
   processor.process_payment(100)
   → strategy.pay(100)

3. Client can change strategy at runtime
   processor.set_strategy(PayPalPayment())
   processor.process_payment(200)
   → new_strategy.pay(200)
```

---

## Comparison: Before vs After

| Aspect | Without Strategy ❌ | With Strategy ✅ |
|--------|-------------------|-----------------|
| **Code structure** | One class with if-elif | Multiple strategy classes |
| **Adding new payment** | Modify existing class | Add new strategy class |
| **Testing** | Hard to test individual methods | Easy to test each strategy |
| **Flexibility** | Fixed at compile time | Switchable at runtime |
| **Maintainability** | All logic in one place | Separated concerns |
| **OCP compliance** | Violates OCP | Follows OCP |
| **SRP compliance** | Violates SRP | Follows SRP |

---

## Benefits of Strategy Pattern

### 1. **Open/Closed Principle**
Add new payment methods without modifying existing code.
```python
# Add new strategy without touching existing code
class ApplePayPayment(PaymentStrategy):
    def pay(self, amount):
        # Apple Pay logic
```

### 2. **Runtime Flexibility**
Switch algorithms dynamically based on user input or conditions.
```python
# User selects payment method
if user_choice == "credit":
    processor.set_strategy(CreditCardPayment())
elif user_choice == "paypal":
    processor.set_strategy(PayPalPayment())
```

### 3. **Better Testing**
Test each strategy independently.
```python
def test_credit_card_payment():
    strategy = CreditCardPayment()
    assert strategy.pay(100) == True
```

### 4. **Clean Code**
No more messy if-elif chains. Each strategy is self-contained.

### 5. **Single Responsibility**
Each strategy class has one job - implement one payment method.

### 6. **Easier Maintenance**
Changes to one payment method don't affect others.

---

## When to Use Strategy Pattern

### Use Strategy Pattern when:

✅ You have **multiple algorithms** for a specific task  
✅ You want to **switch algorithms** at runtime  
✅ You have **if-elif chains** checking types/conditions  
✅ You want to **isolate** algorithm implementation details  
✅ Different behaviors need **different data/logic**  

### Don't use Strategy Pattern when:

❌ You only have **one or two algorithms**  
❌ Algorithms **never change**  
❌ Simple logic that doesn't need abstraction  

---

## Real-World Use Cases

### 1. **Payment Systems**
Different payment gateways (Stripe, PayPal, Square)

### 2. **Compression Algorithms**
ZIP, RAR, 7Z, GZIP compression strategies

### 3. **Sorting Algorithms**
QuickSort, MergeSort, BubbleSort based on data size

### 4. **Navigation Systems**
Walking, driving, cycling, public transport routes

### 5. **Pricing Strategies**
Regular price, discount, seasonal, member pricing

### 6. **Authentication Methods**
Password, OAuth, Biometric, Two-Factor authentication

---

## Implementation Steps

### Step 1: Define Strategy Interface
```python
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount): pass
```

### Step 2: Create Concrete Strategies
```python
class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        # Implementation
```

### Step 3: Create Context Class
```python
class PaymentProcessor:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def process_payment(self, amount):
        return self.strategy.pay(amount)
```

### Step 4: Use It
```python
processor = PaymentProcessor(CreditCardPayment())
processor.process_payment(100)
```

---

## Key Takeaways

1. **Encapsulate algorithms** - Each algorithm in its own class
2. **Make them interchangeable** - All implement same interface
3. **Delegate to strategy** - Context delegates work to strategy object
4. **Runtime flexibility** - Can switch strategies on the fly
5. **Follows SOLID** - Especially OCP and SRP

---

## Common Misconceptions

### ❌ "Strategy Pattern means lots of classes"
**Reality:** Yes, but each class is simple, focused, and testable. Better than one complex class with if-elif chains.

### ❌ "I can use if-elif instead"
**Reality:** if-elif violates OCP and gets messy as you add more strategies. Strategy Pattern scales better.

### ❌ "Strategy Pattern is overkill"
**Reality:** For 2-3 simple cases, maybe. But for systems that will grow, Strategy Pattern saves time in the long run.

---

## Trade-offs of Strategy Pattern

While the Strategy pattern improves flexibility and clean separation of algorithms, it has some real costs:

- **Increased Number of Classes**  
  Each algorithm becomes a separate strategy class, increasing codebase size.

- **Indirect Control Flow**  
  The actual behavior is delegated to a strategy object, so the execution path is less obvious.
  > Client → Context → Strategy → Result

- **Over-engineering Risk**  
  Using Strategy for simple or stable logic adds unnecessary abstraction without clear benefits.

These trade-offs are acceptable when algorithms change frequently or need to be extended independently.

---

## Conclusion

The Strategy Pattern is essential for building flexible, maintainable systems. By encapsulating algorithms into separate classes, you:

- Write cleaner, more organized code
- Make systems easy to extend
- Enable runtime flexibility
- Follow SOLID principles

Use Strategy Pattern when you find yourself writing if-elif chains to handle different behaviors. Your future self will thank you!

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026