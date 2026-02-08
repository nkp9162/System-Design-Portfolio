# REQUEST

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

# HANDLER

class Level1Support:
    """Handles LOW severity."""

    def __init__(self):
        self.name = "Level 1 Support"

    def can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_LOW

    def handle(self, ticket):
        print(f"{self.name} handling: {ticket}")
        ticket.assigned_to = self.name
        ticket.resolved = True


class Level2Support:
    """Handles MEDIUM severity."""

    def __init__(self):
        self.name = "Level 2 Support"

    def can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_MEDIUM

    def handle(self, ticket):
        print(f"{self.name} handling: {ticket}")
        ticket.assigned_to = self.name
        ticket.resolved = True


class Level3Support:
    """Handles HIGH severity."""

    def __init__(self):
        self.name = "Level 3 Support"

    def can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_HIGH

    def handle(self, ticket):
        print(f"{self.name} handling: {ticket}")
        ticket.assigned_to = self.name
        ticket.resolved = True


class ManagementSupport:
    """Handles CRITICAL severity."""

    def __init__(self):
        self.name = "Management"

    def can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_CRITICAL

    def handle(self, ticket):
        print(f"{self.name} handling: {ticket}")
        ticket.assigned_to = self.name
        ticket.resolved = True



class SupportTicketSystem:

    def __init__(self):
        self.level1 = Level1Support()
        self.level2 = Level2Support()
        self.level3 = Level3Support()
        self.management = ManagementSupport()

    def process_ticket(self, ticket):
        print(f"\n{'=' * 60}")
        print(f"Processing: {ticket}")
        print(f"{'=' * 60}")

        if self.level1.can_handle(ticket):
            self.level1.handle(ticket)

        elif self.level2.can_handle(ticket):
            self.level2.handle(ticket)

        elif self.level3.can_handle(ticket):
            self.level3.handle(ticket)

        elif self.management.can_handle(ticket):
            self.management.handle(ticket)

        else:
            print("ERROR: No handler available!")
            ticket.resolved = False

        if ticket.resolved:
            print(f"RESOLVED BY: {ticket.assigned_to}")
        else:
            print("UNRESOLVED")


# HANDLER CHAIN V2 

class Level1SupportV2:
    """Passes forward if cannot handle."""

    def __init__(self):
        self.name = "Level 1 Support"
        self.next_handler = Level2SupportV2()

    def handle(self, ticket):
        print(f"\n{self.name} checking: {ticket}")

        if ticket.severity == SupportTicket.SEVERITY_LOW:
            print(f"{self.name} handling ticket")
            ticket.assigned_to = self.name
            ticket.resolved = True
        else:
            print(f"Passing to {self.next_handler.name}")
            self.next_handler.handle(ticket)


class Level2SupportV2:
    def __init__(self):
        self.name = "Level 2 Support"
        self.next_handler = Level3SupportV2()

    def handle(self, ticket):
        print(f"\n{self.name} checking: {ticket}")

        if ticket.severity == SupportTicket.SEVERITY_MEDIUM:
            print(f"{self.name} handling ticket")
            ticket.assigned_to = self.name
            ticket.resolved = True
        else:
            print(f"Passing to {self.next_handler.name}")
            self.next_handler.handle(ticket)


class Level3SupportV2:
    def __init__(self):
        self.name = "Level 3 Support"
        self.next_handler = ManagementSupportV2()

    def handle(self, ticket):
        print(f"\n{self.name} checking: {ticket}")

        if ticket.severity == SupportTicket.SEVERITY_HIGH:
            print(f"{self.name} handling ticket")
            ticket.assigned_to = self.name
            ticket.resolved = True
        else:
            print(f"Passing to {self.next_handler.name}")
            self.next_handler.handle(ticket)


class ManagementSupportV2:

    def __init__(self):
        self.name = "Management"
        self.next_handler = None

    def handle(self, ticket):
        print(f"\n{self.name} checking: {ticket}")

        if ticket.severity == SupportTicket.SEVERITY_CRITICAL:
            print(f"{self.name} handling ticket")
            ticket.assigned_to = self.name
            ticket.resolved = True
        else:
            print("No one left to handle this!")
            ticket.resolved = False

# USAGE
print("=" * 70)
print("WITHOUT CHAIN OF RESPONSIBILITY")
print("=" * 70)

print("\n" + "=" * 70)
print("APPROACH 1: Central Router")
print("=" * 70)

system = SupportTicketSystem()

tickets = [
    SupportTicket(1, SupportTicket.SEVERITY_LOW, "Password reset"),
    SupportTicket(2, SupportTicket.SEVERITY_MEDIUM, "Software install issue"),
    SupportTicket(3, SupportTicket.SEVERITY_HIGH, "Server slow"),
    SupportTicket(4, SupportTicket.SEVERITY_CRITICAL, "System down"),
]

for t in tickets:
    system.process_ticket(t)

print("\n" + "=" * 70)
print("APPROACH 2: Manual forwarding")
print("=" * 70)

ticket5 = SupportTicket(5, SupportTicket.SEVERITY_CRITICAL, "Data breach")
Level1SupportV2().handle(ticket5)

# severity + customer + age + type + business impact -> handler , thats why strategy pattern fails here. 
