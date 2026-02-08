# Chain of Responsibility Design Pattern — Python

## Overview

The **Chain of Responsibility Pattern** is a behavioral design pattern that:

> Lets you pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain.

In simple terms:
- **Chain of handlers** - Multiple handlers linked together
- **Each handler decides** - Process or pass to next
- **Decoupled sender and receiver** - Sender doesn't know who handles
- **Dynamic chain** - Can add/remove handlers at runtime

---

## Real-World Analogy

### Customer Support Escalation

Think of **customer support tiers**:

**Level 1 Support (First Contact):**
- Handles simple questions, password resets
- If can't solve → escalates to Level 2

**Level 2 Support (Technical):**
- Handles software issues, installations
- If can't solve → escalates to Level 3

**Level 3 Support (Expert):**
- Handles complex bugs, server issues
- If can't solve → escalates to Management

**Management:**
- Handles critical emergencies
- Final decision maker

Each level **tries to help**, if can't → **passes to next level**. Customer doesn't know who will help, just that someone will!

### ATM Cash Withdrawal

Another example is **ATM dispensing money**:
```
Request: Withdraw ₹2,750

₹2,000 notes dispenser: Can give 1 note (₹2,000), passes ₹750
  ↓
₹500 notes dispenser: Can give 1 note (₹500), passes ₹250
  ↓
₹200 notes dispenser: Can give 1 note (₹200), passes ₹50
  ↓
₹50 notes dispenser: Can give 1 note (₹50), done!

Result: 1×₹2000 + 1×₹500 + 1×₹200 + 1×₹50
```

Each dispenser **handles what it can**, **passes the rest** to next!

---

## Problem Statement

We're building a **Support Ticket System** for an IT company:

- Different support levels: Level 1, Level 2, Level 3, Management
- Different ticket severities: LOW, MEDIUM, HIGH, CRITICAL
- Need to route tickets to appropriate support level
- Need different configurations: Business hours, after hours, weekend

**Challenges:**

**Using centralized if-elif approach:**
- Central system knows about ALL handlers
- Massive if-elif chains
- Hard to add/remove handlers
- Cannot change chain at runtime
- Tight coupling between system and handlers

---

## ❌ Without Chain of Responsibility Pattern

### Description

Without Chain of Responsibility, we use **centralized if-elif chains**:
```python
class SupportTicketSystem:
    def __init__(self):
        self.level1 = Level1Support()
        self.level2 = Level2Support()
        self.level3 = Level3Support()
        self.management = ManagementSupport()
    
    def process_ticket(self, ticket):
        # Centralized if-elif chain
        if self.level1.can_handle(ticket):
            self.level1.handle(ticket)
        elif self.level2.can_handle(ticket):
            self.level2.handle(ticket)
        elif self.level3.can_handle(ticket):
            self.level3.handle(ticket)
        elif self.management.can_handle(ticket):
            self.management.handle(ticket)
        else:
            print("ERROR: No handler can process!")
```

**OR** manually passing between handlers:
```python
class Level1Support:
    def __init__(self):
        self.next_handler = Level2Support()  # Must know next!
    
    def handle(self, ticket):
        if self.can_handle(ticket):
            # Process
        else:
            self.next_handler.handle(ticket)  # Pass manually
```

### Code Reference

**File:** `chain_of_responsibility_violated.py`

### Problems with this approach:

- **Centralized if-elif chains** - System knows about ALL handlers
- **Tight coupling** - System/handlers depend on each other
- **Hard to add handlers** - Must modify central system or all handlers
- **No runtime flexibility** - Cannot change chain dynamically
- **Violates OCP** - Must modify existing code for new handlers
- **Cannot have multiple chains** - One rigid chain for all
- **Code duplication** - Similar logic repeated
- **Hard to test** - Cannot test handlers independently

### Diagram: Without Chain of Responsibility
```
┌──────────────────────────────────────────┐
│    SupportTicketSystem                   │
│    (Knows about ALL handlers)            │
├──────────────────────────────────────────┤
│  process_ticket(ticket):                 │
│    if level1.can_handle(ticket):         │
│        level1.handle(ticket)             │
│    elif level2.can_handle(ticket):       │
│        level2.handle(ticket)             │
│    elif level3.can_handle(ticket):       │
│        level3.handle(ticket)             │
│    elif management.can_handle(ticket):   │
│        management.handle(ticket)         │
└──────────────────────────────────────────┘
         │          │          │         │
         ▼          ▼          ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐ ┌──────┐
    │Level 1 │ │Level 2 │ │Level 3 │ │Mgmt  │
    └────────┘ └────────┘ └────────┘ └──────┘

Problem: Central system tightly coupled to ALL handlers!
```

---

## ✅ With Chain of Responsibility Pattern

### Description

With Chain of Responsibility, we **chain handlers together**:
```python
# Create handlers
level1 = Level1Support()
level2 = Level2Support()
level3 = Level3Support()
management = ManagementSupport()

# Build chain
level1.set_next(level2).set_next(level3).set_next(management)

# Process ticket - handler decides to process or pass
level1.handle(ticket)  # Starts chain, flows automatically!
```

Each handler:
- **Checks if it can handle** - `_can_handle()`
- **Processes if capable** - `_process()`
- **Passes to next if not** - `_next_handler.handle()`

### Code Reference

**File:** `chain_of_responsibility_followed.py`

### Architecture

The Chain of Responsibility Pattern has three main components:

1. **Handler Interface** - Defines handling contract (`SupportHandler`)
2. **Concrete Handlers** - Implement specific handling logic (`Level1Support`, `Level2Support`)
3. **Client** - Initiates request processing

### Class Diagram
```
┌──────────────────────────────────────────┐
│      <<abstract>>                        │
│      SupportHandler                      │
├──────────────────────────────────────────┤
│  - _next_handler: SupportHandler         │
├──────────────────────────────────────────┤
│  + set_next(handler): SupportHandler     │
│  + handle(ticket)                        │
│  # _can_handle(ticket): bool             │
│  # _process(ticket)                      │
└──────────────────────────────────────────┘
                  ▲
                  │ extends
    ┌─────────────┼─────────────┬──────────┬──────────┐
    │             │             │          │          │
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐
│ Level1  │ │ Level2  │ │ Level3  │ │  Mgmt   │ │Level1.5  │
│ Support │ │ Support │ │ Support │ │ Support │ │ Support  │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └──────────┘

Chain Flow:
Level1 → Level2 → Level3 → Management
  │        │        │          │
  ✓ or →   ✓ or →  ✓ or →    ✓ (end)
```

### How It Works
```
1. Client starts chain from first handler
   level1.handle(ticket)

2. Handler checks if it can handle
   if self._can_handle(ticket):
       self._process(ticket)  # Handle it!

3. If can't handle, pass to next
   elif self._next_handler:
       self._next_handler.handle(ticket)  # Pass along chain

4. Chain continues until:
   - Some handler processes it, OR
   - Reaches end of chain (unhandled)

Flow Example:
  LOW ticket → Level1 ✓ handles (stops)
  MEDIUM ticket → Level1 → Level2 ✓ handles (stops)
  HIGH ticket → Level1 → Level2 → Level3 ✓ handles (stops)
  CRITICAL ticket → Level1 → Level2 → Level3 → Management ✓ handles
```

---

## The Pain Point: Chain Building Complexity

### Problem

Even with Chain of Responsibility, **clients must know**:
```python
# Client must know:
# - Which handlers exist
# - How to create them
# - In what order to chain them
# - Different configurations for different scenarios

# Business hours chain
level1 = Level1Support()
level1_5 = Level1_5Support()
level2 = Level2Support()
level3 = Level3Support()
management = ManagementSupport()
level1.set_next(level1_5).set_next(level2).set_next(level3).set_next(management)

# After hours chain
after_hours = ManagementSupport()  # Different chain!

# Weekend chain
weekend_level1 = Level1Support()
weekend_mgmt = ManagementSupport()
weekend_level1.set_next(weekend_mgmt)

# Client must manage all this complexity! 😰
```

**Issues:**
- Client knows too much about handlers
- Must rebuild chains for different scenarios
- Hard to maintain when handlers change
- Error-prone chain building

---

## ✅ Solution: Chain Factory Pattern

### Factory to the Rescue!

We introduce a **Factory** that **encapsulates chain building**:
```python
# Client doesn't need to know anything!
# Just specify the scenario:

system = SupportSystem(ChainType.BUSINESS_HOURS)
system.process_ticket(ticket)

# For different scenario:
system = SupportSystem(ChainType.AFTER_HOURS)
system.process_ticket(ticket)

# That's it! Factory handles all complexity!
```

### Code Reference

**File:** `COR_with_factory.py`

### Architecture with Factory
```
┌──────────────────────────────────────────┐
│        SupportSystem                     │
│         (Client)                         │
├──────────────────────────────────────────┤
│  - chain_type: ChainType                 │
│  - chain: SupportHandler                 │
├──────────────────────────────────────────┤
│  + process_ticket(ticket)                │
│  + switch_chain(chain_type)              │
└──────────────────────────────────────────┘
                  │
                  │ uses
                  ▼
┌──────────────────────────────────────────┐
│    SupportChainFactory                   │
│         (Factory)                        │
├──────────────────────────────────────────┤
│  + create_chain(type): SupportHandler    │
│  + get_available_chains(): List          │
└──────────────────────────────────────────┘
                  │
                  │ creates
                  ▼
        Handler Chain (based on type)
```

### Factory Implementation
```python
class ChainType(Enum):
    BUSINESS_HOURS = "business_hours"
    AFTER_HOURS = "after_hours"
    WEEKEND = "weekend"
    # .... more

class SupportChainFactory:
    """Factory creates pre-configured chains"""
    
    @staticmethod
    def create_chain(chain_type: ChainType):
        if chain_type == ChainType.BUSINESS_HOURS:
            # Full chain: Level1 → Level1.5 → Level2 → Level3 → Mgmt
            level1 = Level1Support()
            # ... build chain
            return level1
        
        elif chain_type == ChainType.AFTER_HOURS:
            # Only management for critical issues
            return ManagementSupport()
        
        elif chain_type == ChainType.WEEKEND:
            # Basic + critical: Level1 → Management
            level1 = Level1Support()
            # ... build chain
            return level1
        
        # ... more configurations
```
---

## ⚠️ New Problem After Factory

Factory improved things, but a new issue appears as the system grows.

**Issues:**
- Factory must know every chain
- Adding a new chain requires modifying factory code
- `if/else` or `switch` keeps growing
- Factory becomes a bottleneck / god object
- Violates Open/Closed Principle

---

## ✅ Solution: Builder + Registry Pattern

### Builders to the Rescue!

We move chain construction **out of the factory**.

Factory no longer builds.  It only **looks up who can build**.

```python
# Client code stays SAME
system = SupportSystem(ChainType.BUSINESS_HOURS)
system.process_ticket(ticket)

But internally: Factory → finds builder → builder builds chain
```

### Code Reference

**File:** `COR_with_factory_builder.py`

### Architecture with Builder + Registry
```
┌──────────────────────────────────────────┐
│              SupportSystem               │
│                (Client)                  │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│           SupportChainFactory            │
│        (Lookup + Delegation only)        │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│               Registry                   │
│    chain_type → ChainBuilder mapping     │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│            Concrete Builder              │
│        (knows how to build chain)        │
└──────────────────────────────────────────┘
                    │
                    ▼
             Handler Chain

```

---
## Comparison: Before vs After

| Aspect | Without CoR ❌ | With CoR ✅ | With CoR + Factory ✅✅ | With CoR + Builder + Registry 🚀 |
|--------|---------------|-------------|------------------------|-----------------------------------|
| **Coupling** | Tight (central knows all) | Loose (handlers independent) | Very loose (client knows nothing) | Minimal (factory knows nothing too) |
| **Add handler** | Modify central system | Add to chain manually | Update factory only | Create builder & register |
| **Chain building** | N/A (no chain) | Client must build | Factory builds | Builder builds |
| **Multiple chains** | Not possible | Manual creation | Pre-configured scenarios | Plug-and-play |
| **Runtime change** | Hard | Possible but manual | Easy with switch_chain() | Easy + extensible |
| **Client complexity** | High (knows all handlers) | Medium (knows chain building) | Low (just scenario) | Lowest (pure abstraction) |
| **Factory growth** | N/A | N/A | Increases with cases | Stable |
| **Ownership** | Central team | Mixed | Factory team | Independent teams |
| **Scalability** | Poor | Moderate | Good | Excellent |

---

## Benefits of Chain of Responsibility Pattern

### 1. **Decouples Sender and Receiver**
Sender doesn't know who handles request.
```python
# Client doesn't know which level handles it
level1.handle(ticket)  # Could be L1, L2, L3, or Mgmt
```

### 2. **Single Responsibility**
Each handler has one job - handle its type of request.
```python
class Level1Support:
    # Only handles LOW severity
    def _can_handle(self, ticket):
        return ticket.severity == SEVERITY_LOW
```

### 3. **Easy to Add/Remove Handlers**
Handlers are independent - add without modifying others.
```python
# Add new handler - no changes to existing handlers!
class Level1_5Support(SupportHandler):
    # New intermediate level
    pass

# Insert into chain
level1.set_next(level1_5).set_next(level2)...
```

### 4. **Flexible Chain Configuration**
Build different chains for different scenarios.
```python
# Business hours: Full chain
level1 → level1.5 → level2 → level3 → management

# After hours: Critical only
management

# Weekend: Basic + critical
level1 → management
```

### 5. **Runtime Chain Modification**
Change chain dynamically.
```python
system.switch_chain(ChainType.AFTER_HOURS)  # Dynamic!
```

### 6. **Open/Closed Principle**
Open for extension, closed for modification.

---

## Benefits of Adding Factory
### 1. **Hides Chain Building Complexity**
Client doesn't need to know how to build chains.
```python
# Before: Client must know everything
level1 = Level1Support()
level2 = Level2Support()
# ... create all handlers
level1.set_next(level2).set_next(...)  # Wire them

# After: Client just specifies scenario
system = SupportSystem(ChainType.BUSINESS_HOURS)  # Done!
```

### 2. **Pre-configured Scenarios**
Common chains pre-built and named.
```python
ChainType.BUSINESS_HOURS  # Full support
ChainType.AFTER_HOURS     # Critical only
ChainType.WEEKEND         # Basic + critical
ChainType.VIP_CUSTOMER    # Premium support
```

### 3. **Centralized Configuration**
All chain logic in one place (Factory).
```python
# Add new handler to ALL chains - change factory only!
# Client code unchanged!
```

### 4. **Easy to Discover Chains**
List available configurations.
```python
chains = SupportChainFactory.get_available_chains()
# Returns all available chain types with descriptions
```

### 5. **Reusability**
Factory caches chains - no rebuilding every time.
```python
# First call: Creates chain
chain1 = factory.create_chain(ChainType.BUSINESS_HOURS)

# Second call: Returns cached chain (if implemented)
chain2 = factory.create_chain(ChainType.BUSINESS_HOURS)
```

---

## Benefits of Adding Builders to Factory

### 1. **Removes Factory Conditionals**
Factory no longer needs `if/else` or `switch` statements.
```python
# Before: Modify factory for every new chain
if type == BUSINESS:
    ...
elif type == WEEKEND:
    ...

# After: Just register a builder
ChainFactory.register(ChainType.WEEKEND, WeekendChainBuilder)
```
### 2. **Open for Extension, Closed for Modification**

New chain → create builder + register. Existing factory code remains untouched.

```python
class HolidayChainBuilder(ChainBuilder):
    def build(self):
        ...

ChainFactory.register(ChainType.HOLIDAY, HolidayChainBuilder)
``` 

---

## Real-World Use Cases

### 1. **Support Ticket Systems**
L1 → L2 → L3 → Management escalation

### 2. **Middleware in Web Frameworks**
Request → Auth → Logging → Validation → Handler

### 3. **Event Bubbling in UI**
Button → Panel → Window → Application (event propagation)

### 4. **Approval Workflows**
Employee → Manager → Director → VP → CEO

### 5. **Exception Handling**
try-catch blocks form a chain of exception handlers

### 6. **Logging Systems**
Debug → Info → Warning → Error → Critical handlers

---

## Implementation Steps

### Step 1: Define Handler Interface
```python
class SupportHandler(ABC):
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler):
        self._next_handler = handler
        return handler  # For chaining
    
    def handle(self, request):
        if self._can_handle(request):
            self._process(request)
        elif self._next_handler:
            self._next_handler.handle(request)
    
    @abstractmethod
    def _can_handle(self, request): pass
    
    @abstractmethod
    def _process(self, request): pass
```

### Step 2: Create Concrete Handlers
```python
class Level1Support(SupportHandler):
    def _can_handle(self, ticket):
        return ticket.severity == SEVERITY_LOW
    
    def _process(self, ticket):
        # Handle LOW severity
```

### Step 3: Build Chain
```python
level1 = Level1Support()
level2 = Level2Support()
level3 = Level3Support()

level1.set_next(level2).set_next(level3)
```

### Step 4: Process Request
```python
level1.handle(ticket)  # Starts chain
```

### Step 5 (Optional): Add Factory


```python
class ChainFactory:
    @staticmethod
    def create_chain(chain_type):
        # Build and return appropriate chain
```

### Step 6 (Optional): Chain Builders

Move chain creation responsibility out of the factory and into dedicated builder classes.


```python
# BUILDER INTERFACE
class ChainBuilder(ABC):
    @abstractmethod
    def build(self) -> SupportHandler:
        pass
```
---

## Trade-Offs

### Advantages ✅

- **Decouples sender and receiver** - No tight coupling
- **Flexible chain building** - Add/remove handlers easily
- **Single Responsibility** - Each handler focused
- **Runtime configuration** - Dynamic chain modification
- **Multiple chains** - Different scenarios, different chains
- **With Factory: Simplified client** - No chain building knowledge needed

### Disadvantages ❌

- **Request might not be handled** - Can fall through chain
- **Hard to debug** - Request flows through multiple handlers
- **Performance overhead** - Traversing chain takes time
- **Guaranteed handling not ensured** - Unless terminal handler exists
- **Without Factory: Client complexity** - Must know chain building

### When to Accept Trade-Offs

**Accept CoR when:**
- Multiple handlers can process request
- Want decoupling between sender and receiver
- Need flexible, dynamic handler configuration
- Order of processing matters

**Avoid CoR when:**
- Only one handler exists
- All requests MUST be handled
- Performance is critical
- Simple if-elif is sufficient

---

## Common Mistakes

### ❌ **Not handling end-of-chain**
```python
# Bad - What if no handler can process?
def handle(self, request):
    if self._can_handle(request):
        self._process(request)
    elif self._next_handler:
        self._next_handler.handle(request)
    # ❌ What if _next_handler is None and can't handle?

# Good - Handle end-of-chain explicitly
def handle(self, request):
    if self._can_handle(request):
        self._process(request)
    elif self._next_handler:
        self._next_handler.handle(request)
    else:
        print("End of chain - unhandled!")  # ✓
```

### ❌ **Handler knowing about multiple next handlers**
```python
# Bad - Handler knows about multiple next handlers
class Handler:
    def __init__(self):
        self.next_for_type_a = HandlerA()  # ❌ Too complex
        self.next_for_type_b = HandlerB()

# Good - Single next handler
class Handler:
    def __init__(self):
        self._next_handler = None  # ✓ Simple chain
```

### ❌ **Circular chains**
```python
# Bad - Creates infinite loop!
handler1.set_next(handler2)
handler2.set_next(handler3)
handler3.set_next(handler1)  # ❌ Circular!

# Good - Linear chain
handler1.set_next(handler2).set_next(handler3)  # ✓ Terminal
```

### ❌ **Handler modifying request while passing**
```python
# Bad - Handler modifies request
def handle(self, ticket):
    ticket.severity = "MODIFIED"  # ❌ Side effect!
    if not self._can_handle(ticket):
        self._next_handler.handle(ticket)

# Good - Handler processes OR passes, doesn't modify
def handle(self, ticket):
    if self._can_handle(ticket):
        self._process(ticket)  # ✓ Process
    else:
        self._next_handler.handle(ticket)  # ✓ Pass unchanged
```

---

## Chain of Responsibility vs Other Patterns

### CoR vs Command Pattern

**Chain of Responsibility:**
- **Purpose:** Pass request along chain until handled
- **Focus:** Finding right handler
- **Example:** Support escalation (L1 → L2 → L3)

**Command:**
- **Purpose:** Encapsulate request as object
- **Focus:** Decoupling invoker from action
- **Example:** Remote control buttons execute commands

### CoR vs Decorator Pattern

**Chain of Responsibility:**
- **Purpose:** One handler processes request
- **Flow:** Request stops when handled
- **Example:** Only one support level handles ticket

**Decorator:**
- **Purpose:** All decorators add to request
- **Flow:** Request flows through ALL decorators
- **Example:** Coffee gets milk + sugar + cream (all layers)

### CoR vs Strategy Pattern

**Chain of Responsibility:**
- **Purpose:** Multiple handlers, one processes
- **Selection:** Automatic based on conditions
- **Example:** Chain decides which handler

**Strategy:**
- **Purpose:** Choose algorithm explicitly
- **Selection:** Client selects strategy
- **Example:** Client chooses payment method

---

## Conclusion

The Chain of Responsibility Pattern is essential for building flexible request handling systems. It provides:

- Decoupling between sender and receiver
- Dynamic handler configuration
- Easy addition/removal of handlers
- Clean, maintainable code

**With Factory addition**, it becomes even more powerful:
- Hides chain building complexity
- Pre-configured scenarios
- Client only needs to know scenario name
- Centralized chain management

**With Builder addition**, it becomes more flexible:

Use Chain of Responsibility when you have multiple objects that can handle a request, and you want to give more than one object a chance to handle it. The addition of a Factory pattern makes it production-ready by hiding complexity from clients!

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** February 2026