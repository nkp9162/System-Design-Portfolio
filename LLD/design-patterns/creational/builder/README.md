# Builder Design Pattern — Python

## Overview

The **Builder Pattern** is a creational design pattern that:

> Separates the construction of a complex object from its representation, allowing the same construction process to create different representations.

In simple terms:
- **Builds complex objects step-by-step**
- **Provides fluent interface** for readable code
- **Separates construction logic** from the object itself
- **Allows different representations** using same building process

---

## Real-World Analogy

### Building a House

Think of **constructing a house**:

- **Without Builder** - You tell the construction company: "Build me a house with 3 bedrooms, 2 bathrooms, kitchen, living room, garage, garden, pool, solar panels, smart home system..." (overwhelming!)

- **With Builder** - You work with an architect step-by-step:
  1. First, lay the foundation
  2. Build the walls
  3. Add the roof
  4. Install plumbing
  5. Add electrical systems
  6. Customize interior (optional)
  7. Add extras like pool, garden (optional)

The **builder (architect)** knows how to construct each part, and you can choose which parts you want. Different builders can create different types of houses (modern, traditional, minimalist) using the same process.

### Restaurant Order

Another example is **ordering a custom burger**:

- **Base** - Choose bun type
- **Protein** - Beef, chicken, veggie
- **Cheese** - Type and quantity
- **Vegetables** - Lettuce, tomato, onions
- **Sauces** - Ketchup, mayo, mustard
- **Extras** - Bacon, avocado, egg

You build your burger step-by-step, and the final product can be completely different based on your choices.

---

## Problem Statement

We're building a **Computer Configuration System** that needs to:

- Build computers with many components (CPU, RAM, GPU, storage, peripherals, etc.)
- Support different computer types (Gaming, Office, Server)
- Validate components during construction
- Allow optional components
- Provide readable, maintainable code

**Challenges:**

**Traditional constructor approach:**
```python
Computer(cpu, ram, storage, gpu, wifi, bluetooth, cooling, rgb, os, 
         monitor, keyboard, mouse, speakers, webcam, case)
```

Problems:
- 15+ parameters - impossible to remember
- Easy to mix up parameter order
- All parameters must be provided
- No validation during construction
- Not self-documenting

---

## ❌ Without Builder Pattern

### Description

Without Builder Pattern, we face the **Telescoping Constructor Problem**:
```python
class Computer:
    def __init__(self, cpu, ram, storage, gpu=None, wifi=False, 
                 bluetooth=False, cooling=None, rgb=False, os=None,
                 monitor=None, keyboard=None, mouse=None, 
                 speakers=False, webcam=False, case="Standard"):
        # 15 parameters!
```

**Usage:**
```python
# Hard to read, easy to make mistakes
pc = Computer("i9", 32, 1000, "RTX 4090", True, True, "Liquid", 
              True, "Windows 11", "4K Monitor", "RGB Keyboard", 
              "Gaming Mouse", True, True, "Gaming Tower")
```

### Code Reference

**File:** `builder_violated.py`

### Problems with this approach:

- **Too many parameters** - Constructor has 15+ parameters
- **Parameter order confusion** - Easy to swap parameters accidentally
- **All-or-nothing** - Must provide all parameters even if optional
- **No validation** - Invalid objects can be created
- **Not readable** - `True, False, None` don't explain what they mean
- **Hard to maintain** - Adding new parameter affects all calls
- **No step-by-step construction** - Everything at once

### Diagram: Without Builder Pattern
```
┌─────────────────────────────────────────┐
│           Computer                      │
├─────────────────────────────────────────┤
│  __init__(cpu, ram, storage, gpu,       │
│           wifi, bluetooth, cooling,     │
│           rgb, os, monitor, keyboard,   │
│           mouse, speakers, webcam,      │
│           case)                         │
│                                         │
│  15 PARAMETERS! 😱                      │
└─────────────────────────────────────────┘

Usage:
pc = Computer("i9", 32, 1000, "RTX 4090", True, True, ...)
              ↑     ↑   ↑       ↑         ↑     ↑
            What do these mean? Hard to tell!
```

---

## ✅ With Builder Pattern

### Description

With Builder Pattern, we:

1. **Create Builder class** - Handles object construction
2. **Provide fluent interface** - Methods return `self` for chaining
3. **Build step-by-step** - Add components one at a time
4. **Validate before returning** - Ensure object is valid
5. **Use Director (optional)** - Predefined build recipes

### Code Reference

**File:** `builder_followed.py`

### Architecture

The Builder Pattern has four main components:

1. **Product** - Complex object being built (`Computer`)
2. **Builder Interface** - Defines building steps (`ComputerBuilder`)
3. **Concrete Builders** - Implement specific variations (`GamingComputerBuilder`, `OfficeComputerBuilder`)
4. **Director (Optional)** - Orchestrates building process (`ComputerDirector`)

### Class Diagram
```
┌──────────────────────────────────────────┐
│           Computer                       │
│          (Product)                       │
├──────────────────────────────────────────┤
│  - cpu: str                              │
│  - ram: int                              │
│  - storage: int                          │
│  - gpu: str                              │
│  - ... (other components)                │
└──────────────────────────────────────────┘
                  ▲
                  │ builds
                  │
┌──────────────────────────────────────────┐
│      <<interface>>                       │
│      ComputerBuilder                     │
├──────────────────────────────────────────┤
│  + set_cpu(cpu)                          │
│  + set_ram(ram)                          │
│  + set_storage(storage)                  │
│  + set_gpu(gpu)                          │
│  + ... (other setters)                   │
│  + get_computer(): Computer              │
└──────────────────────────────────────────┘
                  ▲
                  │ implements
    ┌─────────────┼─────────────┬──────────┐
    │             │             │          │
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐
│ Gaming  │ │ Office   │ │ Server   │ │ Custom │
│Computer │ │Computer  │ │ Builder  │ │Builder │
│Builder  │ │ Builder  │ │          │ │        │
└─────────┘ └──────────┘ └──────────┘ └────────┘


┌──────────────────────────────────────────┐
│      ComputerDirector                    │
│      (Optional)                          │
├──────────────────────────────────────────┤
│  - builder: ComputerBuilder              │
├──────────────────────────────────────────┤
│  + build_budget_gaming_pc()              │
│  + build_high_end_gaming_pc()            │
│  + build_basic_office_pc()               │
└──────────────────────────────────────────┘
```

### How It Works
```
1. Create builder instance
   builder = GamingComputerBuilder()

2. Build step-by-step with method chaining (Fluent Interface)
   builder.set_cpu("Intel i9")
          .set_ram(32)
          .set_storage(1000)
          .set_gpu("RTX 4090")
          .set_cooling("Liquid Cooling")

3. Validate and get final product
   computer = builder.get_computer()

4. Each method returns 'self' enabling chaining
   def set_cpu(self, cpu):
       self.computer.cpu = cpu
       return self  # Returns builder for chaining
```

---

## Comparison: Before vs After

| Aspect | Without Builder ❌ | With Builder ✅ |
|--------|-------------------|-----------------|
| **Readability** | `Computer("i9", 32, 1000, ...)` | `builder.set_cpu("i9").set_ram(32)...` |
| **Parameter order** | Must remember exact order | No order dependency |
| **Optional parameters** | Must provide defaults/None | Just skip optional steps |
| **Validation** | No validation possible | Validate in `get_computer()` |
| **Different types** | Need multiple constructors | Different builder classes |
| **Maintainability** | Hard to add new parameters | Easy to add new methods |
| **Self-documenting** | `True, False` unclear | `set_wifi(True)` clear |

---

## Benefits of Builder Pattern

### 1. **Readable Code**
Code is self-documenting and easy to understand.
```python
# Clear what each parameter does
gaming_pc = (builder
    .set_cpu("Intel i9-13900K")
    .set_ram(32)
    .set_gpu("NVIDIA RTX 4090")
    .set_rgb_lighting(True)
    .get_computer())
```

### 2. **Step-by-Step Construction**
Build complex objects gradually, adding components as needed.

### 3. **Validation**
Validate object state before returning final product.
```python
def get_computer(self):
    if not self.computer.cpu:
        raise ValueError("CPU is required!")
    if self.computer.ram < 8:
        raise ValueError("Minimum 8GB RAM required!")
    return self.computer
```

### 4. **Different Representations**
Create different products using same building process.
```python
# Gaming PC with high-end specs
gaming_builder = GamingComputerBuilder()

# Office PC with moderate specs
office_builder = OfficeComputerBuilder()

# Server with server-optimized specs
server_builder = ServerBuilder()
```

### 5. **Immutability**
Can create immutable objects by making product class immutable.

### 6. **Director for Reusability**
Encapsulate common build sequences.
```python
director = ComputerDirector(builder)
budget_pc = director.build_budget_gaming_pc()
high_end_pc = director.build_high_end_gaming_pc()
```

---

## Real-World Use Cases

### 1. **Configuration Objects**
Building complex configurations (database, server, application settings)

### 2. **Document Builders**
Creating documents with various sections (PDF, HTML, XML generators)

### 3. **Query Builders**
Building SQL queries, MongoDB queries, Elasticsearch queries

### 4. **UI Components**
Building complex UI components with many properties

### 5. **HTTP Requests**
Building HTTP requests with headers, body, parameters

### 6. **Test Data Builders**
Creating test objects with specific configurations

---

## Implementation Steps

### Step 1: Define Product
```python
class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        # ... other attributes
```

### Step 2: Create Builder Interface
```python
class ComputerBuilder(ABC):
    @abstractmethod
    def set_cpu(self, cpu): pass
    
    @abstractmethod
    def set_ram(self, ram): pass
    
    @abstractmethod
    def get_computer(self): pass
```

### Step 3: Implement Concrete Builder
```python
class GamingComputerBuilder(ComputerBuilder):
    def __init__(self):
        self.computer = Computer()
    
    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self  # For chaining
    
    def get_computer(self):
        # Validate
        return self.computer
```

### Step 4: Use Builder
```python
builder = GamingComputerBuilder()
pc = builder.set_cpu("i9").set_ram(32).get_computer()
```

### Step 5: Add Director (Optional)
```python
class ComputerDirector:
    def build_gaming_pc(self):
        return (self.builder
            .set_cpu("i9")
            .set_ram(32)
            .get_computer())
```

---

## Trade-Offs

### Advantages ✅

- **Eliminates constructor bloat** - No 10+ parameter constructors
- **Highly readable** - Self-documenting, clear intent
- **Flexible** - Easy to add new optional components
- **Controlled construction** - Validate at each step or at end
- **Reusable build logic** - Director encapsulates common builds

### Disadvantages ❌

- **More code** - Requires separate builder classes
- **Overhead for simple objects** - Overkill if only 2-3 parameters
- **Learning curve** - More complex than simple constructor
- **Additional classes** - Builder, Director add to codebase

### When to Accept Trade-Offs

**Accept the overhead when:**
- Object has 5+ parameters (especially if many are optional)
- Need different representations of same product
- Construction logic is complex and reusable
- Validation is important during construction

**Avoid builder when:**
- Object is simple (2-3 required parameters, no optional)
- Construction is straightforward
- Object won't grow in complexity
- Team unfamiliar with pattern (unless teaching)

---

## Common Mistakes

### ❌ **Not returning self in builder methods**
```python
# Bad - cannot chain
def set_cpu(self, cpu):
    self.computer.cpu = cpu
    # Missing: return self

# Good - enables chaining
def set_cpu(self, cpu):
    self.computer.cpu = cpu
    return self
```

### ❌ **Using builder for simple objects**
```python
# Bad - overkill for simple object
class Person:
    def __init__(self):
        self.name = None
        self.age = None

# Just use constructor!
person = Person("John", 30)
```

### ❌ **Forgetting validation**
```python
# Bad - no validation
def get_computer(self):
    return self.computer

# Good - validate before returning
def get_computer(self):
    if not self.computer.cpu:
        raise ValueError("CPU required!")
    return self.computer
```

### ❌ **Not using Director for common builds**
```python
# Bad - repeating same build logic everywhere
pc1 = builder.set_cpu("i9").set_ram(32)...
pc2 = builder.set_cpu("i9").set_ram(32)...

# Good - use Director
director = ComputerDirector(builder)
pc1 = director.build_high_end_gaming_pc()
pc2 = director.build_high_end_gaming_pc()
```

---

## Conclusion

The Builder Pattern is essential for constructing complex objects with many parameters. It provides:

- Clean, readable code through fluent interface
- Flexibility to create different representations
- Step-by-step construction with validation
- Elimination of constructor parameter explosion

Use Builder Pattern when you have complex objects with many optional parameters, or when you need to create different representations of the same product. It's particularly valuable for configuration objects, document generators, and any domain where object construction is complex.

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026