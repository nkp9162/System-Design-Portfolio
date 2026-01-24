class VendingMachine:
    
    # State constants
    IDLE = "IDLE"
    HAS_MONEY = "HAS_MONEY"
    DISPENSING = "DISPENSING"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    
    def __init__(self, item_count):
        self.state = self.IDLE
        self.item_count = item_count
        self.inserted_money = 0
        self.item_price = 50  # price per item (INR)
    
    def insert_money(self, amount):
        print(f"\n[Action] Insert money: ₹{amount}")
        
        if self.state == self.IDLE:
            if self.item_count > 0:
                self.inserted_money += amount
                self.state = self.HAS_MONEY
                print(f"Money accepted. Total = ₹{self.inserted_money}")
                print(f"Item price = ₹{self.item_price}")
            else:
                print("Machine is out of stock")
                return False
        
        elif self.state == self.HAS_MONEY:
            self.inserted_money += amount
            print(f"Money accepted. Total = ₹{self.inserted_money}")
            print(f"Item price = ₹{self.item_price}")
        
        elif self.state == self.DISPENSING:
            print("Please wait. Dispensing in progress")
            return False
        
        elif self.state == self.OUT_OF_STOCK:
            print("Machine is out of stock")
            return False
        
        return True
    
    def eject_money(self):
        print("\n[Action] Eject money")
        
        if self.state == self.IDLE:
            print("No money to return")
            return False
        
        elif self.state == self.HAS_MONEY:
            print(f"Returning ₹{self.inserted_money}")
            self.inserted_money = 0
            self.state = self.IDLE
            return True
        
        elif self.state == self.DISPENSING:
            print("Cannot eject money while dispensing")
            return False
        
        elif self.state == self.OUT_OF_STOCK:
            if self.inserted_money > 0:
                print(f"Returning ₹{self.inserted_money}")
                self.inserted_money = 0
                return True
            else:
                print("No money to return")
                return False
        
        return False
    
    def dispense(self):
        print("\n[Action] Dispense item")
        
        if self.state == self.IDLE:
            print("Insert money first")
            return False
        
        elif self.state == self.HAS_MONEY:
            if self.inserted_money >= self.item_price:
                print("Sufficient money. Dispensing item")
                self.state = self.DISPENSING
                
                self.item_count -= 1
                change = self.inserted_money - self.item_price
                self.inserted_money = 0
                
                print("Item dispensed successfully")
                if change > 0:
                    print(f"Returning change = ₹{change}")
                
                if self.item_count == 0:
                    self.state = self.OUT_OF_STOCK
                    print("Machine is now out of stock")
                else:
                    self.state = self.IDLE
                    print(f"Items remaining = {self.item_count}")
                
                return True
            else:
                needed = self.item_price - self.inserted_money
                print(f"Insufficient money. Need ₹{needed} more")
                return False
        
        elif self.state == self.DISPENSING:
            print("Already dispensing. Please wait")
            return False
        
        elif self.state == self.OUT_OF_STOCK:
            print("Machine is out of stock")
            return False
        
        return False
    
    def refill(self, count):
        print(f"\n[Action] Refill machine with {count} items")
        
        if self.state == self.IDLE or self.state == self.OUT_OF_STOCK:
            self.item_count += count
            if self.state == self.OUT_OF_STOCK:
                self.state = self.IDLE
            print(f"Refill complete. Total items = {self.item_count}")
            return True
        
        elif self.state == self.HAS_MONEY:
            print("Cannot refill while money is inserted")
            return False
        
        elif self.state == self.DISPENSING:
            print("Cannot refill while dispensing")
            return False
        
        return False
    
    def get_status(self):
        print("\n[VendingMachine Status]")
        print(f"State  : {self.state}")
        print(f"Items  : {self.item_count}")
        print(f"Money  : ₹{self.inserted_money}")


# USAGE

print("=" * 60)
print("VENDING MACHINE - WITHOUT STATE PATTERN")
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

print("\nSCENARIO 4: Try to buy when out of stock")
machine.insert_money(50)
machine.dispense()

print("\nSCENARIO 5: Refill machine")
machine.refill(5)
machine.get_status()
