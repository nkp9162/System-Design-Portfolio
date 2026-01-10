# Observer Design Pattern — Python

## Overview

The **Observer Pattern** is a behavioral design pattern that:

> Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

In simple terms:
- **Subject (Observable)** - Object being watched
- **Observers** - Objects that watch and react to changes
- When subject changes, all observers are automatically notified

**Also known as:** Publish-Subscribe Pattern, Event-Listener Pattern

---

## Real-World Analogy

### Newspaper Subscription

Think of how **newspaper subscriptions** work:

- **Publisher (Subject)** - Newspaper company
- **Subscribers (Observers)** - People who subscribe

**How it works:**
1. People subscribe to the newspaper
2. When new edition is published, all subscribers get it automatically
3. Subscribers can unsubscribe anytime
4. Publisher doesn't need to know who subscribers are, just that they exist
5. New subscribers can join anytime without publisher changing anything

### YouTube Channel

Another analogy is **YouTube subscriptions**:

- **Channel (Subject)** - YouTuber's channel
- **Subscribers (Observers)** - People who subscribed

When YouTuber uploads a new video (state change), all subscribers get a notification automatically. Subscribers can subscribe/unsubscribe anytime.

---

## Problem Statement

We're building a **Weather Monitoring System** that:

- Receives weather data from sensors (temperature, humidity, pressure)
- Displays data on multiple devices (phones, TVs, websites, windows)
- Needs to support dynamic addition/removal of displays
- Different displays show data differently
- Some displays calculate statistics, some show alerts

**Challenges:**
1. How to notify all displays when weather changes?
2. How to add new displays without modifying core system?
3. How to avoid tight coupling between weather station and displays?

---

## ❌ Without Observer Pattern

### Description

Without Observer Pattern, the subject (WeatherStation) **directly manages and calls** all observers:
```python
class WeatherStation:
    def __init__(self):
        self.phone_display = None
        self.tv_display = None
        self.window_display = None
    
    def set_measurements(self, temp, humidity, pressure):
        # Directly call each display
        if self.phone_display:
            self.phone_display.update(temp, humidity, pressure)
        if self.tv_display:
            self.tv_display.update(temp, humidity, pressure)
        # ... manually update each display
```

### Code Reference

**File:** `observer_violated.py`

### Problems with this approach:

- **Tight coupling** - WeatherStation knows about all concrete display classes
- **Violates OCP** - Must modify WeatherStation to add new displays
- **No dynamic add/remove** - Cannot change displays at runtime
- **Hard to maintain** - Adding display requires code changes in multiple places
- **Violates SRP** - WeatherStation handles both weather data and display management
- **No flexibility** - All displays are always notified

### Diagram: Without Observer Pattern
```
┌─────────────────────────────────────────┐
│       WeatherStation                    │
│  (Tightly coupled to all displays)      │
├─────────────────────────────────────────┤
│  - phone_display: PhoneDisplay          │
│  - tv_display: TVDisplay                │
│  - window_display: WindowDisplay        │
├─────────────────────────────────────────┤
│  set_measurements():                    │
│    phone_display.update(...)            │
│    tv_display.update(...)               │
│    window_display.update(...)           │
└─────────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Phone   │ │   TV    │ │ Window  │
    │ Display │ │ Display │ │ Display │
    └─────────┘ └─────────┘ └─────────┘

Problem: WeatherStation must know about every display!
Adding new display = Modifying WeatherStation!
```

---

## ✅ With Observer Pattern

### Description

With Observer Pattern, we:

1. **Define Observer interface** - Common interface for all observers
2. **Define Subject interface** - Interface for managing observers
3. **Implement concrete subject** - WeatherStation maintains observer list
4. **Implement concrete observers** - Each display implements Observer interface
5. **Automatic notification** - Subject notifies all observers when state changes

### Code Reference

**File:** `observer_followed.py`

### Architecture

The Observer Pattern has four main components:

1. **Subject Interface** - Defines methods to attach, detach, and notify observers
2. **Concrete Subject** - Implements Subject interface, maintains state, notifies observers
3. **Observer Interface** - Defines update method that subjects call
4. **Concrete Observers** - Implement Observer interface to receive updates

### Class Diagram
```
┌──────────────────────────────────────────┐
│      <<interface>>                       │
│         Subject                          │
├──────────────────────────────────────────┤
│  + register_observer(observer)           │
│  + remove_observer(observer)             │
│  + notify_observers()                    │
└──────────────────────────────────────────┘
                  ▲
                  │ implements
                  │
┌──────────────────────────────────────────┐
│       WeatherStation                     │
│    (Concrete Subject)                    │
├──────────────────────────────────────────┤
│  - observers: List[Observer]             │
│  - temperature: float                    │
│  - humidity: float                       │
│  - pressure: float                       │
├──────────────────────────────────────────┤
│  + set_measurements(t, h, p)             │
│  + notify_observers()                    │
└──────────────────────────────────────────┘
                  │
                  │ notifies
                  ▼
┌──────────────────────────────────────────┐
│      <<interface>>                       │
│         Observer                         │
├──────────────────────────────────────────┤
│  + update(temperature, humidity,         │
│           pressure)                      │
└──────────────────────────────────────────┘
                  ▲
                  │ implements
    ┌─────────────┼─────────────┬──────────┬──────────┐
    │             │             │          │          │
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ ┌────────┐
│ Phone   │ │   TV    │ │ Website │ │ Stats  │ │ Alerts │
│ Display │ │ Display │ │ Display │ │Display │ │ System │
└─────────┘ └─────────┘ └─────────┘ └────────┘ └────────┘
```

### How It Works
```
1. Observers register with Subject
   weather_station.register_observer(phone_display)
   weather_station.register_observer(tv_display)

2. Subject's state changes
   weather_station.set_measurements(25, 65, 1013)

3. Subject notifies all observers
   for observer in observers:
       observer.update(temperature, humidity, pressure)

4. Each observer receives update and reacts
   phone_display.update(25, 65, 1013)  → Updates phone UI
   tv_display.update(25, 65, 1013)     → Updates TV UI
```

---

## Comparison: Before vs After

| Aspect | Without Observer ❌ | With Observer ✅ |
|--------|-------------------|-----------------|
| **Coupling** | Tight (subject knows all observers) | Loose (subject knows Observer interface) |
| **Adding observers** | Modify subject class | Just register new observer |
| **Removing observers** | Modify subject class | Just call remove_observer() |
| **Dynamic changes** | Cannot add/remove at runtime | Can add/remove anytime |
| **OCP** | Violates (modify for new observers) | Follows (add observers without changes) |
| **Flexibility** | All observers always notified | Can selectively add/remove |
| **Testing** | Hard to test in isolation | Easy to test with mock observers |

---

## Benefits of Observer Pattern

### 1. **Loose Coupling**
Subject doesn't need to know concrete observer classes, only that they implement Observer interface.
```python
# Subject doesn't know about PhoneDisplay, TVDisplay, etc.
# It only knows about Observer interface
def notify_observers(self):
    for observer in self._observers:
        observer.update(...)  # Calls Observer interface method
```

### 2. **Dynamic Relationships**
Add and remove observers at runtime without modifying subject.
```python
# Add observer at runtime
weather_station.register_observer(new_display)

# Remove observer at runtime
weather_station.remove_observer(old_display)
```

### 3. **Broadcast Communication**
One subject can notify unlimited observers (one-to-many relationship).

### 4. **Open/Closed Principle**
Add new observer types without modifying subject.
```python
# Add new observer - no changes to WeatherStation!
class EmailAlert(Observer):
    def update(self, temp, humidity, pressure):
        # Send email when temp > 35
```

### 5. **Reusability**
Observers can observe multiple subjects, subjects can have multiple observers.

### 6. **Easy Testing**
Mock observers for testing subject, mock subject for testing observers.
```python
class MockObserver(Observer):
    def __init__(self):
        self.update_count = 0
    
    def update(self, temp, humidity, pressure):
        self.update_count += 1

# Test that subject notifies observers
weather_station.register_observer(mock)
weather_station.set_measurements(25, 65, 1013)
assert mock.update_count == 1
```

---

## Push vs Pull Model

### Push Model (Used in our example)
Subject **pushes** all data to observers in update method.
```python
def update(self, temperature, humidity, pressure):
    # Observer receives all data
    print(f"Temp: {temperature}")
```

**Pros:** Simple, observers get all data immediately  
**Cons:** Inefficient if observers only need some data

### Pull Model
Subject notifies observers, observers **pull** data they need.
```python
class Observer(ABC):
    @abstractmethod
    def update(self, subject): pass  # Receives subject reference

class PhoneDisplay(Observer):
    def update(self, subject):
        # Pull only needed data
        temp = subject.get_temperature()
        print(f"Temp: {temp}")
```

**Pros:** Efficient, observers get only what they need  
**Cons:** Observers need subject reference

---

## When to Use Observer Pattern

### Use Observer Pattern when:

✅ Change in one object requires changing unknown number of others  
✅ Object should notify others without knowing who they are  
✅ Need broadcast communication (one-to-many)  
✅ Want to decouple objects (loose coupling)  
✅ Need dynamic relationships (add/remove at runtime)  

### Don't use when:

❌ Only one or two objects need notification  
❌ Relationships are fixed and won't change  
❌ Performance is critical (observer notification has overhead)  
❌ Simple event handling is sufficient  

---

## Real-World Use Cases

### 1. **Event Systems**
GUI frameworks (button clicks notify multiple listeners)

### 2. **Social Media**
Followers get notified when you post (Twitter, Instagram)

### 3. **Stock Market**
Stock price changes notify all traders/analysts

### 4. **News Feeds**
RSS feeds notify subscribers of new articles

### 5. **Model-View-Controller (MVC)**
Model (subject) notifies views (observers) when data changes

### 6. **Reactive Programming**
RxJS, React hooks - observers subscribe to state changes

---

## Implementation Best Practices

### 1. **Avoid Memory Leaks**
Always unregister observers when they're no longer needed.
```python
# Good
display.cleanup()
weather_station.remove_observer(display)

# Bad - observer stays in memory even if unused
```

### 2. **Prevent Notification Loops**
Observer shouldn't modify subject during update, causing infinite loop.
```python
# Bad - can cause infinite loop
def update(self, temp, humidity, pressure):
    if temp > 30:
        subject.set_measurements(25, 60, 1013)  # DON'T DO THIS!
```

### 3. **Order Independence**
Don't rely on notification order - observers should be independent.

### 4. **Thread Safety**
If using threads, protect observer list with locks.
```python
import threading

class WeatherStation(Subject):
    def __init__(self):
        self._observers = []
        self._lock = threading.Lock()
    
    def register_observer(self, observer):
        with self._lock:
            self._observers.append(observer)
```

---

## Key Takeaways

1. **One-to-many dependency** - One subject, many observers
2. **Automatic notification** - Observers updated automatically
3. **Loose coupling** - Subject and observers are independent
4. **Dynamic relationships** - Add/remove observers at runtime
5. **Broadcast communication** - All observers get notified
6. **Follows OCP** - Add observers without modifying subject

---

## Common Variations

### 1. **Event Aggregator**
Central event bus that manages all events and subscriptions.

### 2. **Weak References**
Use weak references to prevent memory leaks when observers aren't explicitly removed.

### 3. **Filtered Observers**
Observers can specify conditions for receiving notifications.
```python
class ConditionalObserver(Observer):
    def should_update(self, temp):
        return temp > 30  # Only update if temp > 30
```

---

## Related Patterns

- **Mediator Pattern** - Similar but with central mediator instead of direct observer-subject relationship
- **Singleton Pattern** - Often used for event managers in observer systems
- **Command Pattern** - Can be used to encapsulate observer notifications
- **State Pattern** - State changes can notify observers

---

## Conclusion

The Observer Pattern is fundamental to event-driven programming and reactive systems. It enables:

- Loose coupling between components
- Dynamic, flexible relationships
- Easy addition of new functionality
- Scalable, maintainable systems

Use Observer Pattern whenever you need one object to notify multiple others about state changes, and you want to keep them decoupled and independently testable.

---
**Repository:** [System Design Portfolio](https://github.com/nkp9162/System-Design-Portfolio)

**Author:** Nirbhay Pratihast

**Last Updated:** January 2026