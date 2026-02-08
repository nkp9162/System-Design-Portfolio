# Decorator Design Pattern — Python

## Overview

The **Decorator Pattern** is a structural design pattern that:

> Allows behavior to be added to individual objects, either statically or dynamically, without affecting the behavior of other objects from the same class.

In simple terms:
- **Wraps objects** to add new functionality
- **Maintains same interface** - decorator looks like wrapped object
- **Composable** - decorators can be stacked/layered
- **Runtime flexibility** - add/remove features dynamically

---

## Real-World Analogy

### Pizza with Toppings

Think of ordering a **pizza with toppings**:

**Without Decorator (Inheritance approach):**
- PizzaWithCheese class
- PizzaWithCheeseAndMushrooms class
- PizzaWithCheeseMushroomsAndOlives class
- PizzaWithCheeseMushroomsOlivesAndPepperoni class
- ... 100+ classes for all combinations! 😱

**With Decorator:**
- Base: Plain Pizza
- Wrap with: Cheese decorator
- Wrap with: Mushroom decorator
- Wrap with: Olive decorator
- Wrap with: Pepperoni decorator
- Mix and match as needed!

Each topping **wraps** the pizza, adds its flavor and cost, and presents itself as pizza!

### Getting Dressed

Another example is **wearing clothes**:
```
You (base component)
→ Wear underwear (first decorator)
→ Wear shirt (second decorator)
→ Wear jacket (third decorator)
→ Wear coat (fourth decorator)
```

Each layer **wraps** the previous layer, adds functionality (warmth, protection), but you're still "you" underneath!

---

## Problem Statement

We're building a **Coffee Shop Ordering System** that needs to:

- Offer multiple coffee types (SimpleCoffee, Espresso, Cappuccino)
- Allow customization with extras (Milk, Sugar, Cream, Caramel, Vanilla, Chocolate)
- Calculate total cost based on selections
- Support any combination of extras
- Allow same extra multiple times (double milk, triple sugar)

**Challenges:**

**Using inheritance for combinations:**
- Need class for **EVERY combination**
- With 6 extras: 2^6 = **64 classes**!
- Add one extra: **doubles** the number of classes
- Cannot create combinations dynamically
- Cannot add same extra multiple times
- Class explosion nightmare! 💥

---

## ❌ Without Decorator Pattern

### Description

Without Decorator, we use **inheritance** to create combinations:
```python
class SimpleCoffee:
    pass

class CoffeeWithMilk(SimpleCoffee):
    pass

class CoffeeWithSugar(SimpleCoffee):
    pass

class CoffeeWithMilkAndSugar(SimpleCoffee):  # 3rd class
    pass

class CoffeeWithMilkSugarAndCream(SimpleCoffee):  # 4th class
    pass

# ... need separate class for EVERY combination!
```

**Math behind the madness:**
- 1 extra: 2 classes (with/without)
- 2 extras: 4 classes (all combinations)
- 3 extras: 8 classes
- 4 extras: 16 classes
- 6 extras: **64 classes**!
- 10 extras: **1,024 classes**! 😱

### Code Reference

**File:** `decorator_violated.py`

### Problems with this approach:

- **Class explosion** - Exponential growth with each extra
- **Code duplication** - Same logic repeated in many classes
- **Inflexible** - Cannot create combinations at runtime
- **Cannot add extras multiple times** - Double milk needs another class
- **Violates OCP** - Must create new class for each combination
- **Hard to maintain** - Changes require modifying many classes
- **Tightly coupled** - All combinations must be known upfront
- **Cannot remove extras** - Object fixed at creation time

### Diagram: Without Decorator Pattern
```
Class Hierarchy Explosion:

SimpleCoffee
├── CoffeeWithMilk
├── CoffeeWithSugar
│   └── CoffeeWithMilkAndSugar
├── CoffeeWithCream
│   ├── CoffeeWithMilkAndCream
│   ├── CoffeeWithSugarAndCream
│   └── CoffeeWithMilkSugarAndCream
├── CoffeeWithCaramel
│   ├── CoffeeWithMilkAndCaramel
│   ├── CoffeeWithSugarAndCaramel
│   ├── CoffeeWithMilkSugarAndCaramel
│   ├── CoffeeWithCreamAndCaramel
│   ├── CoffeeWithMilkCreamAndCaramel
│   ├── CoffeeWithSugarCreamAndCaramel
│   └── CoffeeWithMilkSugarCreamAndCaramel
└── ... and it keeps growing exponentially!

With 4 extras: 16 classes
With 6 extras: 64 classes
Add 1 more extra: DOUBLE the classes!
```

---

## ✅ With Decorator Pattern

### Description

With Decorator, we **wrap objects** to add functionality:
```python
# Start with base
coffee = SimpleCoffee()

# Wrap with milk decorator
coffee = MilkDecorator(coffee)

# Wrap with sugar decorator
coffee = SugarDecorator(coffee)

# Wrap with cream decorator
coffee = WhippedCreamDecorator(coffee)

# Result: SimpleCoffee wrapped by Milk, wrapped by Sugar, wrapped by Cream
```


### Code Reference

**File:** `decorator_followed.py`

### Architecture

The Decorator Pattern has four main components:

1. **Component Interface** - Defines operations (`Coffee`)
2. **Concrete Component** - Base implementation (`SimpleCoffee`, `Espresso`)
3. **Decorator Base** - Wraps component, implements interface (`CoffeeDecorator`)
4. **Concrete Decorators** - Add specific features (`MilkDecorator`, `SugarDecorator`)

### Class Diagram
```
┌──────────────────────────────────────────┐
│      <<interface>>                       │
│         Coffee                           │
├──────────────────────────────────────────┤
│  + get_description(): str                │
│  + get_cost(): float                     │
└──────────────────────────────────────────┘
                  ▲
                  │ implements
         ┌────────┴────────┐
         │                 │
┌────────────────┐  ┌──────────────────┐
│ SimpleCoffee   │  │CoffeeDecorator   │
│  (Concrete     │  │  (Decorator      │
│   Component)   │  │   Base)          │
├────────────────┤  ├──────────────────┤
│+get_description│  │- _coffee: Coffee │ ◄─── HAS-A relationship
│+get_cost       │  │+get_description  │
└────────────────┘  │+get_cost         │
                    └──────────────────┘
                            ▲
                            │ extends (IS-A relationship)
      ┌─────────────────────┼─────────────────────┐
      │                     │                     │
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Milk      │      │   Sugar     │      │  Whipped    │
│  Decorator  │      │  Decorator  │      │   Cream     │
│             │      │             │      │  Decorator  │
└─────────────┘      └─────────────┘      └─────────────┘
```

### The Magic: IS-A and HAS-A Together!

**This is the KEY to Decorator Pattern:**
```python
class CoffeeDecorator(Coffee):           # IS-A Coffee (inheritance)
    def __init__(self, coffee: Coffee):
        self._coffee = coffee             # HAS-A Coffee (composition)
```

**Why this is powerful:**

1. **IS-A relationship (Inheritance):**
   - Decorator **is a** Coffee
   - Can be used wherever Coffee is expected
   - Has same interface (get_description, get_cost)

2. **HAS-A relationship (Composition):**
   - Decorator **has a** Coffee (wrapped component)
   - Delegates calls to wrapped component
   - Adds its own behavior before/after delegation

**This dual relationship enables:**
```python
# MilkDecorator IS-A Coffee, so can be passed to SugarDecorator
coffee = SugarDecorator(MilkDecorator(SimpleCoffee()))

# Each decorator:
# - IS-A Coffee (can be treated as Coffee)
# - HAS-A Coffee (wraps another Coffee)
# - This allows infinite wrapping/nesting!
```

**Visual representation:**
```
SugarDecorator
  └─ IS-A Coffee ✓ (can be used as Coffee)
  └─ HAS-A Coffee ✓
       └─ MilkDecorator
            └─ IS-A Coffee ✓ (can be used as Coffee)
            └─ HAS-A Coffee ✓
                 └─ SimpleCoffee
                      └─ IS-A Coffee ✓

Each layer:
- Looks like Coffee (IS-A)
- Contains Coffee (HAS-A)
- Perfect for wrapping!
```

### How It Works
```
1. Create base component
   coffee = SimpleCoffee()
   → Cost: 50, Desc: "Simple Coffee"

2. Wrap with first decorator
   coffee = MilkDecorator(coffee)
   → MilkDecorator.get_cost() = coffee.get_cost() + 10 = 60
   → MilkDecorator.get_description() = coffee.get_description() + " + Milk"

3. Wrap with second decorator
   coffee = SugarDecorator(coffee)
   → SugarDecorator.get_cost() = coffee.get_cost() + 5 = 65
   → SugarDecorator.get_description() = coffee.get_description() + " + Sugar"

4. Each decorator:
   - Calls wrapped component's method
   - Adds its own contribution
   - Returns combined result
```

**Method call chain:**
```
coffee.get_cost()
└─→ SugarDecorator.get_cost()
    └─→ self._coffee.get_cost() + 5
        └─→ MilkDecorator.get_cost()
            └─→ self._coffee.get_cost() + 10
                └─→ SimpleCoffee.get_cost()
                    └─→ return 50

Result: 50 + 10 + 5 = 65
```

---

## Comparison: Before vs After

| Aspect | Without Decorator ❌ | With Decorator ✅ |
|--------|---------------------|------------------|
| **Classes needed** | 2^N (exponential) | N + base (linear) |
| **6 extras** | 64 classes | 9 classes (3 base + 6 decorators) |
| **10 extras** | 1,024 classes | 13 classes (3 base + 10 decorators) |
| **New combination** | Create new class | Just wrap differently |
| **Runtime flexibility** | None (fixed at compile time) | Full (create any combination) |
| **Multiple extras** | Need new class | Just wrap multiple times |
| **Code duplication** | High (repeated logic) | None (logic in one place) |
| **Maintainability** | Nightmare | Easy |

---

## Benefits of Decorator Pattern

### 1. **No Class Explosion**
Linear growth instead of exponential.
```python
# With 6 decorators:
# Inheritance: 64 classes
# Decorator: 9 classes (3 base + 6 decorators)
```

### 2. **Runtime Flexibility**
Create combinations dynamically.
```python
# Customer chooses at runtime
extras = ["milk", "sugar", "cream"]  # User input

coffee = SimpleCoffee()
for extra in extras:
    if extra == "milk":
        coffee = MilkDecorator(coffee)
    elif extra == "sugar":
        coffee = SugarDecorator(coffee)
    # ... wrap based on user choice
```

### 3. **Add Features Multiple Times**
Same decorator can wrap multiple times.
```python
# Double milk, triple sugar!
coffee = SugarDecorator(
    SugarDecorator(
        SugarDecorator(
            MilkDecorator(
                MilkDecorator(SimpleCoffee())
            )
        )
    )
)
```

### 4. **Easy to Extend**
Add new decorators without modifying existing code.
```python
# Add new decorator - no changes to existing code!
class CinnamonDecorator(CoffeeDecorator):
    def get_cost(self):
        return self._coffee.get_cost() + 8.0
```

### 5. **Single Responsibility**
Each decorator has one job.
```python
# MilkDecorator: Only adds milk
# SugarDecorator: Only adds sugar
# Clean, focused classes!
```

### 6. **Composable**
Mix and match decorators freely.
```python
# Any combination works!
coffee1 = MilkDecorator(SugarDecorator(SimpleCoffee()))
coffee2 = SugarDecorator(MilkDecorator(Espresso()))
coffee3 = CaramelDecorator(VanillaDecorator(Cappuccino()))
```

---

## Real-World Use Cases

### 1. **GUI Components**
Add scrollbars, borders, shadows to windows

### 2. **I/O Streams**
BufferedReader wraps FileReader, wraps InputStreamReader

### 3. **Middleware**
Express.js, Django middleware - each adds functionality

### 4. **Authentication/Authorization**
Add authentication, logging, caching layers

### 5. **Text Formatting**
Bold, italic, underline - can be combined

### 6. **Compression/Encryption**
Wrap streams with compression, then encryption

---

## Implementation Steps

### Step 1: Define Component Interface
```python
class Coffee(ABC):
    @abstractmethod
    def get_description(self): pass
    
    @abstractmethod
    def get_cost(self): pass
```

### Step 2: Create Concrete Component
```python
class SimpleCoffee(Coffee):
    def get_description(self):
        return "Simple Coffee"
    
    def get_cost(self):
        return 50.0
```

### Step 3: Create Decorator Base
```python
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee  # HAS-A
    
    def get_description(self):
        return self._coffee.get_description()  # Delegate
    
    def get_cost(self):
        return self._coffee.get_cost()  # Delegate
```

### Step 4: Create Concrete Decorators
```python
class MilkDecorator(CoffeeDecorator):
    def get_description(self):
        return f"{self._coffee.get_description()} + Milk"
    
    def get_cost(self):
        return self._coffee.get_cost() + 10.0
```

### Step 5: Use Decorators
```python
coffee = SugarDecorator(MilkDecorator(SimpleCoffee()))
```

---

## Trade-Offs

### Advantages ✅

- **Avoids class explosion** - Linear vs exponential growth
- **Flexible combinations** - Mix and match at runtime
- **Open/Closed Principle** - Add decorators without modifying code
- **Single Responsibility** - Each decorator has one job
- **Composable** - Decorators work together seamlessly
- **Can add features multiple times** - Double, triple wrapping

### Disadvantages ❌

- **Many small objects** - Each decorator is an object
- **Identity issues** - Wrapped object != original object
- **Complexity** - Can be hard to debug deeply nested decorators
- **Order matters** - Different wrapping order = different result
- **Potential confusion** - Too many decorators can be overwhelming

### When to Accept Trade-Offs

**Accept decorator when:**
- Need flexible feature combinations
- Inheritance leads to class explosion
- Want to add/remove features at runtime
- Decorators are few and well-named

**Avoid decorator when:**
- Simple static inheritance suffices
- Only 2-3 combinations needed
- Object identity is critical
- Performance is critical (many layers = many method calls)

---

## Common Mistakes

### ❌ **Decorator not implementing same interface**
```python
# Bad - Decorator has different interface
class MilkDecorator:  # ❌ Doesn't extend Coffee
    def add_milk(self):  # ❌ Different method name
        pass

# Good - Same interface
class MilkDecorator(CoffeeDecorator):  # ✓ Extends Coffee
    def get_cost(self):  # ✓ Same method name
        return self._coffee.get_cost() + 10
```

### ❌ **Not delegating to wrapped component**
```python
# Bad - Not using wrapped component
class MilkDecorator(CoffeeDecorator):
    def get_cost(self):
        return 60.0  # ❌ Hardcoded, ignores wrapped component!

# Good - Delegate to wrapped component
class MilkDecorator(CoffeeDecorator):
    def get_cost(self):
        return self._coffee.get_cost() + 10.0  # ✓ Delegates
```

### ❌ **Forgetting the dual relationship**
```python
# Bad - Only HAS-A, not IS-A
class MilkDecorator:  # ❌ Not extending Coffee
    def __init__(self, coffee: Coffee):
        self._coffee = coffee  # Has-A only

# Good - Both IS-A and HAS-A
class MilkDecorator(CoffeeDecorator):  # ✓ IS-A Coffee
    def __init__(self, coffee: Coffee):
        self._coffee = coffee  # ✓ HAS-A Coffee
```

### ❌ **Too many decorators**
```python
# Bad - Overly complex
coffee = DecoratorA(DecoratorB(DecoratorC(DecoratorD(
    DecoratorE(DecoratorF(DecoratorG(SimpleCoffee())))))))
# Hard to read and debug!

# Good - Keep it reasonable
coffee = MilkDecorator(SugarDecorator(SimpleCoffee()))
# Clear and manageable
```

---

## Decorator vs Other Patterns

### Decorator vs Adapter

**Decorator:**
- **Purpose:** Add responsibilities to object
- **Interface:** Same as wrapped object
- **Example:** Add milk to coffee (still coffee)

**Adapter:**
- **Purpose:** Make incompatible interfaces compatible
- **Interface:** Different from adaptee
- **Example:** Adapt Stripe API to our payment interface

### Decorator vs Proxy

**Decorator:**
- **Purpose:** Add functionality
- **Focus:** Enhance behavior
- **Example:** Add logging, caching, authentication

**Proxy:**
- **Purpose:** Control access
- **Focus:** Manage access to object
- **Example:** Lazy loading, access control, remote proxy

### Decorator vs Composite

**Decorator:**
- **Purpose:** Add features to single object
- **Structure:** Linear wrapping (coffee → milk → sugar)
- **Example:** Decorated coffee

**Composite:**
- **Purpose:** Treat groups uniformly
- **Structure:** Tree structure (folder contains files/folders)
- **Example:** File system hierarchy

---

## Python's Built-in Decorators

Python has **function decorators** (different but related concept):
```python
# Function decorator (Python syntax)
@login_required
@cache_result
def get_user_data(user_id):
    return database.query(user_id)

# Equivalent to:
get_user_data = cache_result(login_required(get_user_data))
```

While Python's `@decorator` syntax is for functions, the **Decorator Pattern** is for objects. Both wrap something to add functionality!

---

## Conclusion

The Decorator Pattern is essential for adding responsibilities to objects flexibly and dynamically. It provides:

- Avoidance of class explosion through composition
- Runtime flexibility for feature combinations
- Adherence to Open/Closed Principle
- Clean, maintainable code

The **magic of Decorator** is the dual IS-A/HAS-A relationship - each decorator both **is** a component (can be used as one) and **has** a component (wraps one). This enables infinite, flexible wrapping while maintaining a consistent interface.

Use Decorator Pattern when you need flexible feature combinations without the nightmare of exponential class growth. Your future self will thank you when adding new features becomes trivial!

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** February 2026