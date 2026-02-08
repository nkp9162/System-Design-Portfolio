from abc import ABC, abstractmethod
from enum import Enum

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


# HANDLER INTERFACE
class SupportHandler(ABC):

    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, ticket):
        if self._can_handle(ticket):
            self._process(ticket)
        elif self._next_handler:
            print(f"{self.__class__.__name__} passing to next handler")
            self._next_handler.handle(ticket)
        else:
            print(f"{self.__class__.__name__}: End of chain, ticket unhandled")
            ticket.resolved = False

    @abstractmethod
    def _can_handle(self, ticket):
        pass

    @abstractmethod
    def _process(self, ticket):
        pass


# CONCRETE HANDLERS

class Level1Support(SupportHandler):
    """Handles LOW severity tickets"""

    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_LOW

    def _process(self, ticket):
        print(f"\nLevel 1 Support handling: {ticket}")
        print("Action: Resolving basic issue")
        ticket.assigned_to = "Level 1 Support"
        ticket.resolved = True


class Level1_5Support(SupportHandler):
    """Handles escalated LOW severity tickets"""

    def _can_handle(self, ticket):
        return "escalated" in ticket.description.lower() and ticket.severity == SupportTicket.SEVERITY_LOW

    def _process(self, ticket):
        print(f"\nLevel 1.5 Support handling: {ticket}")
        print("Action: Handling escalated basic issue")
        ticket.assigned_to = "Level 1.5 Support"
        ticket.resolved = True


class Level2Support(SupportHandler):
    """Handles MEDIUM severity tickets"""

    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_MEDIUM

    def _process(self, ticket):
        print(f"\nLevel 2 Support handling: {ticket}")
        print("Action: Investigating and resolving technical issue")
        ticket.assigned_to = "Level 2 Support"
        ticket.resolved = True


class Level3Support(SupportHandler):
    """Handles HIGH severity tickets"""

    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_HIGH

    def _process(self, ticket):
        print(f"\nLevel 3 Support handling: {ticket}")
        print("Action: Deep technical investigation and resolution")
        ticket.assigned_to = "Level 3 Support"
        ticket.resolved = True


class ManagementSupport(SupportHandler):
    """Handles CRITICAL severity tickets"""

    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_CRITICAL

    def _process(self, ticket):
        print(f"\nManagement handling: {ticket}")
        print("Action: Emergency response and escalation to leadership")
        ticket.assigned_to = "Management"
        ticket.resolved = True



# CHAIN TYPES
class ChainType(Enum):
    STANDARD = "standard"
    BUSINESS_HOURS = "business_hours"
    AFTER_HOURS = "after_hours"
    WEEKEND = "weekend"
    QUICK_RESPONSE = "quick_response"
    VIP_CUSTOMER = "vip_customer"



# chain factory to create different chains based on scenario and reuse them without rebuilding every time.
class SupportChainFactory:

    _chains = {}  

    @staticmethod
    def create_chain(chain_type: ChainType) -> SupportHandler:

        if chain_type in SupportChainFactory._chains:
            return SupportChainFactory._chains[chain_type]

        if chain_type in (ChainType.STANDARD, ChainType.BUSINESS_HOURS):
            level1 = Level1Support()
            level1_5 = Level1_5Support()
            level2 = Level2Support()
            level3 = Level3Support()
            management = ManagementSupport()

            level1.set_next(level1_5).set_next(level2).set_next(level3).set_next(management)
            head = level1

        elif chain_type == ChainType.AFTER_HOURS:
            head = ManagementSupport()

        elif chain_type == ChainType.WEEKEND:
            level1 = Level1Support()
            management = ManagementSupport()
            level1.set_next(management)
            head = level1

        elif chain_type == ChainType.QUICK_RESPONSE:
            level1 = Level1Support()
            level3 = Level3Support()
            management = ManagementSupport()
            level1.set_next(level3).set_next(management)
            head = level1

        elif chain_type == ChainType.VIP_CUSTOMER:
            level1 = Level1Support()
            level1_5 = Level1_5Support()
            level2 = Level2Support()
            level3 = Level3Support()
            management = ManagementSupport()

            level1.set_next(level1_5).set_next(level2).set_next(level3).set_next(management)
            head = level1

        else:
            head = SupportChainFactory.create_chain(ChainType.STANDARD)

        SupportChainFactory._chains[chain_type] = head
        return head
    
    @staticmethod
    def get_available_chains():
        return [
            {
                "type": ChainType.BUSINESS_HOURS,
                "description": "Full support chain (9 AM - 6 PM weekdays)",
                "handlers": ["Level1", "Level1.5", "Level2", "Level3", "Management"]
            },
            {
                "type": ChainType.AFTER_HOURS,
                "description": "Critical issues only (6 PM - 9 AM)",
                "handlers": ["Management only"]
            },
            {
                "type": ChainType.WEEKEND,
                "description": "Basic + critical support (Weekends)",
                "handlers": ["Level1", "Management"]
            },
            {
                "type": ChainType.QUICK_RESPONSE,
                "description": "Fast-track support (emergency mode)",
                "handlers": ["Level1", "Level3", "Management"]
            },
            {
                "type": ChainType.VIP_CUSTOMER,
                "description": "Premium customer support",
                "handlers": ["Level1", "Level1.5", "Level2", "Level3", "Management"]
            }
        ]


# SUPPORT SYSTEM
class SupportSystem:

    def __init__(self, chain_type: ChainType = ChainType.BUSINESS_HOURS):
        self.chain_type = chain_type
        self.chain = SupportChainFactory.create_chain(chain_type)
        print(f"\nSupport System initialized with: {chain_type.value}")

    def process_ticket(self, ticket: SupportTicket):
        print(f"\n{'='*60}")
        print(f"Processing: {ticket}")
        print(f"Chain Type: {self.chain_type.value}")
        print(f"{'='*60}")

        self.chain.handle(ticket)

        if ticket.resolved:
            print(f"Ticket resolved by: {ticket.assigned_to}")
        else:
            print("Ticket unresolved - may need business hours")

    def switch_chain(self, chain_type: ChainType):
        print(f"\nSwitching from {self.chain_type.value} to {chain_type.value}")
        self.chain_type = chain_type
        self.chain = SupportChainFactory.create_chain(chain_type)


# USAGE

print("="*70)
print("SUPPORT TICKET SYSTEM - WITH FACTORY")
print("="*70)

business_system = SupportSystem(ChainType.BUSINESS_HOURS)

tickets = [
    SupportTicket(1, SupportTicket.SEVERITY_LOW, "Password reset"),
    SupportTicket(2, SupportTicket.SEVERITY_MEDIUM, "Software installation issue"),
    SupportTicket(3, SupportTicket.SEVERITY_HIGH, "Server performance issue"),
]

for ticket in tickets:
    business_system.process_ticket(ticket)


print("\nAvailable chain configurations:")
for chain_info in SupportChainFactory.get_available_chains():
    print(f"\n  {chain_info['type'].value}:")
    print(f"    Description: {chain_info['description']}")
    print(f"    Handlers: {' -> '.join(chain_info['handlers'])}")


print("\nScenario: After Hours")
after_hours_system = SupportSystem(ChainType.AFTER_HOURS)

ticket4 = SupportTicket(4, SupportTicket.SEVERITY_LOW, "Need password reset")
ticket5 = SupportTicket(5, SupportTicket.SEVERITY_CRITICAL, "Production server down!")

after_hours_system.process_ticket(ticket4)
after_hours_system.process_ticket(ticket5)


print("\nScenario: Weekend")
weekend_system = SupportSystem(ChainType.WEEKEND)

ticket6 = SupportTicket(6, SupportTicket.SEVERITY_LOW, "Simple question")
ticket7 = SupportTicket(7, SupportTicket.SEVERITY_MEDIUM, "Installation problem")

weekend_system.process_ticket(ticket6)
weekend_system.process_ticket(ticket7)


print("\nScenario: VIP Customer")
vip_system = SupportSystem(ChainType.VIP_CUSTOMER)

ticket8 = SupportTicket(8, SupportTicket.SEVERITY_MEDIUM, "VIP needs help")
vip_system.process_ticket(ticket8)


print("\nDYNAMIC CHAIN SWITCHING")

system = SupportSystem(ChainType.BUSINESS_HOURS)

ticket9 = SupportTicket(9, SupportTicket.SEVERITY_MEDIUM, "Need help now")
system.process_ticket(ticket9)

print("\nSwitching to after hours mode")
system.switch_chain(ChainType.AFTER_HOURS)

ticket10 = SupportTicket(10, SupportTicket.SEVERITY_MEDIUM, "Need help after hours")
system.process_ticket(ticket10)
