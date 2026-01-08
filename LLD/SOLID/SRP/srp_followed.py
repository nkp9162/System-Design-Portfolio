class Invoice:
    def __init__(self, customer_name, amount):
        self.customer_name = customer_name
        self.amount = amount


class InvoiceCalculator:
    def calculate_total(self, invoice: Invoice):
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"Calculated total with tax: {total}")


class InvoiceRepository:
    def save(self, invoice: Invoice):
        print(f"Invoice for {invoice.customer_name} saved to database")


class InvoiceEmailService:
    def send(self, invoice: Invoice):
        print(f"Invoice email sent to {invoice.customer_name}")


invoice = Invoice("Nirbhay", 1000)

calculator = InvoiceCalculator()
repository = InvoiceRepository()
email_service = InvoiceEmailService()

calculator.calculate_total(invoice)
repository.save(invoice)
email_service.send(invoice)
