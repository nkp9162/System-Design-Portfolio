class Invoice:
    def __init__(self, customer_name, amount, is_locked=False):
        self.customer_name = customer_name
        self.amount = amount
        self.is_locked = is_locked


class InvoiceProcessor:
    def can_process(self, invoice: Invoice) -> bool:
        return True
    
    def process(self, invoice: Invoice) -> float:
        if not self.can_process(invoice):
            return 0.0
        
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"Processing invoice for {invoice.customer_name}")
        print(f"Amount: {invoice.amount}, Tax: 18%, Total: {total}")
        return total


class RegularInvoiceProcessor(InvoiceProcessor):
    def can_process(self, invoice: Invoice) -> bool:
        return not invoice.is_locked
    
    def process(self, invoice: Invoice) -> float:
        if not self.can_process(invoice):
            print(f"[Regular] Invoice for {invoice.customer_name} is locked, skipping")
            return 0.0
        
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"[Regular] Processing invoice for {invoice.customer_name}")
        print(f"Amount: {invoice.amount}, Tax: 18%, Total: {total}")
        return total


class FinalInvoiceProcessor(InvoiceProcessor):
    def can_process(self, invoice: Invoice) -> bool:
        return invoice.is_locked
    
    def process(self, invoice: Invoice) -> float:
        if not self.can_process(invoice):
            print(f"[Final] Invoice for {invoice.customer_name} is not finalized yet, skipping")
            return 0.0
        
        print(f"[Final] Invoice for {invoice.customer_name} is locked")
        print(f"Final Amount: {invoice.amount}")
        return invoice.amount


class ZeroAmountInvoiceProcessor(InvoiceProcessor):
    def can_process(self, invoice: Invoice) -> bool:
        return invoice.amount >= 0
    
    def process(self, invoice: Invoice) -> float:
        if invoice.amount == 0:
            print(f"[Zero Amount] Invoice for {invoice.customer_name} has zero amount")
            return 0.0
        
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"[Zero Amount] Processing invoice for {invoice.customer_name}")
        print(f"Amount: {invoice.amount}, Tax: 18%, Total: {total}")
        return total


def generate_report(processor: InvoiceProcessor, invoices: list):
    print("\n=== Generating Report ===")
    total_revenue = 0.0
    
    for invoice in invoices:
        total = processor.process(invoice)
        total_revenue += total
    
    print(f"Total Revenue: {total_revenue}")
    return total_revenue


invoice1 = Invoice("Nirbhay", 1000, is_locked=False)
invoice2 = Invoice("Rahul", 2000, is_locked=False)
invoice3 = Invoice("Priya", 0, is_locked=False)
invoice4 = Invoice("Amit", 1500, is_locked=True)

print("=== Test 1: Regular Processor ===")
regular_processor = RegularInvoiceProcessor()
generate_report(regular_processor, [invoice1, invoice2])

print("\n=== Test 2: Final Processor ===")
final_processor = FinalInvoiceProcessor()
generate_report(final_processor, [invoice4, invoice1])

print("\n=== Test 3: Zero Amount Processor ===")
zero_processor = ZeroAmountInvoiceProcessor()
generate_report(zero_processor, [invoice3, invoice1])

print("\n=== Test 4: Mixed Invoices with Regular Processor ===")
generate_report(regular_processor, [invoice1, invoice4, invoice3])
