# State Design Pattern — Python

## Overview

The **State Pattern** is a behavioral design pattern that:

> Allows an object to alter its behavior when its internal state changes. The object will appear to change its class.

In simple terms:
- **Object behavior changes** based on its internal state
- **Each state is a separate class** with its own behavior
- **State transitions are explicit** and controlled
- **Eliminates complex if-elif chains** for state handling

---

## Real-World Analogy

### Traffic Light

Think of a **traffic light system**:

**Without State Pattern:**
```python
if light == "RED":
    if action == "change":
        light = "GREEN"
    if action == "walk":
        print("Don't walk!")
elif light == "YELLOW":
    if action == "change":
        light = "RED"
    if action == "walk":
        print("Don't walk!")
elif light == "GREEN":
    if action == "change":
        light = "YELLOW"
    if action == "walk":
        print("Walk!")
# Complex if-elif chains everywhere!
```

**With State Pattern:**
- **RedLight** state → knows it changes to Green, stops cars
- **YellowLight** state → knows it changes to Red, warns drivers  
- **GreenLight** state → knows it changes to Yellow, allows cars

Each state knows its own behavior and next state!

### Human Mood

Another example is **human emotional states**:

- **Happy State** → Laughs at jokes, helps others, spreads positivity
- **Angry State** → Short-tempered, confrontational responses
- **Sad State** → Low energy, withdrawn behavior
- **Excited State** → Energetic, talkative, enthusiastic

Same person, same stimulus (like a joke), but **completely different reactions** based on current emotional state.

---

## Problem Statement

We're building a **Vending Machine** that has multiple states:

- **Idle** - Waiting for money
- **HasMoney** - Money inserted, ready to dispense
- **Dispensing** - Currently dispensing item
- **OutOfStock** - No items available

**Challenges:**

Each state has different behavior for same operations:
- **insert_money()** - Accepted in Idle/HasMoney, rejected in Dispensing/OutOfStock
- **eject_money()** - Only works in HasMoney state
- **dispense()** - Only works in HasMoney with sufficient money
- **refill()** - Only works in Idle/OutOfStock states

How do we manage these state-dependent behaviors cleanly?

---

## ❌ Without State Pattern

### Description

Without State Pattern, we use **if-elif chains** in every method:
```python
def insert_money(self, amount):
    if self.state == "IDLE":
        # Idle behavior
    elif self.state == "HAS_MONEY":
        # HasMoney behavior
    elif self.state == "DISPENSING":
        # Dispensing behavior
    elif self.state == "OUT_OF_STOCK":
        # OutOfStock behavior

def eject_money(self):
    if self.state == "IDLE":
        # Idle behavior
    elif self.state == "HAS_MONEY":
        # HasMoney behavior
    # ... same if-elif chain repeated
```

Every method repeats the same if-elif pattern!

### Code Reference

**File:** `state_violated.py`

### Problems with this approach:

- **if-elif chains everywhere** - Every method has same structure
- **State logic scattered** - State behavior spread across methods
- **Hard to add states** - Must modify all methods
- **Mixed concerns** - State logic mixed with business logic
- **Error-prone** - Easy to miss state transitions
- **Hard to test** - Cannot test states independently
- **Violates OCP** - Must modify class to add states
- **Difficult to visualize** - State machine hidden in conditions

### Diagram: Without State Pattern
```
┌──────────────────────────────────────────┐
│        VendingMachine                    │
│   (State logic in if-elif chains)       │
├──────────────────────────────────────────┤
│  state: string                           │
│  item_count: int                         │
│  inserted_money: int                     │
├──────────────────────────────────────────┤
│  insert_money(amount):                   │
│    if state == IDLE:                     │
│        ...                               │
│    elif state == HAS_MONEY:              │
│        ...                               │
│    elif state == DISPENSING:             │
│        ...                               │
│    elif state == OUT_OF_STOCK:           │
│        ...                               │
│                                          │
│  eject_money():                          │
│    if state == IDLE:                     │
│        ...                               │
│    elif state == HAS_MONEY:              │
│        ...                               │
│    # Same if-elif repeated!              │
│                                          │
│  dispense():                             │
│    if state == IDLE:                     │
│        ...                               │
│    # Same if-elif again!                 │
└──────────────────────────────────────────┘

Problem: if-elif chains in EVERY method!
Adding new state = modifying ALL methods!
```

---

## ✅ With State Pattern

### Description

With State Pattern, we:

1. **Create State interface** - Defines methods all states must implement
2. **Create concrete state classes** - Each state has its own class
3. **Delegate to current state** - Context delegates behavior to state object
4. **States manage transitions** - Each state knows its next state

### Code Reference

**File:** `state_followed.py`

### Architecture

The State Pattern has three main components:

1. **Context** - Maintains reference to current state (`VendingMachine`)
2. **State Interface** - Defines common interface (`VendingMachineState`)
3. **Concrete States** - Implement state-specific behavior (`IdleState`, `HasMoneyState`, etc.)

### Class Diagram
```
┌──────────────────────────────────────────┐
│        VendingMachine                    │
│         (Context)                        │
├──────────────────────────────────────────┤
│  - _state: VendingMachineState           │
│  - item_count: int                       │
│  - inserted_money: int                   │
├──────────────────────────────────────────┤
│  + insert_money(amount)                  │
│  + eject_money()                         │
│  + dispense()                            │
│  + set_state(state)                      │
└──────────────────────────────────────────┘
                  │
                  │ delegates to
                  ▼
┌──────────────────────────────────────────┐
│     <<interface>>                        │
│     VendingMachineState                  │
├──────────────────────────────────────────┤
│  + insert_money(amount)                  │
│  + eject_money()                         │
│  + dispense()                            │
│  + refill(count)                         │
└──────────────────────────────────────────┘
                  ▲
                  │ implements
    ┌─────────────┼──────────┬───────────┬──────────┐
    │             │          │           │          │
┌─────────┐ ┌──────────┐ ┌────────┐ ┌─────────────┐
│  Idle   │ │ HasMoney │ │Dispens-│ │ OutOfStock  │
│  State  │ │  State   │ │ing     │ │   State     │
│         │ │          │ │State   │ │             │
└─────────┘ └──────────┘ └────────┘ └─────────────┘

Each state encapsulates its own behavior!
```

### State Transition Diagram
```
                    ┌─────────────┐
           ┌────────│    Idle     │◄────────┐
           │        └─────────────┘         │
           │              │                 │
   refill  │   insert_money                 │ dispense
   (stock  │              │                 │ (item dispensed)
    = 0)   │              ▼                 │
           │        ┌─────────────┐         │
           │   ┌────│  HasMoney   │─────┐   │
           │   │    └─────────────┘     │   │
           │   │          │             │   │
           │   │  dispense│             │   │
           │   │  (enough │         eject   │
           │   │   money) │         money   │
           │   │          ▼             │   │
           │   │    ┌─────────────┐     │   │
           │   │    │ Dispensing  │─────┘   │
           │   │    └─────────────┘         │
           │   │          │                 │
           │   │          │ (completes)     │
           │   │          ▼                 │
           ▼   │    ┌─────────────┐         │
      ┌─────────────│ OutOfStock  │─────────┘
      │             └─────────────┘
      │                   │
      └───────────────────┘
           refill
         (stock > 0)
```

### How It Works
```
1. Client calls method on Context
   machine.insert_money(50)

2. Context delegates to current state
   def insert_money(self, amount):
       return self._state.insert_money(amount)

3. State executes its behavior
   class IdleState:
       def insert_money(self, amount):
           self.machine.inserted_money += amount
           # Transition to next state
           self.machine.set_state(self.machine.get_has_money_state())

4. Behavior changes automatically with state
   Next insert_money() call uses HasMoneyState behavior!
```

---

## Comparison: Before vs After

| Aspect | Without State ❌ | With State ✅ |
|--------|-----------------|--------------|
| **State logic** | if-elif chains in every method | Each state is separate class |
| **Adding new state** | Modify all methods | Create new state class |
| **State behavior** | Scattered across methods | Encapsulated in state class |
| **State transitions** | Hidden in conditions | Explicit in state classes |
| **Testing** | Hard to test states in isolation | Easy to test each state |
| **Code complexity** | Grows with each state | Stays constant |
| **OCP compliance** | Violates (modify for new states) | Follows (add new classes) |

---

## Benefits of State Pattern

### 1. **Eliminates if-elif Chains**
No more complex conditionals in every method.
```python
# Before: if-elif in every method
def insert_money(self, amount):
    if self.state == "IDLE":
        # ...
    elif self.state == "HAS_MONEY":
        # ...

# After: Delegate to state
def insert_money(self, amount):
    return self._state.insert_money(amount)
```

### 2. **Encapsulates State Behavior**
Each state's logic is in its own class.
```python
# IdleState knows how to handle insert_money
class IdleState:
    def insert_money(self, amount):
        # Idle-specific behavior
```

### 3. **Explicit State Transitions**
State changes are clear and controlled.
```python
# Clear transition from Idle to HasMoney
self.machine.set_state(self.machine.get_has_money_state())
```

### 4. **Easy to Add States**
New states don't affect existing code.
```python
# Add MaintenanceState - no changes to other states!
class MaintenanceState(VendingMachineState):
    def insert_money(self, amount):
        print("Machine under maintenance")
```

### 5. **Independent Testing**
Test each state class separately.
```python
def test_idle_state():
    machine = VendingMachine(3)
    idle = IdleState(machine)
    assert idle.insert_money(50) == True
```

### 6. **Clear State Machine**
State diagram becomes easy to visualize and document.

---

## Real-World Use Cases

### 1. **Order Processing**
Draft → Submitted → Processing → Shipped → Delivered → Cancelled

### 2. **TCP Connection**
Closed → Listen → SYN_SENT → ESTABLISHED → CLOSE_WAIT → CLOSED

### 3. **Document Workflow**
Draft → Review → Approved → Published → Archived

### 4. **Game Character States**
Idle → Walking → Running → Jumping → Attacking → Dead

### 5. **Media Player**
Stopped → Playing → Paused → Buffering

### 6. **Authentication**
LoggedOut → LoggingIn → LoggedIn → SessionExpired

---

## Implementation Steps

### Step 1: Define State Interface
```python
class VendingMachineState(ABC):
    @abstractmethod
    def insert_money(self, amount): pass
    
    @abstractmethod
    def eject_money(self): pass
    
    @abstractmethod
    def dispense(self): pass
```

### Step 2: Create Concrete States
```python
class IdleState(VendingMachineState):
    def insert_money(self, amount):
        # Idle-specific behavior
        self.machine.set_state(self.machine.get_has_money_state())
```

### Step 3: Create Context
```python
class VendingMachine:
    def __init__(self):
        self._state = IdleState(self)
    
    def insert_money(self, amount):
        return self._state.insert_money(amount)
```

### Step 4: Use Context
```python
machine = VendingMachine()
machine.insert_money(50)  # Delegates to current state
```

---

## Key Takeaways

1. **State = Class** - Each state becomes a separate class
2. **Behavior changes with state** - Object appears to change class
3. **No if-elif chains** - State logic encapsulated in state classes
4. **Explicit transitions** - States control their own transitions
5. **Open/Closed Principle** - Add states without modifying existing code

---

## Trade-Offs

### Advantages ✅

- **Eliminates complex conditionals** - No if-elif chains
- **Encapsulates state logic** - Each state is self-contained
- **Easy to extend** - Add states without touching existing code
- **Clear state machine** - Easy to visualize and understand
- **Better testability** - Test each state independently
- **Organized code** - State behavior not scattered

### Disadvantages ❌

- **More classes** - One class per state
- **Overhead for simple states** - May be overkill for 2-3 states
- **State sharing** - Context state must be accessible to all states
- **Memory overhead** - All state objects created upfront (can be optimized)

### When to Accept Trade-Offs

**Accept the overhead when:**
- Have 4+ states with complex behavior
- State transitions are complex
- Need to add new states frequently
- State logic currently scattered and messy
- Want explicit, testable state machine

**Avoid state pattern when:**
- Only 2-3 simple states with trivial behavior
- State logic is already simple and clear
- States will never change
- if-elif is more readable for your case

---

## Common Mistakes

### ❌ **State classes modifying context directly**
```python
# Bad - State accessing context internals
class IdleState:
    def insert_money(self, amount):
        self.machine._internal_flag = True  # ❌ Accessing private

# Good - State uses context's public interface
class IdleState:
    def insert_money(self, amount):
        self.machine.inserted_money += amount  # ✓ Public property
```

### ❌ **Not defining all methods in state interface**
```python
# Bad - Incomplete interface
class State(ABC):
    @abstractmethod
    def action1(self): pass
    # Missing action2, action3...

# Good - Complete interface
class State(ABC):
    @abstractmethod
    def action1(self): pass
    
    @abstractmethod
    def action2(self): pass
    
    @abstractmethod
    def action3(self): pass
```

### ❌ **States with if-elif chains**
```python
# Bad - Defeating the purpose of State Pattern!
class HasMoneyState:
    def dispense(self):
        if self.machine.inserted_money >= 50:
            # ...
        elif self.machine.inserted_money >= 30:
            # ...
        # ❌ if-elif chain in state class!

# Good - Simple, clear logic
class HasMoneyState:
    def dispense(self):
        if self.machine.inserted_money >= self.machine.item_price:
            # Dispense
        else:
            # Insufficient money
```

### ❌ **Creating state objects on every transition**
```python
# Bad - Creating new state objects repeatedly
def transition_to_idle(self):
    self.state = IdleState(self)  # ❌ New object every time

# Good - Reuse state objects
def __init__(self):
    self._idle_state = IdleState(self)  # Create once
    self._has_money_state = HasMoneyState(self)

def transition_to_idle(self):
    self.state = self._idle_state  # ✓ Reuse
```

---

## State vs Strategy Pattern

Both patterns look similar but have different intents:

### State Pattern
- **Purpose:** Behavior changes based on internal state
- **Who controls:** Object itself controls state transitions
- **Awareness:** States know about each other (transitions)
- **Example:** Vending machine changes behavior based on state

### Strategy Pattern
- **Purpose:** Choose algorithm/strategy externally
- **Who controls:** Client chooses strategy
- **Awareness:** Strategies are independent
- **Example:** Choose payment method (Credit Card, PayPal)
```python
# State - Object controls state changes
machine.insert_money(50)  # Machine transitions state internally

# Strategy - Client chooses strategy
processor = PaymentProcessor(StripeStrategy())  # Client chooses
```

---

## Conclusion

The State Pattern is essential for managing complex state-dependent behavior. It provides:

- Clean elimination of if-elif chains
- Encapsulated, testable state logic
- Easy addition of new states
- Clear, explicit state machine

Use State Pattern when you have objects with state-dependent behavior, especially when you find yourself writing the same if-elif chains across multiple methods. It transforms messy conditional logic into clean, maintainable, object-oriented code.

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026