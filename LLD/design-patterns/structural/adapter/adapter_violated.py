# Common payment interface used by our application
class PaymentProcessor:
    def process_payment(self, amount, currency, customer_email):
        pass


# Existing internal implementation
class InternalPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount, currency, customer_email):
        print(f"\nInternal Payment Processor")
        print(f"Processing {amount} {currency}")
        print(f"Customer: {customer_email}")
        print("Payment processed successfully")
        return {"status": "success", "transaction_id": "INT-12345"}


# Third-party payment gateways (incompatible interfaces)

class StripeAPI:
    def create_charge(self, amount_cents, currency_code, email, description):
        print(f"\nStripe Payment Gateway")
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
        print(f"\nPayPal SDK")
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
        print(f"\nRazorpay Client")
        print(f"Transaction: {price} {curr}")
        print(f"Customer ID: {customer_id}")
        print(f"Remarks: {remarks}")
        print("Razorpay transaction initiated")
        return {
            "txn_id": "rzp_789",
            "success": True,
            "price": price
        }


# Application code which only depends on PaymentProcessor Cannot directly use third-party gateways
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
            print(f"Order confirmed. Transaction ID: {result.get('transaction_id')}")
        return result


print("="*60)
print("PAYMENT SYSTEM - WITHOUT ADAPTER PATTERN")
print("="*60)

internal_processor = InternalPaymentProcessor()
app = EcommerceApp(internal_processor)
app.checkout(100, "USD", "customer@example.com")


print("\n" + "="*60)
print("TRYING TO USE THIRD-PARTY PAYMENT GATEWAYS")
print("="*60)

stripe = StripeAPI()
paypal = PayPalSDK()
razorpay = RazorpayClient()

print("\nERROR: Cannot use Stripe, PayPal and Razorpay directly")
print("Different method name, parameters, and return format")

print("\n" + "="*60)
print("BAD SOLUTION: MODIFYING APPLICATION CODE")
print("="*60)

# Application code modified to handle multiple gateways with if-else
class EcommerceAppWithIfElse:

    def __init__(self, gateway_type, gateway):
        self.gateway_type = gateway_type
        self.gateway = gateway

    def checkout(self, amount, currency, customer_email):
        if self.gateway_type == "stripe":
            amount_cents = int(amount * 100)
            result = self.gateway.create_charge(
                amount_cents, currency, customer_email, "Purchase"
            )

        elif self.gateway_type == "paypal":
            result = self.gateway.make_payment(
                amount, currency, customer_email, "Purchase"
            )

        elif self.gateway_type == "razorpay":
            result = self.gateway.initiate_transaction(
                amount, currency, customer_email, "Purchase"
            )


print("Problems with this approach:")
print("Violates Open/Closed Principle")
print("Application knows all gateway implementations")
print("Must modify app for each new gateway")
print("Tight coupling")
print("Hard to test and maintain")