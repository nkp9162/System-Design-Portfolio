from abc import ABC, abstractmethod

class SupportTicket:

    SEVERITY_LOW = "LOW"
    SEVERITY_MEDIUM = "MEDIUM"
    SEVERITY_HIGH = "HIGH"
    SEVERITY_CRITICAL = "CRITICAL"

    def __init__(self, ticket_id, severity, description):
        self.ticket_id = ticket_id
        self.severity = severity
        self.description = description
        self.assigned_to = None
        self.resolved = False

    def __str__(self):
        return f"Ticket #{self.ticket_id} [{self.severity}]: {self.description}"


# HANDLER BASE
class SupportHandler(ABC):
    """Base handler in the chain."""

    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, ticket):
        if self._can_handle(ticket):
            self._process(ticket)
        elif self._next_handler:
            print(f"{self.__class__.__name__} forwarding request")
            self._next_handler.handle(ticket)
        else:
            print(f"{self.__class__.__name__}: end of chain, unhandled")
            ticket.resolved = False

    @abstractmethod
    def _can_handle(self, ticket):
        pass

    @abstractmethod
    def _process(self, ticket):
        pass

# CONCRETE HANDLERS

class Level1Support(SupportHandler):
    """Handles low severity."""

    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_LOW

    def _process(self, ticket):
        print(f"Level 1 handling: {ticket}")
        ticket.assigned_to = "Level 1 Support"
        ticket.resolved = True


class Level2Support(SupportHandler):
    """Handles medium severity."""

    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_MEDIUM

    def _process(self, ticket):
        print(f"Level 2 handling: {ticket}")
        ticket.assigned_to = "Level 2 Support"
        ticket.resolved = True


class Level3Support(SupportHandler):
    """Handles high severity."""

    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_HIGH

    def _process(self, ticket):
        print(f"Level 3 handling: {ticket}")
        ticket.assigned_to = "Level 3 Support"
        ticket.resolved = True


class ManagementSupport(SupportHandler):
    """Handles critical severity."""

    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_CRITICAL

    def _process(self, ticket):
        print(f"Management handling: {ticket}")
        ticket.assigned_to = "Management"
        ticket.resolved = True


# USAGE
print("=" * 70)
print("CHAIN OF RESPONSIBILITY")
print("=" * 70)

# build chain
level1 = Level1Support()
level2 = Level2Support()
level3 = Level3Support()
management = ManagementSupport()

level1.set_next(level2).set_next(level3).set_next(management)

tickets = [
    SupportTicket(1, SupportTicket.SEVERITY_LOW, "Password reset"),
    SupportTicket(2, SupportTicket.SEVERITY_MEDIUM, "Software installation issue"),
    SupportTicket(3, SupportTicket.SEVERITY_HIGH, "Server performance degradation"),
    SupportTicket(4, SupportTicket.SEVERITY_CRITICAL, "Complete system outage"),
]

for ticket in tickets:
    print(f"\n{'=' * 60}")
    print(f"Processing: {ticket}")
    print(f"{'=' * 60}")

    level1.handle(ticket)

    if ticket.resolved:
        print(f"RESOLVED BY: {ticket.assigned_to}")
    else:
        print("UNRESOLVED")


# if you Want to add new level of support
class Level1_5Support(SupportHandler):

    def _can_handle(self, ticket):
        return "escalated" in ticket.description.lower()

    def _process(self, ticket):
        print(f"Level 1.5 handling: {ticket}")
        ticket.assigned_to = "Level 1.5 Support"
        ticket.resolved = True


print("\n" + "=" * 70)
print("ADDING NEW HANDLER")
print("=" * 70)

level1_5 = Level1_5Support()
level1.set_next(level1_5).set_next(level2).set_next(level3).set_next(management)

ticket = SupportTicket(5, SupportTicket.SEVERITY_LOW, "Escalated password issue")

print(f"\n{'=' * 60}")
print(f"Processing: {ticket}")
print(f"{'=' * 60}")

level1.handle(ticket)


# Want to decorate existing handler with logging with decorator pattern
class LoggingHandler(SupportHandler):

    def __init__(self, handler):
        super().__init__()
        self.wrapped_handler = handler

    def _can_handle(self, ticket):
        return self.wrapped_handler._can_handle(ticket)

    def _process(self, ticket):
        print(f"[LOG] Start ticket: {ticket.ticket_id}")
        self.wrapped_handler._process(ticket)
        print(f"[LOG] End ticket: {ticket.ticket_id}")


print("\n" + "=" * 70)
print("LOGGING DECORATOR")
print("=" * 70)

logged_level1 = LoggingHandler(Level1Support())
logged_level2 = LoggingHandler(Level2Support())
logged_level1.set_next(logged_level2)

ticket = SupportTicket(6, SupportTicket.SEVERITY_MEDIUM, "Need logs")

print(f"\n{'=' * 60}")
print(f"Processing: {ticket}")
print(f"{'=' * 60}")

logged_level1.handle(ticket)


# EDGE CASE
print("\n" + "=" * 70)
print("UNHANDLED REQUEST")
print("=" * 70)

ticket = SupportTicket(7, "ULTRA_CRITICAL", "Unknown severity")

simple_chain = Level1Support()
simple_chain.set_next(Level2Support())

print(f"\n{'=' * 60}")
print(f"Processing: {ticket}")
print(f"{'=' * 60}")

simple_chain.handle(ticket)
