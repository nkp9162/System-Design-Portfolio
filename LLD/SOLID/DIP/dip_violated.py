class Invoice:
    def __init__(self, customer_name, amount):
        self.customer_name = customer_name
        self.amount = amount


class MySQLDatabase:
    def save_invoice(self, invoice: Invoice):
        print(f"[MySQL] Saving invoice for {invoice.customer_name} to MySQL database")
        print(f"[MySQL] INSERT INTO invoices VALUES ('{invoice.customer_name}', {invoice.amount})")


class EmailService:
    def send_invoice_email(self, invoice: Invoice):
        print(f"[Email] Sending invoice email to {invoice.customer_name}")
        print(f"[Email] Subject: Invoice for ${invoice.amount}")


class InvoiceProcessor:
    def __init__(self):
        self.database = MySQLDatabase()
        self.email_service = EmailService()

    def process_invoice(self, invoice: Invoice):
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"\n[Processor] Processing invoice for {invoice.customer_name}")
        print(f"[Processor] Amount: {invoice.amount}, Tax: 18%, Total: {total}")

        self.database.save_invoice(invoice)
        self.email_service.send_invoice_email(invoice)


print("=== Invoice Processing (Tightly Coupled) ===")
invoice1 = Invoice("Nirbhay", 1000)
invoice2 = Invoice("Rahul", 2000)

processor = InvoiceProcessor()
processor.process_invoice(invoice1)
processor.process_invoice(invoice2)

print("\n=== What if we want to use MongoDB instead? ===")
print("ERROR: Must modify InvoiceProcessor class!")
print("ERROR: Cannot easily switch implementations!")
