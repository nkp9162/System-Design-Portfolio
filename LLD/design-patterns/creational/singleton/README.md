# Singleton Design Pattern — Python

## Overview

The **Singleton Pattern** is a creational design pattern that:

> Ensures a class has only one instance and provides a global point of access to it.

In simple terms:
- **Only one instance exists** - No matter how many times you create it
- **Global access point** - Instance accessible from anywhere
- **Lazy initialization** - Instance created only when needed
- **Thread-safe** - Works correctly in multi-threaded environment

---

## Real-World Analogy

### Government President/Prime Minister

Think of a **country's president or prime minister**:

- Only **one president** exists at a time
- Everyone refers to the **same president**
- You can't create multiple presidents
- Everyone has access to contact the president (global access point)
- When new president is elected, old one is replaced

Similarly, Singleton ensures only one instance exists!

### Device Manager in Operating System

Another example is **device manager** in an OS:

- Only **one device manager** controls all hardware
- All applications access the **same device manager**
- Prevents conflicts (imagine multiple managers trying to control same printer!)
- Centralized control ensures consistency

---

## Problem Statement

We're building applications that need **shared resources**:

- **Database Connection** - Only one connection pool needed
- **Configuration Manager** - Single source of configuration
- **Logger** - Centralized logging
- **Cache Manager** - Shared cache across application

**Challenges:**

**Without Singleton:**
- Multiple instances waste memory and resources
- Expensive initialization repeated unnecessarily
- Inconsistent state across instances
- Resource exhaustion (connection pools, file handles)
- No centralized control

---

## ❌ Without Singleton Pattern

### Description

Without Singleton, every instantiation creates a **new object**:
```python
db1 = DatabaseConnection()  # Creates new connection
db2 = DatabaseConnection()  # Creates ANOTHER new connection
db3 = DatabaseConnection()  # Creates YET ANOTHER connection

# Problem: 3 separate connections!
print(id(db1))  # Different ID
print(id(db2))  # Different ID
print(id(db3))  # Different ID
```

Each connection:
- Takes time to establish
- Consumes memory
- Uses resources (network sockets, file handles)

### Code Reference

**File:** `singleton_violated.py`

### Problems with this approach:

- **Resource waste** - Multiple instances consume memory unnecessarily
- **Expensive initialization** - Repeated for each instance
- **Inconsistent state** - Changes in one instance don't affect others
- **No global access** - Each part of code creates own instance
- **Connection pool exhaustion** - Too many database connections
- **Memory bloat** - Duplicate objects

### Diagram: Without Singleton
```
┌──────────────────────────────────────────┐
│        Application Code                  │
└──────────────────────────────────────────┘
         │          │          │
         │ new      │ new      │ new
         ▼          ▼          ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │   DB   │ │   DB   │ │   DB   │
    │ Conn 1 │ │ Conn 2 │ │ Conn 3 │
    │ID:1001 │ │ID:1002 │ │ID:1003 │
    └────────┘ └────────┘ └────────┘

Problem: Multiple instances created!
Each wastes resources!
```

---

## ✅ With Singleton Pattern

### Description

With Singleton, only **one instance** exists:
```python
db1 = DatabaseConnection()  # Creates instance
db2 = DatabaseConnection()  # Returns SAME instance
db3 = DatabaseConnection()  # Returns SAME instance

# All refer to same instance!
print(id(db1) == id(db2) == id(db3))  # True
```

No matter how many times you instantiate, you get the same object!

### Code Reference

**File:** `singleton_followed.py`

---

## Three Ways to Implement Singleton in Python

Python offers multiple ways to implement Singleton. Let's understand each:

---

### 1. Using `__new__` Method (Class Method Override)
```python
class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Initialize instance attributes here
        self.connection_id = id(self)
```

#### How It Works:

**Why `__new__` and not `__init__`?**

In Python, object creation happens in two steps:
1. **`__new__`** - Creates the object (returns instance)
2. **`__init__`** - Initializes the object (modifies instance)
```python
# Object creation flow:
obj = MyClass()
# Step 1: instance = MyClass.__new__(MyClass)
# Step 2: MyClass.__init__(instance)
```

**Why we MUST use `__new__`:**
- `__new__` **controls instance creation**
- `__init__` is called **AFTER** instance is created
- If we use `__init__`, Python creates new instance every time, then initializes it
- We need to **prevent instance creation**, so we override `__new__`

**Why separate `_initialize()` method?**
```python
def __new__(cls):
    if cls._instance is None:
        cls._instance = super().__new__(cls)
        cls._instance._initialize()  # ✓ Initialize only once
    return cls._instance

def _initialize(self):
    # This runs only once, when instance is first created
    self.connection_id = id(self)
```

**Problem if we used `__init__`:**
```python
# BAD - Don't do this!
def __init__(self):
    # This runs EVERY TIME, even for existing instance!
    self.connection_id = id(self)  # Would reset every time!
```

**Thread Safety (Double-Checked Locking):**
```python
if cls._instance is None:        # First check (no lock - fast)
    with cls._lock:               # Acquire lock
        if cls._instance is None: # Second check (with lock - safe)
            cls._instance = super().__new__(cls)
```

Why double-check?
- First check without lock is **fast** (no waiting)
- If instance exists, return immediately
- Only acquire lock if instance doesn't exist
- Second check ensures another thread didn't create instance while waiting for lock

#### Pros ✅
- **Simple and intuitive** - Easy to understand
- **Control over creation** - Direct control with `__new__`
- **Lazy initialization** - Instance created only when needed
- **Thread-safe** - With lock implementation

#### Cons ❌
- **Not truly encapsulated** - Can access `_instance` directly
- **Can be broken** - `DatabaseConnection._instance = None` breaks it
- **More boilerplate** - Need to handle `__new__` and `_initialize`

---

### 2. Using Metaclass (Most Pythonic)
```python
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigurationManager(metaclass=SingletonMeta):
    def __init__(self):
        # Initialize as normal
        self.config = {...}
```

#### How It Works:

**What is a Metaclass?**

In Python, **everything is an object**, including classes:
```python
class MyClass:
    pass

# MyClass is an object!
print(type(MyClass))  # <class 'type'>
```

- `type` is the **metaclass** of all classes
- Metaclass controls **how classes are created**
- Just like classes create instances, metaclasses create classes

**Why inherit from `type`?**
```python
class SingletonMeta(type):  # Inherit from type
    pass
```

- `type` is the default metaclass
- To create custom metaclass, we inherit from `type`
- This lets us customize class creation behavior

**How `metaclass` parameter works:**
```python
class ConfigurationManager(metaclass=SingletonMeta):
    pass

# Behind the scenes:
# ConfigurationManager = SingletonMeta('ConfigurationManager', bases, attrs)
```

When you use `metaclass=SingletonMeta`:
- `SingletonMeta` creates the class
- `SingletonMeta.__call__()` is invoked when you instantiate the class

**Flow:**
```python
config = ConfigurationManager()

# What actually happens:
# 1. Python calls: SingletonMeta.__call__(ConfigurationManager)
# 2. Our __call__ checks if instance exists
# 3. If not, creates instance using super().__call__()
# 4. Returns instance
```

**Why `__call__` in metaclass?**
- `__call__` makes an object callable
- When you do `ConfigurationManager()`, you're "calling" the class
- Metaclass's `__call__` intercepts this call
- We check if instance exists before creating new one

#### Pros ✅
- **Clean class definition** - No extra code in class itself
- **Reusable** - Same metaclass for multiple Singleton classes
- **Pythonic** - Uses Python's metaclass mechanism properly
- **Better encapsulation** - Harder to break accidentally

#### Cons ❌
- **Complex concept** - Metaclasses are advanced Python
- **Can be confusing** - Not obvious to beginners
- **Still breakable** - `ConfigurationManager.__class__._instances.clear()`

---

### 3. Using Decorator (Best for Python)
```python
def singleton(cls):
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Logger:
    def __init__(self):
        self.logs = []
```

#### How It Works:

**Decorator Magic:**
```python
@singleton
class Logger:
    pass

# Equivalent to:
class Logger:
    pass
Logger = singleton(Logger)  # Logger is now the wrapper function!
```

When you use `@singleton`:
1. Original `Logger` class is passed to `singleton()` function
2. `singleton()` returns `get_instance` function
3. `Logger` name now refers to `get_instance`, not the original class

**Calling decorated class:**
```python
logger = Logger()  # Actually calls get_instance()

# get_instance() does:
# 1. Check if instance exists in instances dict
# 2. If not, create: instances[cls] = cls()  (calls original Logger)
# 3. Return instance
```

**Closure for encapsulation:**
```python
def singleton(cls):
    instances = {}  # This is in closure - not accessible outside!
    
    def get_instance(*args, **kwargs):
        # get_instance can access 'instances' but outsiders cannot!
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance
```

**Why this is BEST for Python:**

❌ **`__new__` method - Can be broken:**
```python
class DatabaseConnection:
    _instance = None  # Class variable - accessible!

# Someone can do:
DatabaseConnection._instance = None  # ❌ Breaks Singleton!
db = DatabaseConnection()  # Creates new instance
```

❌ **Metaclass - Still breakable:**
```python
class ConfigurationManager(metaclass=SingletonMeta):
    pass

# Someone can do:
SingletonMeta._instances.clear()  # ❌ Clears all instances!
config = ConfigurationManager()  # Creates new instance
```

✅ **Decorator - Truly encapsulated:**
```python
@singleton
class Logger:
    pass

# Try to break it:
Logger._instances  # ❌ AttributeError: 'function' has no attribute '_instances'
Logger.instances   # ❌ AttributeError
# instances dict is in closure - INACCESSIBLE!
```

The `instances` dict is in **closure scope** - completely private and inaccessible from outside!

#### Pros ✅
- **Truly encapsulated** - `instances` dict in closure, not accessible
- **Cannot be broken** - No way to access internal state
- **Clean syntax** - Just add `@singleton` decorator
- **Pythonic** - Decorators are common Python pattern
- **Reusable** - Same decorator for any class
- **Simple to understand** - Clear what it does

#### Cons ❌
- **Function wrapper** - Class is replaced by function (minor issue)
- **Type checking issues** - `isinstance(logger, Logger)` might fail with some tools
- **Cannot subclass easily** - Decorated class is a function
``` 
Ex-:
  class FileLogger(Logger):
      pass
    
❌ TypeError: function is not a valid base class

```
---

## Comparison of Three Implementations

| Aspect | `__new__` Method | Metaclass | Decorator |
|--------|-----------------|-----------|-----------|
| **Encapsulation** | ❌ Weak (`_instance` accessible) | ⚠️ Medium (can access `_instances`) | ✅ Strong (closure) |
| **Breakability** | ❌ Easy to break | ⚠️ Can be broken | ✅ Very hard to break |
| **Complexity** | ⚠️ Medium | ❌ High (metaclasses) | ✅ Low (simple) |
| **Pythonic** | ⚠️ Okay | ✅ Very Pythonic | ✅ Most Pythonic |
| **Reusability** | ❌ Per class | ✅ Reusable | ✅ Reusable |
| **Code in class** | ❌ Yes (boilerplate) | ✅ Clean class | ✅ Clean class |
| **Thread safety** | ✅ Can implement | ✅ Can implement | ✅ Can implement |
| **Type checking** | ✅ Works fine | ✅ Works fine | ⚠️ Can have issues |

**Recommendation:** Use **Decorator** for most cases in Python due to superior encapsulation!

---

## Thread Safety Deep Dive

### Why Thread Safety Matters
```python
# Without thread safety:
Thread 1: if _instance is None:  # ✓ True
Thread 2: if _instance is None:  # ✓ True (both see None!)
Thread 1:     _instance = new()  # Creates instance A
Thread 2:     _instance = new()  # Creates instance B (overwrites A!)

# Result: Two instances created! Singleton broken!
```

### Solution: Locking
```python
_lock = threading.Lock()

def __new__(cls):
    if cls._instance is None:        # First check (no lock)
        with cls._lock:               # Acquire lock
            if cls._instance is None: # Second check (with lock)
                cls._instance = super().__new__(cls)
    return cls._instance
```

**Why double-checked locking?**

**Without double-check (only lock):**
```python
def __new__(cls):
    with cls._lock:  # Every call waits for lock - SLOW!
        if cls._instance is None:
            cls._instance = super().__new__(cls)
    return cls._instance
```
Problem: **Every call** acquires lock, even after instance exists. Slow!

**With double-check:**
```python
def __new__(cls):
    if cls._instance is None:        # Fast check - no lock
        with cls._lock:               # Only acquire if needed
            if cls._instance is None: # Verify still None
                cls._instance = super().__new__(cls)
    return cls._instance
```
Benefits:
- **Fast path**: If instance exists, return immediately (no lock)
- **Safe creation**: Lock prevents race condition during creation
- **Best of both worlds**: Fast after creation, safe during creation

### Understanding `thread.join()`
```python
threads = []
for i in range(5):
    thread = threading.Thread(target=create_instance, args=(i,))
    threads.append(thread)
    thread.start()  # Start thread (runs in background)

# Wait for all threads to complete
for thread in threads:
    thread.join()  # Main thread waits here
```

**What `join()` does:**
- Makes main thread **wait** for worker thread to finish
- Without `join()`, main thread continues immediately
- Main thread would exit before worker threads complete

**Example without `join()`:**
```python
# Start threads
for thread in threads:
    thread.start()

# No join() - main thread continues immediately!
print("Done!")  # ❌ Prints before threads finish!
# Program exits while threads still running!
```

**With `join()`:**
```python
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()  # Wait for each thread

print("Done!")  # ✓ Prints after ALL threads finish!
```

### Daemon vs Non-Daemon Threads

**Non-Daemon Threads (Default):**
```python
thread = threading.Thread(target=func)  # Non-daemon by default
thread.start()

# Program waits for non-daemon threads to complete before exiting
```

**Daemon Threads:**
```python
thread = threading.Thread(target=func, daemon=True)
thread.start()

# Program exits even if daemon threads are still running
# Daemon threads are killed by OS when program exits
```

**Key Differences:**

| Aspect | Non-Daemon | Daemon |
|--------|-----------|--------|
| **Program exit** | Waits for thread | Exits immediately |
| **Use case** | Important work | Background tasks |
| **Example** | Database save | Auto-save every 5 min |

**In our Singleton test:**
```python
thread = threading.Thread(target=create_instance, args=(i,))
# Non-daemon by default - good!
# We want to wait for all threads to verify Singleton works
```

We use **non-daemon** because:
- Need to verify all threads completed
- Need to check they all got same instance
- Results would be incomplete if program exited early

---

## Real-World Use Cases

### 1. **Database Connection Pool**
Single pool manages all connections

### 2. **Configuration Manager**
One source of configuration for entire application

### 3. **Logger**
Centralized logging across application

### 4. **Cache Manager**
Shared cache to avoid duplicate data

### 5. **Thread Pool**
Single pool manages worker threads

### 6. **Device Manager**
Control hardware devices (printer, scanner)

---

## Trade-Offs

### Advantages ✅

- **Controlled instance creation** - Only one instance
- **Global access point** - Available everywhere
- **Resource efficiency** - No duplicate instances
- **Lazy initialization** - Created only when needed
- **Consistent state** - Single source of truth

### Disadvantages ❌

- **Global state** - Can make testing difficult
- **Hidden dependencies** - Not obvious from function signature
- **Tight coupling** - Code depends on global Singleton
- **Hard to unit test** - Shared state between tests
- **Cannot be subclassed easily** - Singleton of subclass is different instance
- **Violates Single Responsibility** - Class controls both its behavior and instance creation

### When to Accept Trade-Offs

**Accept Singleton when:**
- Truly need single instance (connection pool, config)
- Resource is expensive to create
- Shared state is essential
- Global access simplifies architecture

**Avoid Singleton when:**
- Just want global variable (use module-level variable instead)
- Testing is primary concern (use dependency injection)
- Multiple instances might be needed later
- State should be isolated between tests

---

## Common Mistakes

### ❌ **Using Singleton as global variable**
```python
# Bad - Singleton used just for global access
class GlobalData:
    pass

# Good - Use module-level variable instead
global_data = {}
```

### ❌ **Not thread-safe implementation**
```python
# Bad - Not thread-safe
def __new__(cls):
    if cls._instance is None:
        cls._instance = super().__new__(cls)  # Race condition!
    return cls._instance

# Good - Thread-safe with lock
def __new__(cls):
    if cls._instance is None:
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
    return cls._instance
```

### ❌ **Using `__init__` for initialization**
```python
# Bad - __init__ called every time
def __init__(self):
    self.data = load_data()  # ❌ Reloads every instantiation!

# Good - Separate _initialize called once
def __new__(cls):
    if cls._instance is None:
        cls._instance = super().__new__(cls)
        cls._instance._initialize()
    return cls._instance

def _initialize(self):
    self.data = load_data()  # ✓ Loads only once
```

### ❌ **Making Singleton when not needed**
```python
# Bad - Premature Singleton
@singleton
class UserService:
    def get_user(self, id): pass

# Good - Regular class, inject dependencies
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
```

---

## Testing Singleton Classes

### Problem: Shared State Between Tests
```python
# Test 1
def test_config():
    config = ConfigurationManager()
    config.set("debug", True)
    assert config.get("debug") == True

# Test 2
def test_config_default():
    config = ConfigurationManager()
    # ❌ FAILS! debug is True from previous test!
    assert config.get("debug") == False
```

### Solution 1: Reset Method
```python
class ConfigurationManager:
    @classmethod
    def reset(cls):
        cls._instance = None

# In test
def test_config():
    ConfigurationManager.reset()  # Reset before test
    config = ConfigurationManager()
    # ... test code
```

### Solution 2: Dependency Injection
```python
# Don't use Singleton directly in business logic
class UserService:
    def __init__(self, config):  # Inject config
        self.config = config

# In tests, inject mock
def test_user_service():
    mock_config = MockConfig()
    service = UserService(mock_config)
```

---

## Conclusion

The Singleton Pattern ensures only one instance of a class exists throughout the application. It provides:

- Controlled instance creation
- Global access point
- Resource efficiency
- Consistent shared state

**Python offers three implementations:**
1. **`__new__` method** - Simple but breakable
2. **Metaclass** - Pythonic but complex
3. **Decorator** - Best encapsulation and most Pythonic

Use Singleton for resources that truly need single instance (database pools, loggers, configuration). Avoid overuse - not everything needs to be Singleton!

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** February 2026