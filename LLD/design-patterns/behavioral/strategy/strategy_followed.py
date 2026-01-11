from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass
    
    @abstractmethod
    def get_payment_name(self) -> str:
        pass


class CreditCardPayment(PaymentStrategy):
    
    def pay(self, amount: float) -> bool:
        print("Payment Type: Credit Card")
        print("Step 1: Validating card number...")
        print("Step 2: Checking card expiry...")
        print("Step 3: Verifying CVV...")
        print("Step 4: Processing payment through card network...")
        fee = amount * 0.03
        total = amount + fee
        print(f"Transaction Fee: ${fee:.2f} (3%)")
        print(f"Total Amount: ${total:.2f}")
        print("✓ Credit Card Payment Successful!")
        return True
    
    def get_payment_name(self) -> str:
        return "Credit Card"


class PayPalPayment(PaymentStrategy):
    
    def pay(self, amount: float) -> bool:
        print("Payment Type: PayPal")
        print("Step 1: Redirecting to PayPal...")
        print("Step 2: Authenticating user...")
        print("Step 3: Processing payment through PayPal...")
        fee = amount * 0.04
        total = amount + fee
        print(f"Transaction Fee: ${fee:.2f} (4%)")
        print(f"Total Amount: ${total:.2f}")
        print("✓ PayPal Payment Successful!")
        return True
    
    def get_payment_name(self) -> str:
        return "PayPal"


class BankTransferPayment(PaymentStrategy):
    
    def pay(self, amount: float) -> bool:
        print("Payment Type: Bank Transfer")
        print("Step 1: Validating account number...")
        print("Step 2: Verifying bank details...")
        print("Step 3: Initiating transfer...")
        fee = 2.00
        total = amount + fee
        print(f"Transaction Fee: ${fee:.2f} (Flat)")
        print(f"Total Amount: ${total:.2f}")
        print("✓ Bank Transfer Successful!")
        return True
    
    def get_payment_name(self) -> str:
        return "Bank Transfer"


class CryptocurrencyPayment(PaymentStrategy):
    
    def pay(self, amount: float) -> bool:
        print("Payment Type: Cryptocurrency")
        print("Step 1: Generating wallet address...")
        print("Step 2: Waiting for blockchain confirmation...")
        print("Step 3: Verifying transaction...")
        fee = amount * 0.01
        total = amount + fee
        print(f"Transaction Fee: ${fee:.2f} (1%)")
        print(f"Total Amount: ${total:.2f}")
        print("✓ Cryptocurrency Payment Successful!")
        return True
    
    def get_payment_name(self) -> str:
        return "Cryptocurrency"


class GooglePayPayment(PaymentStrategy):
    
    def pay(self, amount: float) -> bool:
        print("Payment Type: Google Pay")
        print("Step 1: Authenticating via Google...")
        print("Step 2: Processing payment...")
        fee = amount * 0.02
        total = amount + fee
        print(f"Transaction Fee: ${fee:.2f} (2%)")
        print(f"Total Amount: ${total:.2f}")
        print("✓ Google Pay Payment Successful!")
        return True
    
    def get_payment_name(self) -> str:
        return "Google Pay"


class PaymentProcessor:
    
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: PaymentStrategy):
        print(f"\n→ Switching payment method to: {strategy.get_payment_name()}")
        self._strategy = strategy
    
    def process_payment(self, amount: float) -> bool:
        print(f"\n{'='*50}")
        print(f"Processing ${amount} payment...")
        print(f"{'='*50}")
        return self._strategy.pay(amount)


print("="*60)
print("PAYMENT SYSTEM - WITH STRATEGY PATTERN")
print("="*60)

processor = PaymentProcessor(CreditCardPayment())
processor.process_payment(100)

processor.set_strategy(PayPalPayment())
processor.process_payment(200)

processor.set_strategy(BankTransferPayment())
processor.process_payment(150)

processor.set_strategy(CryptocurrencyPayment())
processor.process_payment(500)

processor.set_strategy(GooglePayPayment())
processor.process_payment(300)

print("\n" + "="*60)
print("DYNAMIC STRATEGY SELECTION:")
print("="*60)


def get_payment_strategy(method: str) -> PaymentStrategy:
    strategies = {
        "credit": CreditCardPayment(),
        "paypal": PayPalPayment(),
        "bank": BankTransferPayment(),
        "crypto": CryptocurrencyPayment(),
        "gpay": GooglePayPayment()
    }
    return strategies.get(method, CreditCardPayment())

# User choosing payment method
user_choice = "crypto"
print(f"User selected: {user_choice}")
processor.set_strategy(get_payment_strategy(user_choice))
processor.process_payment(250)
