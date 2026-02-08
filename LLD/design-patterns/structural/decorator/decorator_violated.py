# BASE COMPONENT
class SimpleCoffee:

    def get_description(self):
        return "Simple Coffee"

    def get_cost(self):
        return 50.0

# INHERITANCE EXPLOSION
class CoffeeWithMilk(SimpleCoffee):

    def get_description(self):
        return "Coffee with Milk"

    def get_cost(self):
        return 50.0 + 10.0


class CoffeeWithSugar(SimpleCoffee):

    def get_description(self):
        return "Coffee with Sugar"

    def get_cost(self):
        return 50.0 + 5.0


class CoffeeWithMilkAndSugar(SimpleCoffee):

    def get_description(self):
        return "Coffee with Milk and Sugar"

    def get_cost(self):
        return 50.0 + 10.0 + 5.0


class CoffeeWithWhippedCream(SimpleCoffee):

    def get_description(self):
        return "Coffee with Whipped Cream"

    def get_cost(self):
        return 50.0 + 15.0


class CoffeeWithMilkAndWhippedCream(SimpleCoffee):

    def get_description(self):
        return "Coffee with Milk and Whipped Cream"

    def get_cost(self):
        return 50.0 + 10.0 + 15.0


class CoffeeWithSugarAndWhippedCream(SimpleCoffee):

    def get_description(self):
        return "Coffee with Sugar and Whipped Cream"

    def get_cost(self):
        return 50.0 + 5.0 + 15.0


class CoffeeWithMilkSugarAndWhippedCream(SimpleCoffee):

    def get_description(self):
        return "Coffee with Milk, Sugar and Whipped Cream"

    def get_cost(self):
        return 50.0 + 10.0 + 5.0 + 15.0


class CoffeeWithCaramel(SimpleCoffee):

    def get_description(self):
        return "Coffee with Caramel"

    def get_cost(self):
        return 50.0 + 20.0


# RUNTIME FLEXIBILITY PROBLEM
def try_custom_combination():
    print("\n" + "=" * 60)
    print("PROBLEM: No dynamic combinations")
    print("=" * 60)

    print("\nDesired order:")
    print("Simple Coffee + Milk + Sugar + Cream + Caramel")

    print("\nReality:")
    print("- Need a brand new class")
    print("- Hardcoded description and cost")
    print("- Code change required")

    print("\nEdge cases:")
    print("- Double milk?")
    print("- Triple sugar?")
    print("- Extra cream?")
    print("=> More and more classes")


# DUPLICATION PROBLEM
class CoffeeWithMilkSugarWhippedCreamAndCaramel(SimpleCoffee):

    def get_description(self):
        return "Coffee with Milk, Sugar, Whipped Cream and Caramel"

    def get_cost(self):
        cost = 50.0
        cost += 10.0   # milk
        cost += 5.0    # sugar
        cost += 15.0   # cream
        cost += 20.0   # caramel
        return cost


# IMMUTABILITY PROBLEM
def try_remove_extra():
    print("\n" + "=" * 60)
    print("PROBLEM: Cannot remove add-ons")
    print("=" * 60)

    coffee = CoffeeWithMilkAndSugar()
    print(f"\nCreated: {coffee.get_description()}")
    print(f"Cost: {coffee.get_cost()}")

    print("\nCustomer says: remove sugar")
    print("Result: Not possible")
    print("Need to create a new object")


# USAGE
print("=" * 60)
print("COFFEE SHOP - WITHOUT DECORATOR PATTERN")
print("=" * 60)

print("\n Creating some coffees:")
coffee1 = SimpleCoffee()
print(coffee1.get_description(), "->", coffee1.get_cost())

coffee2 = CoffeeWithMilk()
print(coffee2.get_description(), "->", coffee2.get_cost())

coffee3 = CoffeeWithMilkSugarAndWhippedCream()
print(coffee3.get_description(), "->", coffee3.get_cost())

try_custom_combination()
try_remove_extra()
