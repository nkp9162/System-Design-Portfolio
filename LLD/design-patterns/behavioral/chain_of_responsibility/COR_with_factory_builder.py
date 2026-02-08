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
            self._next_handler.handle(ticket)
        else:
            ticket.resolved = False

    @abstractmethod
    def _can_handle(self, ticket):
        pass

    @abstractmethod
    def _process(self, ticket):
        pass


class Level1Support(SupportHandler):
    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_LOW

    def _process(self, ticket):
        print(f"Level 1 resolved {ticket}")
        ticket.assigned_to = "Level 1"
        ticket.resolved = True


class Level1_5Support(SupportHandler):
    def _can_handle(self, ticket):
        return "escalated" in ticket.description.lower() and ticket.severity == SupportTicket.SEVERITY_LOW

    def _process(self, ticket):
        print(f"Level 1.5 resolved {ticket}")
        ticket.assigned_to = "Level 1.5"
        ticket.resolved = True


class Level2Support(SupportHandler):
    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_MEDIUM

    def _process(self, ticket):
        print(f"Level 2 resolved {ticket}")
        ticket.assigned_to = "Level 2"
        ticket.resolved = True


class Level3Support(SupportHandler):
    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_HIGH

    def _process(self, ticket):
        print(f"Level 3 resolved {ticket}")
        ticket.assigned_to = "Level 3"
        ticket.resolved = True


class ManagementSupport(SupportHandler):
    def _can_handle(self, ticket):
        return ticket.severity == SupportTicket.SEVERITY_CRITICAL

    def _process(self, ticket):
        print(f"Management resolved {ticket}")
        ticket.assigned_to = "Management"
        ticket.resolved = True



class ChainType(Enum):
    BUSINESS_HOURS = "business_hours"
    AFTER_HOURS = "after_hours"
    WEEKEND = "weekend"
    VIP_CUSTOMER = "vip_customer"


# BUILDER INTERFACE
class ChainBuilder(ABC):
    @abstractmethod
    def build(self) -> SupportHandler:
        pass


# CONCRETE BUILDERS

class BusinessHoursChain(ChainBuilder):
    def build(self):
        l1 = Level1Support()
        l15 = Level1_5Support()
        l2 = Level2Support()
        l3 = Level3Support()
        m = ManagementSupport()

        l1.set_next(l15).set_next(l2).set_next(l3).set_next(m)
        return l1


class AfterHoursChain(ChainBuilder):
    def build(self):
        return ManagementSupport()


class WeekendChain(ChainBuilder):
    def build(self):
        l1 = Level1Support()
        m = ManagementSupport()
        l1.set_next(m)
        return l1


class VIPChain(ChainBuilder):
    def build(self):
        l1 = Level1Support()
        l15 = Level1_5Support()
        l2 = Level2Support()
        l3 = Level3Support()
        m = ManagementSupport()

        l1.set_next(l15).set_next(l2).set_next(l3).set_next(m)
        return l1


# FACTORY (no if else)
class SupportChainFactory:
    _registry = {}
    _cache = {}

    @classmethod
    def register(cls, chain_type: ChainType, builder):
        cls._registry[chain_type] = builder

    @classmethod
    def create_chain(cls, chain_type: ChainType):
        if chain_type in cls._cache:
            return cls._cache[chain_type]

        builder = cls._registry.get(chain_type)
        if not builder:
            raise ValueError("Chain not registered")

        chain = builder().build()
        cls._cache[chain_type] = chain
        return chain


# REGISTRATION OF CHAINS
SupportChainFactory.register(ChainType.BUSINESS_HOURS, BusinessHoursChain)
SupportChainFactory.register(ChainType.AFTER_HOURS, AfterHoursChain)
SupportChainFactory.register(ChainType.WEEKEND, WeekendChain)
SupportChainFactory.register(ChainType.VIP_CUSTOMER, VIPChain)



class SupportSystem:

    def __init__(self, chain_type: ChainType):
        self.chain_type = chain_type
        self.chain = SupportChainFactory.create_chain(chain_type)

    def switch_chain(self, chain_type: ChainType):
        self.chain_type = chain_type
        self.chain = SupportChainFactory.create_chain(chain_type)

    def process_ticket(self, ticket: SupportTicket):
        self.chain.handle(ticket)
        print("Resolved:", ticket.resolved, "By:", ticket.assigned_to)



# usage
system = SupportSystem(ChainType.BUSINESS_HOURS)
system.process_ticket(SupportTicket(1, SupportTicket.SEVERITY_LOW, "reset"))

system.switch_chain(ChainType.AFTER_HOURS)
system.process_ticket(SupportTicket(2, SupportTicket.SEVERITY_LOW, "reset"))
