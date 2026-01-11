from abc import ABC, abstractmethod

# Target interface expected by the application
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, customer_email):
        pass


# Existing compatible implementation
class InternalPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount, currency, customer_email):
        print("\nInternal Payment Processor")
        print(f"Processing {amount} {currency}")
        print(f"Customer: {customer_email}")
        print("Payment processed successfully")
        return {"status": "success", "transaction_id": "INT-12345"}


# Third-party gateways with incompatible interfaces

class StripeAPI:
    def create_charge(self, amount_cents, currency_code, email, description):
        print("\nStripe Payment Gateway")
        print(f"Charging {amount_cents} cents ({currency_code})")
        print(f"Email: {email}")
        print(f"Description: {description}")
        print("Stripe charge created")
        return {
            "charge_id": "ch_stripe_123",
            "paid": True,
            "amount": amount_cents
        }


class PayPalSDK:
    def make_payment(self, total, currency_type, payer_email, note):
        print("\nPayPal SDK")
        print(f"Payment of {total} {currency_type}")
        print(f"Payer: {payer_email}")
        print(f"Note: {note}")
        print("PayPal payment completed")
        return {
            "payment_id": "PAY-paypal-456",
            "state": "approved",
            "total": total
        }


class RazorpayClient:
    def initiate_transaction(self, price, curr, customer_id, remarks):
        print("\nRazorpay Client")
        print(f"Transaction: {price} {curr}")
        print(f"Customer ID: {customer_id}")
        print(f"Remarks: {remarks}")
        print("Razorpay transaction initiated")
        return {
            "txn_id": "rzp_789",
            "success": True,
            "price": price
        }


# Adapters convert third-party APIs to PaymentProcessor interface

class StripeAdapter(PaymentProcessor):
    def __init__(self):
        self.stripe = StripeAPI()

    def process_payment(self, amount, currency, customer_email):
        amount_cents = int(amount * 100)

        result = self.stripe.create_charge(
            amount_cents=amount_cents,
            currency_code=currency,
            email=customer_email,
            description="Product purchase"
        )

        return {
            "status": "success" if result.get("paid") else "failed",
            "transaction_id": result.get("charge_id"),
            "amount": result.get("amount") / 100
        }


class PayPalAdapter(PaymentProcessor):
    def __init__(self):
        self.paypal = PayPalSDK()

    def process_payment(self, amount, currency, customer_email):
        result = self.paypal.make_payment(
            total=amount,
            currency_type=currency,
            payer_email=customer_email,
            note="Product purchase"
        )

        return {
            "status": "success" if result.get("state") == "approved" else "failed",
            "transaction_id": result.get("payment_id"),
            "amount": result.get("total")
        }


class RazorpayAdapter(PaymentProcessor):
    def __init__(self):
        self.razorpay = RazorpayClient()

    def process_payment(self, amount, currency, customer_email):
        result = self.razorpay.initiate_transaction(
            price=amount,
            curr=currency,
            customer_id=customer_email,
            remarks="Product purchase"
        )

        return {
            "status": "success" if result.get("success") else "failed",
            "transaction_id": result.get("txn_id"),
            "amount": result.get("price")
        }


# Application depends only on PaymentProcessor interface
class EcommerceApp:
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor

    def checkout(self, amount, currency, customer_email):
        print(f"\n{'='*60}")
        print("E-commerce Checkout Process")
        print(f"{'='*60}")

        result = self.payment_processor.process_payment(
            amount, currency, customer_email
        )

        if result.get("status") == "success":
            print("Order confirmed")
            print(f"Transaction ID: {result.get('transaction_id')}")
            print(f"Amount: {result.get('amount')} {currency}")
        else:
            print("Payment failed")

        return result

# usage
print("="*60)
print("PAYMENT SYSTEM - WITH ADAPTER PATTERN")
print("="*60)

print("\nUsing Internal Payment Processor")
app = EcommerceApp(InternalPaymentProcessor())
app.checkout(100, "USD", "customer@example.com")

print("\nUsing Stripe via Adapter")
app = EcommerceApp(StripeAdapter())
app.checkout(150, "USD", "john@example.com")

print("\nUsing PayPal via Adapter")
app = EcommerceApp(PayPalAdapter())
app.checkout(200, "USD", "jane@example.com")

print("\nUsing Razorpay via Adapter")
app = EcommerceApp(RazorpayAdapter())
app.checkout(5000, "INR", "rahul@example.com")

# Demonstrate flexibility - switch payment processor easily
print("\n" + "="*60)
print("DEMONSTRATING FLEXIBILITY")
print("="*60)
def process_order(payment_processor: PaymentProcessor, amount: float):
    app = EcommerceApp(payment_processor)
    app.checkout(amount, "USD", "customer@example.com")


print("\nProcessing orders with different payment processors")
processors = [
    ("Internal", InternalPaymentProcessor()),
    ("Stripe", StripeAdapter()),
    ("PayPal", PayPalAdapter())
]

for name, processor in processors:
    print(f"\nUsing {name}")
    process_order(processor, 99.99)

# Adding new gateway is easy!
print("\n" + "="*60)
print("ADDING NEW PAYMENT GATEWAY (Square)")
print("="*60)

class SquareAPI:
    def process_transaction(self, amt, curr, email_addr):
        print("\nSquare API")
        print(f"Processing {amt} {curr}")
        print(f"Email: {email_addr}")
        print("Square transaction complete")
        return {"txn_status": "completed", "ref_id": "sq_999", "amt": amt}


class SquareAdapter(PaymentProcessor):
    def __init__(self):
        self.square = SquareAPI()

    def process_payment(self, amount, currency, customer_email):
        result = self.square.process_transaction(amount, currency, customer_email)

        return {
            "status": "success" if result.get("txn_status") == "completed" else "failed",
            "transaction_id": result.get("ref_id"),
            "amount": result.get("amt")
        }

print("\nUsing Square via Adapter")
app = EcommerceApp(SquareAdapter())
app.checkout(75, "USD", "mike@example.com")

print("\nSquare gateway added without modifying EcommerceApp")
