# Adapter Design Pattern — Python

## Overview

The **Adapter Pattern** is a structural design pattern that:

> Allows objects with incompatible interfaces to collaborate by converting the interface of one class into an interface expected by the clients.

In simple terms:
- **Makes incompatible interfaces work together**
- **Wraps existing class with new interface**
- **Acts as a bridge between two incompatible interfaces**

**Also known as:** Wrapper Pattern

---

## Real-World Analogy

### Power Adapter (Electrical)

Think of a **power adapter for international travel**:

- **Your laptop (Client)** - Expects US-style plug (110V, Type A)
- **UK power outlet (Adaptee)** - Provides UK-style socket (230V, Type G)
- **Power adapter (Adapter)** - Converts UK socket to US plug format

You plug your laptop into the adapter, and the adapter plugs into the UK outlet. Your laptop doesn't need to change, and the UK outlet doesn't need to change. The adapter makes them compatible.

### Memory Card Reader

Another example is a **memory card reader**:

- **Your computer (Client)** - Has USB port
- **SD card (Adaptee)** - Has SD card interface
- **Card reader (Adapter)** - Converts SD card interface to USB

The card reader allows your computer to read the SD card without either needing to change their interfaces.

---

## Problem Statement

We're building an **E-commerce Payment System** that needs to:

- Process payments using our standard interface
- Integrate multiple third-party payment gateways (Stripe, PayPal, Razorpay, Square)
- Support switching between payment gateways easily
- Avoid modifying application code for each new gateway

**Challenges:**

Each payment gateway has a different API:
- **Stripe** - Uses `create_charge(amount_cents, currency_code, email, description)`
- **PayPal** - Uses `make_payment(total, currency_type, payer_email, note)`
- **Razorpay** - Uses `initiate_transaction(price, curr, customer_id, remarks)`
- **Our App** - Expects `process_payment(amount, currency, customer_email)`

How do we integrate these incompatible interfaces without changing our application code?

---

## ❌ Without Adapter Pattern

### Description

Without Adapter Pattern, we face two bad options:

**Option 1:** Modify application code with if-elif for each gateway
```python
def checkout(self, amount, currency, email):
    if self.gateway_type == "stripe":
        # Convert to Stripe format
        self.gateway.create_charge(amount*100, currency, email, "Purchase")
    elif self.gateway_type == "paypal":
        # Convert to PayPal format
        self.gateway.make_payment(amount, currency, email, "Purchase")
    # ... more if-elif
```

**Option 2:** Cannot use third-party libraries at all

### Code Reference

**File:** `adapter_violated.py`

### Problems with this approach:

- **Incompatible interfaces** - Cannot integrate third-party libraries
- **Violates OCP** - Must modify app code for each new gateway
- **Tight coupling** - Application knows about all gateway implementations
- **Code duplication** - Similar conversion logic repeated everywhere
- **Hard to test** - Cannot mock gateways easily
- **Violates SRP** - Application handles both business logic and interface conversion
- **No reusability** - Conversion logic cannot be reused

### Diagram: Without Adapter Pattern
```
┌─────────────────────────────────────────┐
│       EcommerceApp                      │
│  (Must know about ALL gateways)         │
├─────────────────────────────────────────┤
│  checkout(amount, currency, email):     │
│    if gateway == "stripe":              │
│        stripe.create_charge(...)        │
│    elif gateway == "paypal":            │
│        paypal.make_payment(...)         │
│    elif gateway == "razorpay":          │
│        razorpay.initiate_transaction(...│
└─────────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Stripe  │ │ PayPal  │ │Razorpay │
    │   API   │ │   SDK   │ │ Client  │
    └─────────┘ └─────────┘ └─────────┘

Problem: App is tightly coupled to all incompatible interfaces!
```

---

## ✅ With Adapter Pattern

### Description

With Adapter Pattern, we:

1. **Define target interface** - `PaymentProcessor` with `process_payment()` method
2. **Create adapters** - One adapter for each third-party gateway
3. **Adapter implements target interface** - Appears compatible to client
4. **Adapter wraps adaptee** - Internally uses third-party API
5. **Client uses target interface** - Doesn't know about adapters or adaptees

### Code Reference

**File:** `adapter_followed.py`

### Architecture

The Adapter Pattern has four main components:

1. **Target Interface** - Interface that client expects (`PaymentProcessor`)
2. **Client** - Uses target interface (`EcommerceApp`)
3. **Adaptee** - Existing class with incompatible interface (`StripeAPI`, `PayPalSDK`)
4. **Adapter** - Implements target interface, wraps adaptee (`StripeAdapter`, `PayPalAdapter`)

### Class Diagram
```
┌──────────────────────────────────────────┐
│     <<interface>>                        │
│     PaymentProcessor                     │
│     (Target Interface)                   │
├──────────────────────────────────────────┤
│  + process_payment(amount, currency,     │
│                    customer_email)       │
└──────────────────────────────────────────┘
                  ▲
                  │ implements
    ┌─────────────┼─────────────┬──────────┬──────────┐
    │             │             │          │          │
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│Internal │ │ Stripe   │ │ PayPal   │ │Razorpay  │ │ Square   │
│Processor│ │ Adapter  │ │ Adapter  │ │ Adapter  │ │ Adapter  │
└─────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
                  │             │          │
                  │ wraps       │ wraps    │ wraps
                  ▼             ▼          ▼
            ┌──────────┐ ┌──────────┐ ┌──────────┐
            │ StripeAPI│ │PayPalSDK │ │Razorpay  │
            │(Adaptee) │ │(Adaptee) │ │ Client   │
            └──────────┘ └──────────┘ └──────────┘


┌──────────────────────────────────────────┐
│         EcommerceApp                     │
│         (Client)                         │
├──────────────────────────────────────────┤
│  - payment_processor: PaymentProcessor   │
├──────────────────────────────────────────┤
│  + checkout(amount, currency, email)     │
└──────────────────────────────────────────┘
         │
         │ uses
         ▼
    PaymentProcessor (Target Interface)
    
Client only knows about PaymentProcessor interface!
```

### How It Works
```
1. Client makes request using target interface
   app.checkout(100, "USD", "customer@example.com")
   
2. Client calls adapter (thinks it's calling PaymentProcessor)
   stripe_adapter.process_payment(100, "USD", "customer@example.com")
   
3. Adapter converts request to adaptee's format
   amount_cents = 100 * 100  # Convert to cents
   
4. Adapter calls adaptee's method
   stripe.create_charge(10000, "USD", "customer@example.com", "Purchase")
   
5. Adapter converts adaptee's response back to expected format
   return {"status": "success", "transaction_id": "ch_123", ...}
   
6. Client receives response in expected format
   result = {"status": "success", ...}
```

---

## Types of Adapters

### 1. Object Adapter (Composition) - Used in our example
Adapter **contains** instance of adaptee.
```python
class StripeAdapter(PaymentProcessor):
    def __init__(self):
        self.stripe = StripeAPI()  # Composition
    
    def process_payment(self, amount, currency, email):
        # Delegate to adaptee
        return self.stripe.create_charge(...)
```

**Pros:** More flexible, can adapt multiple classes  
**Cons:** Requires object creation

### 2. Class Adapter (Inheritance)
Adapter **inherits** from adaptee (not possible in Python if single inheritance).
```python
class StripeAdapter(PaymentProcessor, StripeAPI):  # Multiple inheritance
    def process_payment(self, amount, currency, email):
        # Can call inherited methods directly
        return self.create_charge(...)
```

**Pros:** Direct access to adaptee methods  
**Cons:** Less flexible, tight coupling through inheritance

**Note:** Python supports multiple inheritance, but object adapter is generally preferred.

---

## Comparison: Before vs After

| Aspect | Without Adapter ❌ | With Adapter ✅ |
|--------|-------------------|-----------------|
| **Interface compatibility** | Must change app or gateway | Adapter makes them compatible |
| **Coupling** | Tight (app knows all gateways) | Loose (app knows only interface) |
| **Adding gateways** | Modify application code | Create new adapter class |
| **Code changes** | Application code changes | No application code changes |
| **OCP** | Violates OCP | Follows OCP |
| **Reusability** | Conversion logic not reusable | Adapters reusable across apps |
| **Testing** | Hard to test in isolation | Easy to test with mock adapters |

---

## Benefits of Adapter Pattern

### 1. **Interface Compatibility**
Makes incompatible interfaces work together without modifying either.
```python
# Client uses standard interface
app = EcommerceApp(stripe_adapter)
app.checkout(100, "USD", "customer@example.com")

# Works the same with any adapter
app = EcommerceApp(paypal_adapter)
app.checkout(100, "USD", "customer@example.com")
```

### 2. **Single Responsibility Principle**
Separates interface conversion from business logic.

### 3. **Open/Closed Principle**
Add new adapters without modifying existing code.
```python
# Add new gateway - no changes to EcommerceApp
class SquareAdapter(PaymentProcessor):
    def process_payment(self, amount, currency, email):
        # Adapter logic
```

### 4. **Reusability**
Adapters can be reused across different applications.
```python
# Use same adapter in different apps
mobile_app = MobileApp(stripe_adapter)
web_app = WebApp(stripe_adapter)
```

### 5. **Flexibility**
Switch implementations at runtime.
```python
# Switch payment gateway based on user preference
if user_country == "India":
    processor = RazorpayAdapter()
else:
    processor = StripeAdapter()

app = EcommerceApp(processor)
```

### 6. **Easy Testing**
Create mock adapters for testing.
```python
class MockPaymentAdapter(PaymentProcessor):
    def process_payment(self, amount, currency, email):
        return {"status": "success", "transaction_id": "test-123"}

# Test with mock
app = EcommerceApp(MockPaymentAdapter())
```

---

## Real-World Use Cases

### 1. **Payment Gateway Integration**
Integrate Stripe, PayPal, Razorpay with unified interface

### 2. **Database Adapters**
Adapt different database drivers (MySQL, PostgreSQL, MongoDB) to single interface

### 3. **Logging Systems**
Adapt different logging libraries (log4j, winston, bunyan) to unified interface

### 4. **API Versioning**
Adapt old API to new API interface for backward compatibility

### 5. **Third-Party Library Integration**
Adapt external libraries to your application's interface

### 6. **Legacy System Integration**
Make old systems work with new systems

---

## Implementation Steps

### Step 1: Define Target Interface
```python
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, email): pass
```

### Step 2: Identify Adaptee
```python
class StripeAPI:
    def create_charge(self, amount_cents, currency_code, email, description):
        # Stripe's implementation
```

### Step 3: Create Adapter
```python
class StripeAdapter(PaymentProcessor):
    def __init__(self):
        self.stripe = StripeAPI()
    
    def process_payment(self, amount, currency, email):
        # Convert and delegate
        amount_cents = int(amount * 100)
        result = self.stripe.create_charge(amount_cents, currency, email, "Purchase")
        # Convert response
        return {"status": "success", ...}
```

### Step 4: Use Adapter
```python
adapter = StripeAdapter()
app = EcommerceApp(adapter)
```

---


## Trade-Offs

### Advantages ✅

- **Decouples client from adaptee** - Client doesn't know about adaptee's interface
- **Reusable adapters** - Same adapter can be used in multiple contexts
- **Easy to add new adapters** - Follows Open/Closed Principle
- **Single Responsibility** - Adapter handles only interface conversion
- **Flexible** - Can adapt multiple adaptees with single adapter

### Disadvantages ❌

- **Increased complexity** - Adds extra layer of abstraction
- **Performance overhead** - Additional method calls through adapter
- **More classes** - Need adapter for each incompatible interface
- **Not always obvious** - Might over-engineer simple conversions
- **Maintenance** - Must update adapter if adaptee's interface changes

### When to Accept Trade-Offs

**Accept the overhead when:**
- Integrating third-party libraries you cannot modify
- Need to support multiple incompatible interfaces
- Want to isolate interface changes from client code
- Reusability across applications is important

**Avoid adapter when:**
- You control both interfaces and can make them compatible
- Simple conversion can be done inline
- Performance is critical and overhead is unacceptable
- Only used in one place (might be over-engineering)

---

## Common Mistakes

### ❌ **Adapter doing too much**
```python
# Bad - Adapter has business logic
class StripeAdapter(PaymentProcessor):
    def process_payment(self, amount, currency, email):
        # ❌ DON'T add business logic in adapter
        if amount > 1000:
            apply_discount()
        # Adapter should only convert interfaces
```

### ❌ **Not following target interface**
```python
# Bad - Adapter has different method signature
class StripeAdapter(PaymentProcessor):
    def process_payment(self, amount, currency):  # ❌ Missing email parameter
        pass
```
---

## Conclusion

The Adapter Pattern is essential for integrating incompatible interfaces. It enables:

- Seamless integration of third-party libraries
- Reusability of existing code
- Flexibility to switch implementations
- Clean, maintainable architecture

Use Adapter Pattern when you need to make incompatible interfaces work together without modifying their source code. It's one of the most practical and widely-used design patterns in real-world applications.

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026