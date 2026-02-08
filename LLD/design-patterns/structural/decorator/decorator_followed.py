from abc import ABC, abstractmethod

# COMPONENT INTERFACE
class Coffee(ABC):

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass

# CONCRETE COMPONENTS (Base Coffees)
class SimpleCoffee(Coffee):

    def get_description(self) -> str:
        return "Simple Coffee"

    def get_cost(self) -> float:
        return 50.0


class Espresso(Coffee):

    def get_description(self) -> str:
        return "Espresso"

    def get_cost(self) -> float:
        return 70.0


class Cappuccino(Coffee):

    def get_description(self) -> str:
        return "Cappuccino"

    def get_cost(self) -> float:
        return 80.0

# DECORATOR BASE CLASS
class CoffeeDecorator(Coffee):

    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def get_description(self) -> str:
        return self._coffee.get_description()

    def get_cost(self) -> float:
        return self._coffee.get_cost()

# CONCRETE DECORATORS
class MilkDecorator(CoffeeDecorator):

    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Milk"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 10.0


class SugarDecorator(CoffeeDecorator):

    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Sugar"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 5.0


class WhippedCreamDecorator(CoffeeDecorator):

    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Whipped Cream"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 15.0


class CaramelDecorator(CoffeeDecorator):

    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Caramel"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 20.0


class VanillaDecorator(CoffeeDecorator):

    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Vanilla"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 12.0


class ChocolateDecorator(CoffeeDecorator):

    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Chocolate"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 18.0


def display_coffee(title: str, coffee: Coffee):
    print(f"\n{title}")
    print(f"Description : {coffee.get_description()}")
    print(f"Cost        : ₹{coffee.get_cost():.2f}")



# USAGE 

print("=" * 60)
print("COFFEE SHOP - DECORATOR PATTERN")
print("=" * 60)

# Basic combinations
coffee1 = SimpleCoffee()
display_coffee("Order 1: Simple Coffee", coffee1)

coffee2 = MilkDecorator(SimpleCoffee())
display_coffee("Order 2: Coffee with Milk", coffee2)

coffee3 = SugarDecorator(MilkDecorator(SimpleCoffee()))
display_coffee("Order 3: Coffee with Milk and Sugar", coffee3)

# Complex combination
coffee4 = CaramelDecorator(
    WhippedCreamDecorator(
        SugarDecorator(
            MilkDecorator(SimpleCoffee())
        )
    )
)
display_coffee(
    "Order 4: Coffee with Milk, Sugar, Cream, Caramel",
    coffee4
)

# Same add-on multiple times
coffee5 = SugarDecorator(
    SugarDecorator(
        SugarDecorator(
            MilkDecorator(
                MilkDecorator(SimpleCoffee())
            )
        )
    )
)
display_coffee(
    "Order 5: Double Milk, Triple Sugar",
    coffee5
)

# Works with different base coffees
espresso = MilkDecorator(Espresso())
display_coffee("Espresso with Milk", espresso)

cappuccino = ChocolateDecorator(
    VanillaDecorator(Cappuccino())
)
display_coffee(
    "Cappuccino with Vanilla and Chocolate",
    cappuccino
)

# ADDING NEW COFFEE DECORATOR WITHOUT MODIFYING OLD CODE
class CinnamonDecorator(CoffeeDecorator):

    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Cinnamon"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 8.0


coffee6 = CinnamonDecorator(MilkDecorator(SimpleCoffee()))
display_coffee(
    "Coffee with Milk and Cinnamon (New Add-on)",
    coffee6
)

# RUNTIME CUSTOMIZATION
def customize_coffee(base: Coffee, extras: list[str]) -> Coffee:
    coffee = base

    for extra in extras:
        if extra == "milk":
            coffee = MilkDecorator(coffee)
        elif extra == "sugar":
            coffee = SugarDecorator(coffee)
        elif extra == "cream":
            coffee = WhippedCreamDecorator(coffee)
        elif extra == "caramel":
            coffee = CaramelDecorator(coffee)
        elif extra == "vanilla":
            coffee = VanillaDecorator(coffee)
        elif extra == "chocolate":
            coffee = ChocolateDecorator(coffee)

    return coffee


custom1 = customize_coffee(Cappuccino(), ["milk", "sugar"])
display_coffee("Custom Cappuccino", custom1)

custom2 = customize_coffee(Espresso(), ["vanilla", "chocolate", "cream"])
display_coffee("Custom Espresso", custom2)

custom3 = customize_coffee(SimpleCoffee(), ["caramel", "milk"])
display_coffee("Custom Simple Coffee", custom3)
