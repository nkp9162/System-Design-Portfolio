# Factory Patterns — Python

## Overview

The **Factory Patterns** are creational design patterns that provide ways to create objects while hiding the creation logic. There are two main factory patterns:

### 1. Factory Method Pattern
> Defines an interface for creating an object, but lets subclasses decide which class to instantiate.

### 2. Abstract Factory Pattern
> Provides an interface for creating families of related or dependent objects without specifying their concrete classes.

In simple terms:
- **Factory Method** - One factory creates one type of product
- **Abstract Factory** - One factory creates a family of related products

---

## Real-World Analogy

### Factory Method Analogy
Think of a **restaurant**:
- You order "a burger" (abstract request)
- The kitchen decides whether to make a beef burger, chicken burger, or veggie burger based on context
- You don't need to know how it's made, just that you'll get a burger

### Abstract Factory Analogy
Think of a **furniture store**:
- **Modern Furniture Factory** creates: modern chair + modern table + modern sofa
- **Victorian Furniture Factory** creates: victorian chair + victorian table + victorian sofa
- **Art Deco Furniture Factory** creates: art deco chair + art deco table + art deco sofa

Each factory produces a **complete family** of matching furniture. You can't mix modern chair with victorian table - the factory ensures consistency.

---

## Problem Statement

We're building a **Cross-Platform UI Framework** that needs to:

- Support multiple operating systems (Windows, Mac, Linux, Android)
- Maintain consistent look and feel per OS
- Create UI components (Buttons, Checkboxes, etc.)
- Be easily extensible for new platforms

**Challenges:**
1. How to create OS-specific UI components without tight coupling?
2. How to ensure UI components match (all Windows or all Mac)?
3. How to add new OS support without modifying existing code?

---

## ❌ Without Factory Pattern

### Description

Without Factory Pattern, we use **if-elif conditions** to create objects:
```python
def create_ui(self):
    if self.os_type == "Windows":
        self.button = WindowsButton()
        self.checkbox = WindowsCheckbox()
    elif self.os_type == "Mac":
        self.button = MacButton()
        self.checkbox = MacCheckbox()
    # ... more conditions
```

### Code Reference

**File:** `factory_violated.py`

### Problems with this approach:

- **Tight coupling** - Application knows about all concrete UI classes
- **Violates OCP** - Must modify Application to add new OS
- **No consistency guarantee** - Could accidentally mix Windows button with Mac checkbox
- **if-elif bloat** - Creation logic grows with each OS
- **Hard to test** - Cannot easily mock UI components
- **Violates SRP** - Application handles both business logic and object creation

### Diagram: Without Factory
```
┌─────────────────────────────────────────┐
│         Application                     │
│  (Knows about ALL concrete classes)     │
├─────────────────────────────────────────┤
│  create_ui():                           │
│    if os == "Windows":                  │
│      button = WindowsButton()           │
│      checkbox = WindowsCheckbox()       │
│    elif os == "Mac":                    │
│      button = MacButton()               │
│      checkbox = MacCheckbox()           │
│    ...                                  │
└─────────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Windows │ │   Mac   │ │  Linux  │
    │   UI    │ │   UI    │ │   UI    │
    └─────────┘ └─────────┘ └─────────┘

Problem: Application is coupled to all concrete classes!
```

---

## ✅ With Factory Patterns

### Description

With Factory Patterns, we:

1. **Define abstract product interfaces** (Button, Checkbox)
2. **Create concrete products** for each OS (WindowsButton, MacButton, etc.)
3. **Define abstract factory interface** (GUIFactory)
4. **Create concrete factories** for each OS (WindowsFactory, MacFactory, etc.)
5. **Application uses factory** without knowing concrete classes

### Code Reference

**File:** `factory_followed.py`

### Architecture Overview
```
PRODUCTS (What we create)
┌────────────────────────────────────────────────────────┐
│                                                        │
│  <<interface>>        <<interface>>                    │
│    Button              Checkbox                        │
│                                                        │
│      ▲                    ▲                            │
│      │                    │                            │
│  ────┼────────────────────┼────                        │
│  │   │   │    │   │   │   │   │                       │
│  │   │   │    │   │   │   │   │                       │
│ Win Mac Lin  Win Mac Lin Android                      │
│                                                        │
└────────────────────────────────────────────────────────┘

FACTORIES (How we create them)
┌────────────────────────────────────────────────────────┐
│                                                        │
│           <<interface>>                                │
│            GUIFactory                                  │
│   + create_button(): Button                            │
│   + create_checkbox(): Checkbox                        │
│                                                        │
│                 ▲                                      │
│                 │ implements                           │
│     ┌───────────┼───────────┬──────────┐              │
│     │           │           │          │              │
│ Windows     Mac      Linux    Android                 │
│ Factory   Factory   Factory   Factory                 │
│                                                        │
└────────────────────────────────────────────────────────┘

APPLICATION (Client)
┌────────────────────────────────────────────────────────┐
│                Application                             │
│  - factory: GUIFactory                                 │
│  + create_ui()                                         │
│  + render()                                            │
└────────────────────────────────────────────────────────┘
         │
         │ uses
         ▼
    GUIFactory (abstract)
    
Application only knows about abstract interfaces!
```

---

## Factory Method vs Abstract Factory

### Factory Method Pattern

**Purpose:** Define interface for creating **one type** of object

**Structure:**
```python
class GUIFactoryCreator:
    @staticmethod
    def get_factory(os_type: str) -> GUIFactory:
        # Returns appropriate factory
        return WindowsFactory() or MacFactory() or ...
```

**Use when:**
- Creating single products
- Subclasses decide which class to instantiate
- Simple object creation with variations

### Abstract Factory Pattern

**Purpose:** Create **families of related objects**

**Structure:**
```python
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self): pass
    
    @abstractmethod
    def create_checkbox(self): pass
```

**Use when:**
- Creating families of related products
- Products must be used together
- Need to ensure consistency across products

### Key Difference

| Aspect | Factory Method | Abstract Factory |
|--------|---------------|------------------|
| **Focus** | Creating one product | Creating product families |
| **Methods** | Usually one factory method | Multiple factory methods |
| **Complexity** | Simpler | More complex |
| **Use case** | Single product variations | Related products that must match |

---

## Comparison: Before vs After

| Aspect | Without Factory ❌ | With Factory ✅ |
|--------|-------------------|----------------|
| **Coupling** | Tight (knows all concrete classes) | Loose (knows only abstractions) |
| **Extensibility** | Must modify Application | Just add new factory |
| **Consistency** | Can mix incompatible components | Factory ensures matching family |
| **Testing** | Hard to mock | Easy to inject mock factory |
| **OCP** | Violates (must modify for new OS) | Follows (add new factory class) |
| **SRP** | Violates (creation + logic) | Follows (separated concerns) |

---

## Benefits of Factory Patterns

### 1. **Decoupling**
Client code doesn't depend on concrete classes, only abstractions.
```python
# Client only knows about GUIFactory, not WindowsFactory
app = Application(factory)  # Works with ANY factory
```

### 2. **Consistency**
Abstract Factory ensures all products belong to same family.
```python
# WindowsFactory creates ONLY Windows components
factory = WindowsFactory()
button = factory.create_button()     # WindowsButton
checkbox = factory.create_checkbox()  # WindowsCheckbox
```

### 3. **Easy Extension**
Add new product families without modifying existing code.
```python
# Add Android support - no changes to Application!
class AndroidFactory(GUIFactory):
    def create_button(self): return AndroidButton()
    def create_checkbox(self): return AndroidCheckbox()
```

### 4. **Single Responsibility**
Separates object creation from business logic.

### 5. **Testability**
Easy to inject mock factories for testing.
```python
class MockFactory(GUIFactory):
    def create_button(self): return MockButton()
    def create_checkbox(self): return MockCheckbox()

app = Application(MockFactory())  # Test with mocks!
```

### 6. **Flexibility**
Switch between implementations at runtime.
```python
# Runtime selection based on user preference
if user_os == "Windows":
    factory = WindowsFactory()
else:
    factory = MacFactory()

app = Application(factory)
```

---

## When to Use Factory Patterns

### Use Factory Method when:

✅ Class can't anticipate the type of objects it needs to create  
✅ You want subclasses to specify objects to create  
✅ You have complex object creation logic  
✅ You want to delegate instantiation responsibility  

### Use Abstract Factory when:

✅ System needs to be independent of how products are created  
✅ System should work with multiple families of products  
✅ Family of products must be used together  
✅ You want to enforce consistency across products  

### Don't use when:

❌ Object creation is simple (just `new ClassName()`)  
❌ You'll never have variations of products  
❌ Adding unnecessary complexity to simple code  

---

## Real-World Use Cases

### 1. **UI Frameworks**
Cross-platform UI libraries (Qt, JavaFX, React Native)

### 2. **Database Connections**
Different database drivers (MySQL, PostgreSQL, MongoDB)

### 3. **Document Generation**
Different formats (PDF, Word, HTML)

### 4. **Game Development**
Different difficulty levels creating different enemies/items

### 5. **Plugin Systems**
Loading different plugin implementations

### 6. **Theme Systems**
Dark theme factory, light theme factory, custom theme factory

---

## Implementation Steps

### Step 1: Define Product Interfaces
```python
class Button(ABC):
    @abstractmethod
    def render(self): pass
```

### Step 2: Create Concrete Products
```python
class WindowsButton(Button):
    def render(self):
        print("Windows button")
```

### Step 3: Define Abstract Factory
```python
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: pass
```

### Step 4: Create Concrete Factories
```python
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
```

### Step 5: Use Factory in Client
```python
app = Application(WindowsFactory())
```

---

## Key Takeaways

1. **Encapsulate creation** - Hide object creation complexity
2. **Depend on abstractions** - Client uses interfaces, not concrete classes
3. **Ensure consistency** - Abstract Factory keeps product families consistent
4. **Easy extension** - Add new factories without modifying existing code
5. **Follows SOLID** - Especially OCP, DIP, and SRP

---

## Common Mistakes

### ❌ **Over-engineering**
Don't use factories for simple object creation. If `new ClassName()` works fine, use it.

### ❌ **Confusing the two patterns**
- Factory Method: Creating variations of one product
- Abstract Factory: Creating families of related products

### ❌ **Not using abstractions**
Factory should return abstract types, not concrete classes.
```python
# Bad
def create_button(self) -> WindowsButton:  # Concrete type

# Good
def create_button(self) -> Button:  # Abstract type
```

---

## Related Patterns

- **Builder Pattern** - Constructs complex objects step by step
- **Prototype Pattern** - Creates objects by cloning
- **Singleton Pattern** - Often used with factories to ensure one instance
- **Strategy Pattern** - Factories can create different strategies

---

## Conclusion

Factory Patterns are fundamental to writing flexible, maintainable object-oriented code. They:

- Decouple object creation from usage
- Make code more testable and extensible
- Enforce consistency across related objects
- Follow SOLID principles naturally

Use Factory Method for simple object creation variations, and Abstract Factory when you need to create families of related objects that must be used together.

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026