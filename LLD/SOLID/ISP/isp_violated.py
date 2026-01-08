from abc import ABC, abstractmethod


class Invoice:
    def __init__(self, customer_name, amount):
        self.customer_name = customer_name
        self.amount = amount


class InvoiceOperations(ABC):
    @abstractmethod
    def calculate_total(self, invoice: Invoice) -> float:
        pass

    @abstractmethod
    def save_to_database(self, invoice: Invoice):
        pass

    @abstractmethod
    def send_email(self, invoice: Invoice):
        pass

    @abstractmethod
    def generate_pdf(self, invoice: Invoice):
        pass

    @abstractmethod
    def send_sms(self, invoice: Invoice):
        pass


class FullInvoiceService(InvoiceOperations):
    def calculate_total(self, invoice: Invoice) -> float:
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"[Full Service] Calculated total: {total}")
        return total

    def save_to_database(self, invoice: Invoice):
        print(f"[Full Service] Saved invoice for {invoice.customer_name} to database")

    def send_email(self, invoice: Invoice):
        print(f"[Full Service] Email sent to {invoice.customer_name}")

    def generate_pdf(self, invoice: Invoice):
        print(f"[Full Service] PDF generated for {invoice.customer_name}")

    def send_sms(self, invoice: Invoice):
        print(f"[Full Service] SMS sent to {invoice.customer_name}")


class ReadOnlyInvoiceService(InvoiceOperations):
    def calculate_total(self, invoice: Invoice) -> float:
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"[ReadOnly] Calculated total: {total}")
        return total

    def save_to_database(self, invoice: Invoice):
        raise NotImplementedError("ReadOnly service cannot save to database!")

    def send_email(self, invoice: Invoice):
        raise NotImplementedError("ReadOnly service cannot send emails!")

    def generate_pdf(self, invoice: Invoice):
        raise NotImplementedError("ReadOnly service cannot generate PDFs!")

    def send_sms(self, invoice: Invoice):
        raise NotImplementedError("ReadOnly service cannot send SMS!")


class EmailOnlyInvoiceService(InvoiceOperations):
    def calculate_total(self, invoice: Invoice) -> float:
        raise NotImplementedError("Email service doesn't calculate totals!")

    def save_to_database(self, invoice: Invoice):
        raise NotImplementedError("Email service doesn't save to database!")

    def send_email(self, invoice: Invoice):
        print(f"[Email Only] Email sent to {invoice.customer_name}")

    def generate_pdf(self, invoice: Invoice):
        raise NotImplementedError("Email service doesn't generate PDFs!")

    def send_sms(self, invoice: Invoice):
        raise NotImplementedError("Email service doesn't send SMS!")


invoice = Invoice("Nirbhay", 1000)

print("=== Full Service ===")
full_service = FullInvoiceService()
full_service.calculate_total(invoice)
full_service.save_to_database(invoice)
full_service.send_email(invoice)

print("\n=== ReadOnly Service ===")
readonly_service = ReadOnlyInvoiceService()
readonly_service.calculate_total(invoice)
try:
    readonly_service.save_to_database(invoice)
except NotImplementedError as e:
    print(f"ERROR: {e}")

print("\n=== Email Only Service ===")
email_service = EmailOnlyInvoiceService()
email_service.send_email(invoice)
try:
    email_service.calculate_total(invoice)
except NotImplementedError as e:
    print(f"ERROR: {e}")
