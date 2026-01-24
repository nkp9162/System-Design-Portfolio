from abc import ABC, abstractmethod

# CONTEXT - Vending Machine
class VendingMachine:
    
    def __init__(self, item_count):
        self.item_count = item_count
        self.inserted_money = 0
        self.item_price = 50
        
        # Initialize states
        self._idle_state = IdleState(self)
        self._has_money_state = HasMoneyState(self)
        self._dispensing_state = DispensingState(self)
        self._out_of_stock_state = OutOfStockState(self)
        
        # Initial state
        if item_count > 0:
            self._state = self._idle_state
        else:
            self._state = self._out_of_stock_state
    
    def set_state(self, state):
        self._state = state
    
    def insert_money(self, amount):
        return self._state.insert_money(amount)
    
    def eject_money(self):
        return self._state.eject_money()
    
    def dispense(self):
        return self._state.dispense()
    
    def refill(self, count):
        return self._state.refill(count)
    
    # State getters
    def get_idle_state(self):
        return self._idle_state
    
    def get_has_money_state(self):
        return self._has_money_state
    
    def get_dispensing_state(self):
        return self._dispensing_state
    
    def get_out_of_stock_state(self):
        return self._out_of_stock_state
    
    def get_status(self):
        print("\n[VendingMachine Status]")
        print(f"State  : {self._state.__class__.__name__}")
        print(f"Items  : {self.item_count}")
        print(f"Money  : ₹{self.inserted_money}")


# STATE INTERFACE
class VendingMachineState(ABC):

    def __init__(self, machine: VendingMachine):
        self.machine = machine
    
    @abstractmethod
    def insert_money(self, amount):
        pass
    
    @abstractmethod
    def eject_money(self):
        pass
    
    @abstractmethod
    def dispense(self):
        pass
    
    @abstractmethod
    def refill(self, count):
        pass


# CONCRETE STATES

class IdleState(VendingMachineState):

    def insert_money(self, amount):
        print(f"\n[IdleState] Insert money: ₹{amount}")
        self.machine.inserted_money += amount
        print(f"Money accepted. Total = ₹{self.machine.inserted_money}")
        print(f"Item price = ₹{self.machine.item_price}")
        
        self.machine.set_state(self.machine.get_has_money_state())
        return True
    
    def eject_money(self):
        print("\n[IdleState] Eject money")
        print("No money to eject")
        return False
    
    def dispense(self):
        print("\n[IdleState] Dispense request")
        print("Insert money first")
        return False
    
    def refill(self, count):
        print(f"\n[IdleState] Refill machine with {count} items")
        self.machine.item_count += count
        print(f"Refill complete. Total items = {self.machine.item_count}")
        return True


class HasMoneyState(VendingMachineState):
    
    def insert_money(self, amount):
        print(f"\n[HasMoneyState] Insert money: ₹{amount}")
        self.machine.inserted_money += amount
        print(f"Money accepted. Total = ₹{self.machine.inserted_money}")
        return True
    
    def eject_money(self):
        print("\n[HasMoneyState] Eject money")
        print(f"Returning ₹{self.machine.inserted_money}")
        self.machine.inserted_money = 0
        self.machine.set_state(self.machine.get_idle_state())
        return True
    
    def dispense(self):
        print("\n[HasMoneyState] Dispense request")
        
        if self.machine.inserted_money >= self.machine.item_price:
            print("Sufficient money. Dispensing item")
            self.machine.set_state(self.machine.get_dispensing_state())
            
            self.machine.item_count -= 1
            change = self.machine.inserted_money - self.machine.item_price
            self.machine.inserted_money = 0
            
            print("Item dispensed")
            if change > 0:
                print(f"Returning change = ₹{change}")
            
            if self.machine.item_count == 0:
                self.machine.set_state(self.machine.get_out_of_stock_state())
                print("Machine is now out of stock")
            else:
                self.machine.set_state(self.machine.get_idle_state())
                print(f"Items remaining = {self.machine.item_count}")
            
            return True
        else:
            needed = self.machine.item_price - self.machine.inserted_money
            print(f"Insufficient money. Need ₹{needed} more")
            return False
    
    def refill(self, count):
        print(f"\n[HasMoneyState] Refill attempt with {count} items")
        print("Cannot refill while money is inserted")
        return False


class DispensingState(VendingMachineState):
    
    def insert_money(self, amount):
        print(f"\n[DispensingState] Insert money: ₹{amount}")
        print("Please wait. Dispensing in progress")
        return False
    
    def eject_money(self):
        print("\n[DispensingState] Eject money")
        print("Cannot eject during dispensing")
        return False
    
    def dispense(self):
        print("\n[DispensingState] Dispense request")
        print("Already dispensing")
        return False
    
    def refill(self, count):
        print(f"\n[DispensingState] Refill attempt with {count} items")
        print("Cannot refill during dispensing")
        return False


class OutOfStockState(VendingMachineState):

    def insert_money(self, amount):
        print(f"\n[OutOfStockState] Insert money: ₹{amount}")
        print("Machine is out of stock")
        return False
    
    def eject_money(self):
        print("\n[OutOfStockState] Eject money")
        if self.machine.inserted_money > 0:
            print(f"Returning ₹{self.machine.inserted_money}")
            self.machine.inserted_money = 0
            return True
        else:
            print("No money to eject")
            return False
    
    def dispense(self):
        print("\n[OutOfStockState] Dispense request")
        print("Machine is out of stock")
        return False
    
    def refill(self, count):
        print(f"\n[OutOfStockState] Refill machine with {count} items")
        self.machine.item_count += count
        print(f"Refill complete. Total items = {self.machine.item_count}")
        self.machine.set_state(self.machine.get_idle_state())
        return True


# USAGE

print("=" * 60)
print("VENDING MACHINE - WITH STATE PATTERN")
print("=" * 60)

machine = VendingMachine(item_count=3)

print("\nSCENARIO 1: Normal purchase")
machine.get_status()
machine.insert_money(30)
machine.insert_money(20)
machine.dispense()
machine.get_status()

print("\nSCENARIO 2: Insufficient money")
machine.insert_money(30)
machine.dispense()
machine.eject_money()
machine.get_status()

print("\nSCENARIO 3: Buy until out of stock")
machine.insert_money(50)
machine.dispense()
machine.insert_money(50)
machine.dispense()
machine.get_status()

print("\nSCENARIO 4: Out of stock")
machine.insert_money(50)
machine.dispense()

print("\nSCENARIO 5: Refill machine")
machine.refill(5)
machine.get_status()

print("\nSCENARIO 6: Complex workflow")
machine.insert_money(25)
machine.insert_money(15)
machine.insert_money(10)
machine.dispense()
machine.insert_money(50)
machine.dispense()
machine.get_status()
