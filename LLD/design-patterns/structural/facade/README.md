# Facade Design Pattern — Python

## Overview

The **Facade Pattern** is a structural design pattern that:

> Provides a simplified interface to a complex subsystem, making it easier to use by hiding the complexity behind a unified interface.

In simple terms:
- **Hides complexity** of multiple subsystems
- **Provides simple interface** for common operations
- **Acts as a wrapper** around complex system
- **Reduces coupling** between client and subsystems

---

## Real-World Analogy

### Restaurant Service

Think of ordering food at a **restaurant**:

**Without Facade (Kitchen chaos):**
- You go to the kitchen
- Find the chef for appetizers
- Talk to another chef for main course
- Find the pastry chef for dessert
- Coordinate with dishwasher for plates
- Talk to sommelier for wine pairing
- Manage timing of all courses yourself

**With Facade (Waiter):**
- You tell the waiter: "I'll have the dinner special"
- Waiter coordinates with kitchen, chefs, sommelier
- Everything arrives perfectly timed
- You don't need to know kitchen complexity

The **waiter is the facade** - simple interface to complex kitchen operations.

### Car Dashboard

Another example is your **car's dashboard**:

**Without Facade:**
- Manually adjust fuel injection
- Control spark plug timing
- Manage transmission gears
- Monitor engine temperature
- Adjust air/fuel mixture

**With Facade:**
- Press gas pedal (go faster)
- Press brake pedal (slow down)
- Turn steering wheel (change direction)

The **dashboard and controls are facades** that hide engine complexity.

---

## Problem Statement

We're building a **Smart Home Automation System** with multiple subsystems:

- **Security System** - Alarms, sensors, cameras
- **Lighting System** - Smart bulbs, dimming, color control
- **Climate Control** - AC, heating, temperature
- **Entertainment System** - TV, sound system, streaming
- **Window Blinds** - Automated curtains
- **Door Locks** - Smart locks
- **Garage Door** - Automated garage

**Challenges:**

Users want simple commands like "Leave Home" or "Movie Night", but currently must:
- Know about 7+ different subsystems
- Remember exact sequence of operations
- Interact with each subsystem individually
- Coordinate timing and dependencies

This is too complex for average users!

---

## ❌ Without Facade Pattern

### Description

Without Facade, clients must interact with ALL subsystems directly:
```python
# Leaving home - Client must do everything manually
security = SecuritySystem()
lights = LightingSystem()
climate = ClimateControl()
entertainment = EntertainmentSystem()
blinds = WindowBlinds()
locks = DoorLocks()
garage = GarageDoor()

# Must call each system in correct order
entertainment.turn_off_tv()
entertainment.turn_off_sound_system()
lights.turn_off_all_lights()
climate.turn_off_climate_control()
blinds.close_all_blinds()
locks.lock_all_doors()
security.arm_system()
garage.open_garage()

# 8 method calls just to leave home! 
```

### Code Reference

**File:** `facade_violated.py`

### Problems with this approach:

- **Client knows too much** - Must understand all 7+ subsystems
- **Complex for simple tasks** - 8+ steps just to leave home
- **Error-prone** - Easy to forget steps or wrong order
- **Code duplication** - Same sequences repeated everywhere
- **Tight coupling** - Client depends on all subsystems
- **Hard to maintain** - Changes require updating all clients
- **Not user-friendly** - Too technical for end users

### Diagram: Without Facade Pattern
```
┌──────────────────────────────────────────┐
│            Client                        │
│     (Must know everything!)              │
└──────────────────────────────────────────┘
   │      │      │      │      │      │
   │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌──────┐ ┌────────┐ ┌───────┐
│ Secure │ │ Lights │ │Climate │ │ ENTs │ │ Blinds │ │ Locks │
└────────┘ └────────┘ └────────┘ └──────┘ └────────┘ └───────┘

Client directly coupled to ALL subsystems!
Must coordinate everything manually!
```

---

## ✅ With Facade Pattern

### Description

With Facade Pattern, we create a unified interface:
```python
# Simple facade interface
smart_home = SmartHomeFacade()

# Leaving home - ONE method call!
smart_home.leave_home()

# Movie night - ONE method call!
smart_home.movie_night()

# Sleep mode - ONE method call!
smart_home.sleep_mode()
```

Facade internally coordinates all subsystems.

### Code Reference

**File:** `facade_followed.py`

### Architecture

The Facade Pattern has three main components:

1. **Facade** - Simplified interface (`SmartHomeFacade`)
2. **Subsystems** - Complex classes that do actual work
3. **Client** - Uses facade instead of subsystems directly

### Class Diagram
```
┌──────────────────────────────────────────┐
│            Client                        │
│      (Simple interface!)                 │
└──────────────────────────────────────────┘
                  │
                  │ uses
                  ▼
┌──────────────────────────────────────────┐
│        SmartHomeFacade                   │
│          (FACADE)                        │
├──────────────────────────────────────────┤
│  + leave_home()                          │
│  + arrive_home()                         │
│  + movie_night()                         │
│  + sleep_mode()                          │
│  + party_mode()                          │
│  + vacation_mode()                       │
│  + emergency_mode()                      │
└──────────────────────────────────────────┘
   │      │      │      │      │      │
   │ coordinates all subsystems internally
   ▼      ▼      ▼      ▼      ▼      ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌──────┐ ┌────────┐ ┌───────┐
│ Secure │ │ Lights │ │Climate │ │ ENTs │ │ Blinds │ │ Locks │
└────────┘ └────────┘ └────────┘ └──────┘ └────────┘ └───────┘
      (Complex Subsystems)

Client only knows Facade!
Facade handles all complexity!
```

### How It Works
```
1. Client calls simple facade method
   smart_home.leave_home()

2. Facade coordinates subsystems internally
   def leave_home(self):
       self._entertainment.turn_off_tv()
       self._lights.turn_off_all_lights()
       self._climate.turn_off_climate_control()
       self._blinds.close_all_blinds()
       self._locks.lock_all_doors()
       self._security.arm_system()
       self._garage.open_garage()

3. Client gets simple result
   "Home secured and ready for departure!"

All complexity hidden inside facade!
```

---

## Comparison: Before vs After

| Aspect | Without Facade ❌ | With Facade ✅ |
|--------|-------------------|----------------|
| **Method calls** | 8+ calls for simple task | 1 call for any task |
| **Subsystem knowledge** | Must know all 7+ subsystems | Only know facade |
| **Coupling** | Tightly coupled to all subsystems | Loosely coupled to facade |
| **Code complexity** | Complex coordination in client | Simple method calls |
| **Error-prone** | Easy to forget steps | Facade handles everything |
| **Maintenance** | Changes affect all clients | Changes isolated to facade |
| **User-friendly** | Too technical | Simple and intuitive |

---

## Benefits of Facade Pattern

### 1. **Simplified Interface**
Complex operations become simple method calls.
```python
# Before: 8+ method calls
# After: 1 method call
smart_home.leave_home()
```

### 2. **Hides Complexity**
Client doesn't need to know about subsystems.

### 3. **Reduces Coupling**
Client depends only on facade, not on all subsystems.

### 4. **Easy to Use**
Non-technical users can control complex systems.

### 5. **Centralized Logic**
Common operations encapsulated in one place.
```python
# Movie night logic in ONE place
def movie_night(self):
    # All subsystem coordination here
```

### 6. **Optional Direct Access**
Advanced users can still access subsystems if needed.
```python
# Simple for most users
smart_home.movie_night()

# Advanced users can access subsystems
lights = smart_home.get_lighting_system()
lights.set_brightness(30)
```

---

## Real-World Use Cases

### 1. **Smart Home Systems**
Unified control for security, lighting, climate, entertainment

### 2. **Compiler/Interpreter**
Simple "compile" command hides lexer, parser, optimizer, code generator

### 3. **E-commerce Checkout**
Single "checkout" hides inventory, payment, shipping, notification systems

### 4. **Database Access**
ORM facades hide complex SQL, connection pooling, transactions

### 5. **Media Libraries**
Simple "play" command hides codecs, buffers, hardware acceleration

### 6. **Operating System**
File operations hide complex disk, cache, permission systems

---

## Implementation Steps

### Step 1: Identify Subsystems
```python
# Complex subsystems
security = SecuritySystem()
lights = LightingSystem()
climate = ClimateControl()
# ... more subsystems
```

### Step 2: Create Facade Class
```python
class SmartHomeFacade:
    def __init__(self):
        self._security = SecuritySystem()
        self._lights = LightingSystem()
        self._climate = ClimateControl()
        # Initialize all subsystems
```

### Step 3: Add Simple Methods
```python
def leave_home(self):
    """Simple method that coordinates subsystems"""
    self._lights.turn_off_all_lights()
    self._climate.turn_off_climate_control()
    self._locks.lock_all_doors()
    self._security.arm_system()
```

### Step 4: Use Facade
```python
facade = SmartHomeFacade()
facade.leave_home()  # Simple!
```

---

## Trade-Offs

### Advantages ✅

- **Greatly simplifies client code** - From 8+ calls to 1 call
- **Hides complexity** - Client doesn't need subsystem knowledge
- **Reduces dependencies** - Only depends on facade
- **Easy to understand** - Clear, semantic method names
- **Centralizes common operations** - Reusable scenarios

### Disadvantages ❌

- **Additional layer** - One more class in the system
- **Might limit functionality** - Facade may not expose everything
- **Can become god object** - If too many responsibilities added
- **Not always needed** - Overkill for simple systems

### When to Accept Trade-Offs

**Accept the overhead when:**
- Subsystem is genuinely complex (5+ classes)
- Common operations involve multiple subsystems
- Users need simplified interface
- Want to decouple client from subsystem changes

**Avoid facade when:**
- Subsystem is simple (1-2 classes)
- Clients need full control over subsystem
- Adding unnecessary layer of indirection
- Facade would just be pass-through methods

---

## Common Mistakes

### ❌ **Facade doing business logic**
```python
# Bad - Facade should delegate, not implement
class SmartHomeFacade:
    def leave_home(self):
        # ❌ Don't implement logic in facade
        if temperature > 30:
            turn_on_ac()
        # Facade should just coordinate subsystems
```

### ❌ **Making subsystems inaccessible**
```python
# Bad - Making subsystems private prevents advanced usage
class SmartHomeFacade:
    def __init__(self):
        self.__security = SecuritySystem()  # ❌ Too restrictive
        
# Good - Provide getter for advanced users
def get_security_system(self):
    return self._security
```

### ❌ **Facade knowing too much**
```python
# Bad - Facade shouldn't know internal details
class SmartHomeFacade:
    def leave_home(self):
        # ❌ Don't access internal implementation details
        self._security.sensor_array[0].activate()
        
# Good - Use subsystem's public interface
self._security.arm_system()
```

### ❌ **Creating facade for simple system**
```python
# Bad - Unnecessary facade for one class
class SimpleFacade:
    def __init__(self):
        self.service = SimpleService()
    
    def do_thing(self):
        return self.service.do_thing()  # ❌ Just pass-through

# Just use SimpleService directly!
```

---

## Facade vs Adapter vs Decorator

### Facade
- **Purpose:** Simplify complex interface
- **Wraps:** Multiple classes (subsystem)
- **Intent:** Hide complexity

### Adapter
- **Purpose:** Make incompatible interfaces compatible
- **Wraps:** Usually one class
- **Intent:** Interface conversion

### Decorator
- **Purpose:** Add responsibilities dynamically
- **Wraps:** One object
- **Intent:** Enhance functionality

**Example:**
```python
# Facade - Simplifies multiple subsystems
facade.leave_home()  # Coordinates 7+ subsystems

# Adapter - Converts interface
adapter.process_payment()  # Converts to Stripe API

# Decorator - Adds behavior
encrypted_file.write()  # Adds encryption to file writing
```

---

## Conclusion

The Facade Pattern is essential for managing complexity in large systems. It provides:

- Simple, user-friendly interface to complex subsystems
- Reduced coupling between clients and subsystems
- Centralized control for common operations
- Improved maintainability and usability

Use Facade Pattern when you have complex subsystems that clients need to interact with, but you want to hide that complexity behind a simple, intuitive interface. It's particularly valuable in systems with multiple interconnected components like smart homes, enterprise applications, and frameworks.

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026