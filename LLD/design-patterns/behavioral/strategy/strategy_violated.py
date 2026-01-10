class PaymentProcessor:
    
    def __init__(self, payment_type):
        self.payment_type = payment_type
    
    def process_payment(self, amount):
        print(f"\n{'='*50}")
        print(f"Processing ${amount} payment...")
        print(f"{'='*50}")
        
        if self.payment_type == "credit_card":
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
        
        elif self.payment_type == "paypal":
            print("Payment Type: PayPal")
            print("Step 1: Redirecting to PayPal...")
            print("Step 2: Authenticating user...")
            print("Step 3: Processing payment through PayPal...")
            fee = amount * 0.04
            total = amount + fee
            print(f"Transaction Fee: ${fee:.2f} (4%)")
            print(f"Total Amount: ${total:.2f}")
            print("✓ PayPal Payment Successful!")
        
        elif self.payment_type == "bank_transfer":
            print("Payment Type: Bank Transfer")
            print("Step 1: Validating account number...")
            print("Step 2: Verifying bank details...")
            print("Step 3: Initiating transfer...")
            fee = 2.00
            total = amount + fee
            print(f"Transaction Fee: ${fee:.2f} (Flat)")
            print(f"Total Amount: ${total:.2f}")
            print("✓ Bank Transfer Successful!")
        
        elif self.payment_type == "cryptocurrency":
            print("Payment Type: Cryptocurrency")
            print("Step 1: Generating wallet address...")
            print("Step 2: Waiting for blockchain confirmation...")
            print("Step 3: Verifying transaction...")
            fee = amount * 0.01
            total = amount + fee
            print(f"Transaction Fee: ${fee:.2f} (1%)")
            print(f"Total Amount: ${total:.2f}")
            print("✓ Cryptocurrency Payment Successful!")
        
        else:
            print(f"ERROR: Unsupported payment type '{self.payment_type}'")
            return False
        
        return True


print("="*60)
print("PAYMENT SYSTEM - WITHOUT STRATEGY PATTERN")
print("="*60)

credit_processor = PaymentProcessor("credit_card")
credit_processor.process_payment(100)

paypal_processor = PaymentProcessor("paypal")
paypal_processor.process_payment(200)

bank_processor = PaymentProcessor("bank_transfer")
bank_processor.process_payment(150)

crypto_processor = PaymentProcessor("cryptocurrency")
crypto_processor.process_payment(500)
