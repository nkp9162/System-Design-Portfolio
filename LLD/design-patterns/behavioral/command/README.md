# Command Design Pattern — Python

## Overview

The **Command Pattern** is a behavioral design pattern that:

> Encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

In simple terms:
- **Turns requests into objects** - Commands are first-class objects
- **Decouples sender from receiver** - Invoker doesn't know about receiver
- **Enables undo/redo** - Commands know how to reverse themselves
- **Supports queuing and logging** - Commands can be stored and executed later

---

## Real-World Analogy

### Restaurant Order System

Think of ordering food at a **restaurant**:

**Without Command Pattern:**
- Customer tells waiter: "Make me pasta with tomato sauce"
- Waiter goes to kitchen and cooks the pasta themselves
- No record of order
- Cannot cancel or modify order
- Waiter must know how to cook everything

**With Command Pattern:**
- Customer places **order** (command object)
- Order ticket written with details
- Waiter (invoker) takes order to kitchen
- Chef (receiver) prepares the food
- Order can be cancelled, modified, or repeated
- Kitchen queue manages multiple orders

The **order slip is the command** - it encapsulates the request!

### TV Remote Control

Another example is a **universal remote control**:

- **Button press** creates a command object
- Remote doesn't know what TV, AC, or lights do
- Each button can be programmed with any command
- Macro buttons execute multiple commands
- Some remotes have undo button

The remote is **decoupled** from devices - it just executes commands!

---

## Problem Statement

We're building a **Smart Home Remote Control System** that needs to:

- Control multiple devices (lights, fans, AC, TV)
- Support undo/redo operations
- Create macros (movie mode, good night mode)
- Log command history
- Queue and schedule commands

**Challenges:**

**Without Command Pattern:**
- Remote tightly coupled to all device types
- Massive if-elif chains for each device
- String-based operation names (error-prone)
- Complex undo logic that doesn't work well
- Cannot queue or schedule operations
- Cannot create macros

---

## ❌ Without Command Pattern

### Description

Without Command Pattern, the remote **directly controls devices** using if-elif chains:
```python
def execute_operation(self, device_name, operation, *args):
    device = self.devices[device_name]
    
    if isinstance(device, Light):
        if operation == "on":
            device.turn_on()
        elif operation == "off":
            device.turn_off()
    
    elif isinstance(device, Fan):
        if operation == "on":
            device.turn_on(args[0])
        elif operation == "off":
            device.turn_off()
        # ... more conditions
    
    # ... more device types
```

Undo is manual and fragile:
```python
def undo(self):
    # Must manually track and reverse state
    # Doesn't work well for complex operations
```

### Code Reference

**File:** `command_violated.py`

### Problems with this approach:

- **Tight coupling** - Remote knows about all device types
- **if-elif chains** - One for each device type
- **String-based operations** - Typos cause runtime errors
- **Complex undo** - Manual state tracking is fragile
- **No queuing** - Cannot queue or schedule commands
- **No macros** - Cannot combine multiple operations
- **No history** - Cannot log what was executed
- **Hard to extend** - Adding device requires modifying remote

### Diagram: Without Command Pattern
```
┌──────────────────────────────────────────┐
│        RemoteControl                     │
│    (Tightly coupled to devices)          │
├──────────────────────────────────────────┤
│  execute_operation(device, op, args):    │
│    if isinstance(device, Light):         │
│        if op == "on": device.turn_on()   │
│        elif op == "off": ...             │
│    elif isinstance(device, Fan):         │
│        if op == "on": ...                │
│        elif op == "off": ...             │
│    elif isinstance(device, AC):          │
│        ...                               │
└──────────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │ Light  │ │  Fan   │ │   AC   │
    └────────┘ └────────┘ └────────┘

Remote must know about ALL devices!
Massive if-elif chains!
```

---

## ✅ With Command Pattern

### Description

With Command Pattern, we **encapsulate requests as command objects**:
```python
# Create command objects
light_on = LightOnCommand(living_room_light)
fan_on = FanOnCommand(living_room_fan, speed=4)
ac_temp = ACTemperatureCommand(bedroom_ac, 22)

# Remote just executes commands
remote.execute_command(light_on)
remote.execute_command(fan_on)
remote.execute_command(ac_temp)

# Undo is automatic
remote.undo()
```

Commands are objects that can be:
- Stored in variables
- Passed as parameters
- Queued for later execution
- Logged to history
- Combined into macros

### Code Reference

**File:** `command_followed.py`

### Architecture

The Command Pattern has four main components:

1. **Command Interface** - Defines execute() and undo() (`Command`)
2. **Concrete Commands** - Implement specific operations (`LightOnCommand`, `FanOnCommand`)
3. **Receiver** - Knows how to perform operations (`Light`, `Fan`, `AC`)
4. **Invoker** - Asks command to execute (`RemoteControl`)

### Class Diagram
```
┌──────────────────────────────────────────┐
│        RemoteControl                     │
│         (Invoker)                        │
├──────────────────────────────────────────┤
│  - command_history: List[Command]        │
│  - undo_history: List[Command]           │
├──────────────────────────────────────────┤
│  + execute_command(cmd: Command)         │
│  + undo()                                │
│  + redo()                                │
│  + show_history()                        │
└──────────────────────────────────────────┘
                  │
                  │ uses
                  ▼
┌──────────────────────────────────────────┐
│      <<interface>>                       │
│         Command                          │
├──────────────────────────────────────────┤
│  + execute()                             │
│  + undo()                                │
└──────────────────────────────────────────┘
                  ▲
                  │ implements
    ┌─────────────┼──────────┬────────────┬────────────┐
    │             │          │            │            │
┌─────────┐ ┌──────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐
│LightOn  │ │ FanOn    │ │ ACTemp │ │TVVolume │ │  Macro   │
│Command  │ │ Command  │ │Command │ │ Command │ │ Command  │
└─────────┘ └──────────┘ └────────┘ └─────────┘ └──────────┘
    │             │          │            │
    │ uses        │ uses     │ uses       │ uses
    ▼             ▼          ▼            ▼
┌────────┐   ┌────────┐ ┌────────┐   ┌────────┐
│ Light  │   │  Fan   │ │   AC   │   │   TV   │
│        │   │        │ │        │   │        │ 
└────────┘   └────────┘ └────────┘   └────────┘
                   (Receivers) 
                   
Invoker decoupled from Receivers!
Commands encapsulate requests!
```

### How It Works
```
1. Client creates command with receiver
   light_on = LightOnCommand(living_room_light)

2. Client passes command to invoker
   remote.execute_command(light_on)

3. Invoker executes command
   def execute_command(self, command):
       command.execute()
       self.command_history.append(command)

4. Command calls receiver method
   def execute(self):
       self.light.turn_on()

5. Undo reverses the operation
   def undo(self):
       self.light.turn_off()
```

---

## Comparison: Before vs After

| Aspect | Without Command ❌ | With Command ✅ |
|--------|-------------------|-----------------|
| **Coupling** | Remote knows all devices | Remote only knows Command interface |
| **Operations** | String-based ("on", "off") | Type-safe command objects |
| **Undo/Redo** | Manual, fragile state tracking | Automatic, each command undoes itself |
| **Macros** | Not possible | Easy with MacroCommand |
| **Queuing** | Not possible | Commands are objects, can queue |
| **History** | Not tracked | Automatic history tracking |
| **Extensibility** | Modify remote for new devices | Just create new command class |

---

## Benefits of Command Pattern

### 1. **Decouples Invoker from Receiver**
Remote doesn't need to know about device implementations.
```python
# Remote doesn't know what Light is
remote.execute_command(LightOnCommand(light))

# Works the same for any command
remote.execute_command(FanOnCommand(fan))
remote.execute_command(ACOnCommand(ac))
```

### 2. **Commands are Objects**
Can be stored, passed around, and manipulated.
```python
# Store commands
commands = [
    LightOnCommand(light),
    FanOnCommand(fan),
    ACOnCommand(ac)
]

# Execute later
for cmd in commands:
    remote.execute_command(cmd)
```

### 3. **Easy Undo/Redo**
Each command knows how to undo itself.
```python
class LightOnCommand:
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()  # Simple!
```

### 4. **Macro Commands**
Combine multiple commands into one.
```python
movie_mode = MacroCommand([
    LightOffCommand(light),
    TVOnCommand(tv),
    ACOnCommand(ac)
])

remote.execute_command(movie_mode)
remote.undo()  # Undoes all three!
```

### 5. **Command History**
Automatically track what was executed.
```python
remote.show_history()
# Output:
# 1. LightOnCommand
# 2. FanOnCommand
# 3. ACTemperatureCommand
```

### 6. **Queueing and Scheduling**
Commands can be queued for later execution.
```python
# Queue commands
command_queue = Queue()
command_queue.put(LightOnCommand(light))
command_queue.put(FanOnCommand(fan))

# Execute when ready
while not command_queue.empty():
    cmd = command_queue.get()
    remote.execute_command(cmd)
```

---

## Real-World Use Cases

### 1. **GUI Actions**
Menu items, toolbar buttons, keyboard shortcuts all use commands

### 2. **Undo/Redo Systems**
Text editors, graphics applications, IDEs

### 3. **Transaction Systems**
Database transactions, financial operations

### 4. **Job Queues**
Background tasks, scheduled jobs, worker pools

### 5. **Remote Controls**
Universal remotes, smart home systems

### 6. **Game Input**
Player actions that can be replayed or undone

---

## Implementation Steps

### Step 1: Define Command Interface
```python
class Command(ABC):
    @abstractmethod
    def execute(self): pass
    
    @abstractmethod
    def undo(self): pass
```

### Step 2: Create Concrete Commands
```python
class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()
```

### Step 3: Create Invoker
```python
class RemoteControl:
    def __init__(self):
        self.history = []
    
    def execute_command(self, command):
        command.execute()
        self.history.append(command)
    
    def undo(self):
        command = self.history.pop()
        command.undo()
```

### Step 4: Use Commands
```python
light = Light("Living Room")
light_on = LightOnCommand(light)
remote = RemoteControl()
remote.execute_command(light_on)
```

---

## Trade-Offs

### Advantages ✅

- **Decouples invoker and receiver** - No tight coupling
- **Supports undo/redo** - Each command knows how to reverse
- **Commands are first-class objects** - Can store, queue, log
- **Easy to add new commands** - Just create new command class
- **Macro commands** - Combine multiple operations
- **Transactional support** - Can implement commit/rollback

### Disadvantages ❌

- **More classes** - One class per command type
- **Code verbosity** - Simple operations need command classes
- **Memory overhead** - Command objects and history storage
- **Complexity for simple cases** - Overkill if just calling methods

### When to Accept Trade-Offs

**Accept the overhead when:**
- Need undo/redo functionality
- Need to queue or schedule operations
- Want to log command history
- Building macro/scripting capability
- Decoupling invoker from receiver is important

**Avoid command pattern when:**
- Just need simple method calls
- No undo, queuing, or logging required
- Performance critical (command object creation overhead)
- Team unfamiliar with pattern (unless teaching)

---

## Common Mistakes

### ❌ **Commands with business logic**
```python
# Bad - Command contains business logic
class TransferMoneyCommand:
    def execute(self):
        if self.from_account.balance < self.amount:
            raise InsufficientFunds()  # ❌ Business logic in command
        self.from_account.withdraw(self.amount)
        self.to_account.deposit(self.amount)

# Good - Command delegates to receiver
class TransferMoneyCommand:
    def execute(self):
        self.bank.transfer(self.from_account, self.to_account, self.amount)
```

### ❌ **Not implementing undo properly**
```python
# Bad - Undo doesn't restore state
class FanSpeedCommand:
    def execute(self):
        self.fan.set_speed(5)
    
    def undo(self):
        self.fan.set_speed(0)  # ❌ Assumes fan was off, but it might have been at speed 3!

# Good - Save previous state
class FanSpeedCommand:
    def execute(self):
        self.previous_speed = self.fan.speed
        self.fan.set_speed(self.new_speed)
    
    def undo(self):
        self.fan.set_speed(self.previous_speed)  # ✓ Restores actual previous state
```

### ❌ **Invoker knowing about concrete commands**
```python
# Bad - Invoker depends on concrete commands
class RemoteControl:
    def turn_on_light(self):
        cmd = LightOnCommand(self.light)  # ❌ Invoker creates command
        cmd.execute()

# Good - Client creates and passes command
class RemoteControl:
    def execute_command(self, command: Command):
        command.execute()  # ✓ Invoker only knows Command interface

# Client code
remote = RemoteControl()
remote.execute_command(LightOnCommand(light))
```

### ❌ **Forgetting to clear redo history**
```python
# Bad - Redo history not cleared
def execute_command(self, command):
    command.execute()
    self.history.append(command)
    # ❌ Forgot to clear redo_history

# Good - Clear redo on new command
def execute_command(self, command):
    command.execute()
    self.history.append(command)
    self.redo_history.clear()  # ✓ New command invalidates redo
```

---

## Command vs Strategy vs State

These patterns look similar but serve different purposes:

### Command Pattern
- **Purpose:** Encapsulate request as object
- **Focus:** Decoupling invoker from receiver
- **Example:** Remote control button executes command

### Strategy Pattern
- **Purpose:** Choose algorithm at runtime
- **Focus:** Interchangeable algorithms
- **Example:** Choose payment method (Credit, PayPal)

### State Pattern
- **Purpose:** Change behavior based on state
- **Focus:** State-dependent behavior
- **Example:** Vending machine behaves differently based on state
```python
# Command - Request as object
remote.execute_command(LightOnCommand(light))

# Strategy - Choose algorithm
processor = PaymentProcessor(StripeStrategy())

# State - Behavior changes with state
vending_machine.insert_money(50)  # Behavior depends on current state
```

---

## Conclusion

The Command Pattern is essential for building flexible, extensible systems with undo/redo capabilities. It provides:

- Decoupling between invoker and receiver
- First-class command objects that can be stored and manipulated
- Automatic undo/redo support
- Easy macro creation and command composition
- Command history and logging

Use Command Pattern when you need to parameterize objects with operations, support undo/redo, or queue/log requests. It's particularly valuable in GUI applications, remote controls, transaction systems, and any system requiring operation history.

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026