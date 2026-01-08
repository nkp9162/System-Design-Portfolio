from abc import ABC, abstractmethod

class Invoice:
    def __init__(self, customer_name, amount):
        self.customer_name = customer_name
        self.amount = amount


class InvoiceCalculator(ABC):
    @abstractmethod
    def calculate_total(self, invoice: Invoice) -> float:
        pass


class InvoicePersistence(ABC):
    @abstractmethod
    def save_to_database(self, invoice: Invoice):
        pass


class InvoiceEmailNotification(ABC):
    @abstractmethod
    def send_email(self, invoice: Invoice):
        pass


class InvoicePDFGenerator(ABC):
    @abstractmethod
    def generate_pdf(self, invoice: Invoice):
        pass


class InvoiceSMSNotification(ABC):
    @abstractmethod
    def send_sms(self, invoice: Invoice):
        pass


class FullInvoiceService(
    InvoiceCalculator,
    InvoicePersistence,
    InvoiceEmailNotification,
    InvoicePDFGenerator,
    InvoiceSMSNotification
):
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


class ReadOnlyInvoiceService(InvoiceCalculator):
    def calculate_total(self, invoice: Invoice) -> float:
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"[ReadOnly] Calculated total: {total}")
        return total


class EmailOnlyInvoiceService(InvoiceEmailNotification):
    def send_email(self, invoice: Invoice):
        print(f"[Email Only] Email sent to {invoice.customer_name}")


class InvoiceNotificationService(
    InvoiceEmailNotification,
    InvoiceSMSNotification
):
    def send_email(self, invoice: Invoice):
        print(f"[Notification] Email sent to {invoice.customer_name}")

    def send_sms(self, invoice: Invoice):
        print(f"[Notification] SMS sent to {invoice.customer_name}")


class InvoiceReportService(
    InvoiceCalculator,
    InvoicePDFGenerator
):
    def calculate_total(self, invoice: Invoice) -> float:
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"[Report] Calculated total: {total}")
        return total

    def generate_pdf(self, invoice: Invoice):
        print(f"[Report] PDF generated for {invoice.customer_name}")


invoice = Invoice("Nirbhay", 1000)

print("=== Full Service ===")
full_service = FullInvoiceService()
full_service.calculate_total(invoice)
full_service.save_to_database(invoice)
full_service.send_email(invoice)

print("\n=== ReadOnly Service ===")
readonly_service = ReadOnlyInvoiceService()
readonly_service.calculate_total(invoice)

print("\n=== Email Only Service ===")
email_service = EmailOnlyInvoiceService()
email_service.send_email(invoice)

print("\n=== Notification Service ===")
notification_service = InvoiceNotificationService()
notification_service.send_email(invoice)
notification_service.send_sms(invoice)

print("\n=== Report Service ===")
report_service = InvoiceReportService()
report_service.calculate_total(invoice)
report_service.generate_pdf(invoice)
