class Invoice:
    def __init__(self, customer_name, amount):
        self.customer_name = customer_name
        self.amount = amount


class InvoiceRepository:
    """
    Problem: This class violates OCP
    Every time we need to support a new database,
    we have to MODIFY this class by adding new if-elif conditions.
    """
    
    def __init__(self, db_type):
        self.db_type = db_type
    
    def save(self, invoice: Invoice):
        """
        Violation: Adding new database requires modifying this method
        """
        if self.db_type == "mysql":
            print(f"[MySQL] Saving invoice for {invoice.customer_name}")
            print(f"[MySQL] INSERT INTO invoices VALUES ('{invoice.customer_name}', {invoice.amount})")
        
        elif self.db_type == "mongodb":
            print(f"[MongoDB] Saving invoice for {invoice.customer_name}")
            print(f"[MongoDB] db.invoices.insert({{customer: '{invoice.customer_name}', amount: {invoice.amount}}})")
        
        elif self.db_type == "postgresql":
            print(f"[PostgreSQL] Saving invoice for {invoice.customer_name}")
            print(f"[PostgreSQL] INSERT INTO invoices VALUES ('{invoice.customer_name}', {invoice.amount})")
        
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")



invoice1 = Invoice("Nirbhay", 1000)
invoice2 = Invoice("Rahul", 2000)
invoice3 = Invoice("Priya", 1500)

mysql_repo = InvoiceRepository("mysql")
mysql_repo.save(invoice1)

mongodb_repo = InvoiceRepository("mongodb")
mongodb_repo.save(invoice2)

postgres_repo = InvoiceRepository("postgresql")
postgres_repo.save(invoice3)

# Problem: If we want to add Redis, we need to modify InvoiceRepository class!