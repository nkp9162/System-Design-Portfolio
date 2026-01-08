from abc import ABC, abstractmethod

class Invoice:
    def __init__(self, customer_name, amount):
        self.customer_name = customer_name
        self.amount = amount


class InvoiceRepository(ABC):
    @abstractmethod
    def save(self, invoice: Invoice):
        pass


class MySQLInvoiceRepository(InvoiceRepository):
    def save(self, invoice: Invoice):
        print(f"[MySQL] Saving invoice for {invoice.customer_name}")
        print(f"[MySQL] INSERT INTO invoices VALUES ('{invoice.customer_name}', {invoice.amount})")


class MongoDBInvoiceRepository(InvoiceRepository):
    def save(self, invoice: Invoice):
        print(f"[MongoDB] Saving invoice for {invoice.customer_name}")
        print(f"[MongoDB] db.invoices.insert({{customer: '{invoice.customer_name}', amount: {invoice.amount}}})")


class PostgreSQLInvoiceRepository(InvoiceRepository):
    def save(self, invoice: Invoice):
        print(f"[PostgreSQL] Saving invoice for {invoice.customer_name}")
        print(f"[PostgreSQL] INSERT INTO invoices VALUES ('{invoice.customer_name}', {invoice.amount})")


class RedisInvoiceRepository(InvoiceRepository):
    def save(self, invoice: Invoice):
        print(f"[Redis] Saving invoice for {invoice.customer_name}")
        print(f"[Redis] SET invoice:{invoice.customer_name} '{invoice.amount}'")


invoice1 = Invoice("Nirbhay", 1000)
invoice2 = Invoice("Rahul", 2000)
invoice3 = Invoice("Priya", 1500)
invoice4 = Invoice("Amit", 3000)

mysql_repo = MySQLInvoiceRepository()
mysql_repo.save(invoice1)

mongodb_repo = MongoDBInvoiceRepository()
mongodb_repo.save(invoice2)

postgres_repo = PostgreSQLInvoiceRepository()
postgres_repo.save(invoice3)

redis_repo = RedisInvoiceRepository()
redis_repo.save(invoice4)
