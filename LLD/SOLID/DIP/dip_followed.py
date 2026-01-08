from abc import ABC, abstractmethod

class Invoice:
    def __init__(self, customer_name, amount):
        self.customer_name = customer_name
        self.amount = amount

class InvoiceRepository(ABC):
    @abstractmethod
    def save(self, invoice: Invoice):
        pass

class NotificationService(ABC):
    @abstractmethod
    def notify(self, invoice: Invoice):
        pass

class MySQLRepository(InvoiceRepository):
    def save(self, invoice: Invoice):
        print(f"[MySQL] Saving invoice for {invoice.customer_name} to MySQL database")
        print(f"[MySQL] INSERT INTO invoices VALUES ('{invoice.customer_name}', {invoice.amount})")

class MongoDBRepository(InvoiceRepository):
    def save(self, invoice: Invoice):
        print(f"[MongoDB] Saving invoice for {invoice.customer_name} to MongoDB")
        print(f"[MongoDB] db.invoices.insert({{customer: '{invoice.customer_name}', amount: {invoice.amount}}})")


class PostgreSQLRepository(InvoiceRepository):
    def save(self, invoice: Invoice):
        print(f"[PostgreSQL] Saving invoice for {invoice.customer_name} to PostgreSQL")
        print(f"[PostgreSQL] INSERT INTO invoices VALUES ('{invoice.customer_name}', {invoice.amount})")


class EmailNotificationService(NotificationService):
    def notify(self, invoice: Invoice):
        print(f"[Email] Sending invoice email to {invoice.customer_name}")
        print(f"[Email] Subject: Invoice for ${invoice.amount}")


class SMSNotificationService(NotificationService):
    def notify(self, invoice: Invoice):
        print(f"[SMS] Sending invoice SMS to {invoice.customer_name}")
        print(f"[SMS] Your invoice of ${invoice.amount} has been processed")


class SlackNotificationService(NotificationService):
    def notify(self, invoice: Invoice):
        print(f"[Slack] Posting invoice notification for {invoice.customer_name}")
        print(f"[Slack] Invoice amount: ${invoice.amount}")


class InvoiceProcessor:
    def __init__(self, repository: InvoiceRepository, notification: NotificationService):
        self.repository = repository
        self.notification = notification

    def process_invoice(self, invoice: Invoice):
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"\n[Processor] Processing invoice for {invoice.customer_name}")
        print(f"[Processor] Amount: {invoice.amount}, Tax: 18%, Total: {total}")

        self.repository.save(invoice)
        self.notification.notify(invoice)


invoice1 = Invoice("Nirbhay", 1000)
invoice2 = Invoice("Rahul", 2000)
invoice3 = Invoice("Priya", 1500)

print("=== Scenario 1: MySQL + Email ===")
processor1 = InvoiceProcessor(
    repository=MySQLRepository(),
    notification=EmailNotificationService()
)
processor1.process_invoice(invoice1)

print("\n=== Scenario 2: MongoDB + SMS ===")
processor2 = InvoiceProcessor(
    repository=MongoDBRepository(),
    notification=SMSNotificationService()
)
processor2.process_invoice(invoice2)

print("\n=== Scenario 3: PostgreSQL + Slack ===")
processor3 = InvoiceProcessor(
    repository=PostgreSQLRepository(),
    notification=SlackNotificationService()
)
processor3.process_invoice(invoice3)

print("\n=== Scenario 4: MongoDB + Email ===")
processor4 = InvoiceProcessor(
    repository=MongoDBRepository(),
    notification=EmailNotificationService()
)
processor4.process_invoice(invoice1)
