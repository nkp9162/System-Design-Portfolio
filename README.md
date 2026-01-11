# 🎯 System Design Portfolio

> A curated **system design portfolio** covering **Low-Level Design (LLD)**, **High-Level Design (HLD)**, and **real-world project implementations**.  
This repository focuses on **design thinking**, **SOLID principles**, **design patterns**, and **scalable architecture decisions**.
The goal of this repo is to demonstrate *how and why* design decisions are made in real systems.

---

## 📚 Repository Structure
```
system-design-portfolio/
├── LLD/                         # Low-Level Design
│   ├── SOLID/                   # SOLID Principles (Foundations)
│   │
│   ├── design-patterns/         # Gang of Four Design Patterns (23)
│   │   ├── creational/
│   │   ├── structural/
│   │   └── behavioral/
│   │
│   └── lld-practice/            # LLD Problems & case studies
│       ├── parking_lot/
│       ├── elevator_system/
│       ├── payment_gateway/
│       └── ...
│
├── HLD/                         # High-Level Design (Planned)
│   ├── concepts/
│   ├── case-studies/
│   └── diagrams/
│
└── Projects/                    # End-to-end real-world implementations
    ├── scalable_services/
    ├── system_simulations/
    └── ...

```
---

# 🔥 What’s Inside

## 📐 Low-Level Design (LLD)
**Status:** ✅ Active

The LLD section focuses on building strong software design foundations.  
It follows a clear progression:

> **Principles → Patterns → Real interview-level problems**

This helps understand not just *how* to design systems, but *why* certain design choices are made.

---

## 🧱 SOLID Principles (Foundations)

This section explains **SOLID principles from the ground up**, with a strong focus on **why** and **when** to apply them.

Each principle includes:

- Clear problem statement (what goes wrong without the principle)
- `*_violated.py` example (bad or rigid design)
- `*_followed.py` example (refactored, cleaner design)
- `README.md` covering:
  - Simple explanation
  - Trade-offs
  - When **not** to apply the principle
  - Interview-oriented insights

**Example:**  
`SRP/` demonstrates how multiple responsibilities reduce maintainability and how to refactor safely using Single Responsibility Principle.

[➡️ Explore SOLID Principles](LLD/SOLID/)

### Design Patterns (GoF)

Each pattern includes:
- Problem statement (why the pattern is needed)
- Implementation **with and without** the pattern
- UML / class diagrams
- Trade-offs and limitations
- When **not** to use the pattern
- Relation to SOLID principles (where applicable)
The goal is to understand patterns as **tools**, not rules.

**Categories covered:**

- **Creational (5)**  
  Singleton, Factory, Abstract Factory, Builder, Prototype

- **Structural (7)**  
  Adapter, Decorator, Proxy, Facade, Composite, Bridge, Flyweight

- **Behavioral (11)**  
  Strategy, Observer, Command, State, Chain of Responsibility, Iterator,  
  Template Method, Mediator, Memento, Visitor, Interpreter

[➡️ Explore Design Patterns](LLD/design-patterns/)

### LLD Case Studies (Real-World Problems)

A collection of commonly asked **LLD interview problems**, each solved with:
- Clear requirements (functional & non-functional)
- Entity modeling
- Applied design patterns & SOLID principles
- Class & sequence diagrams
- Design trade-offs and future improvements

**Problems included:**

1. Parking Lot System  
2. Library Management System  
3. Elevator System  
4. Hotel Management System  
5. Splitwise (Expense Sharing)  
6. Snake and Ladder Game  
7. Tic-Tac-Toe  
8. Chess Game  
9. ATM System  
10. Movie Ticket Booking System  
11. Online Shopping Cart  
12. LRU Cache Implementation  

[➡️ Explore LLD Problems](LLD/lld-practice/)

---

### 🌐 High-Level Design (HLD)
**Status:** 🚧 Coming Soon

This section will focus on **scalable system design**, including:
- Traffic estimation & capacity planning
- API design
- Database selection & data modeling
- Caching strategies
- Bottlenecks and failure handling
- Trade-off analysis

**Planned systems:**
- URL Shortener
- Twitter / X
- Netflix
- WhatsApp
- Uber

➡️ **Explore:** `HLD/`

---

### 💼 Real-World Projects
**Status:** 🚧 Coming Soon

End-to-end projects demonstrating:
- Practical use of design patterns
- Layered architecture
- Clean, maintainable code
- Design documentation alongside implementation
- Performance and scalability considerations

➡️ **Location:** `Projects/`

---

## 🛠️ Tech Stack & Tools
- **Programming Language:** Python 3.11+
- **Design & Diagrams:** Draw.io, PlantUML
- **Documentation:** Markdown
- **Version Control:** Git & GitHub

---

## Skills Demonstrated

- SOLID Principles
- Object-Oriented Design
- Design Patterns (GoF)
- Low-Level & High-Level System Design
- UML (Class & Sequence Diagrams)
- Clean Code & Maintainable Architecture
- Trade-off & scalability thinking

## 📖 How to Navigate

Each design or project typically contains:
- `README.md` → High-level overview
- `DESIGN.md` → Detailed design decisions & trade-offs
- `diagrams/` → UML and architecture diagrams
- `src/` → Clean, runnable code

---

## 🚀 Quick Start
```bash
# Clone the repository
git clone https://github.com/nkp9162/System-Design-Portfolio.git

# Navigate to a specific LLD problem
cd system-design-portfolio/LLD/lld-practice/01-parking-lot-system

# Run the example
python src/main.py
```
---

## About the Author

**Nirbhay Pratihast**  
Software Engineer | System Design Enthusiast

- **LinkedIn:** [Nirbhay Pratihast](https://www.linkedin.com/in/nirbhay-pratihast-is-ready/)
- **Email:** nkp9162@gmail.com


---

## 📝 License
This project is licensed under the [MIT License](LICENSE).

---

**⭐ Star this repo if you find it helpful!**