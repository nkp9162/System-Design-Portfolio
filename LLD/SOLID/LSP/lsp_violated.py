class Invoice:
    def __init__(self, customer_name, amount):
        self.customer_name = customer_name
        self.amount = amount


class InvoiceProcessor:
    """Base class for processing invoices"""
    
    def process(self, invoice: Invoice):
        """Process the invoice and return total"""
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"Processing invoice for {invoice.customer_name}")
        print(f"Amount: {invoice.amount}, Tax: 18%, Total: {total}")
        return total


class RegularInvoiceProcessor(InvoiceProcessor):
    """Handles regular invoices - works fine"""
    
    def process(self, invoice: Invoice):
        tax = 0.18
        total = invoice.amount + (invoice.amount * tax)
        print(f"[Regular] Processing invoice for {invoice.customer_name}")
        print(f"Amount: {invoice.amount}, Tax: 18%, Total: {total}")
        return total


class FinalInvoiceProcessor(InvoiceProcessor):
    """
    Handles final/locked invoices
    Problem: This violates LSP!
    Cannot be substituted for base class because it raises exception
    """
    
    def process(self, invoice: Invoice):
        # Violation: Changes behavior in unexpected way
        raise Exception("Final invoices cannot be processed! They are locked.")


class ZeroAmountInvoiceProcessor(InvoiceProcessor):
    """
    Handles zero amount invoices
    Problem: This violates LSP!
    Returns None instead of a number, breaking contract
    """
    
    def process(self, invoice: Invoice):
        if invoice.amount == 0:
            print(f"[Zero Amount] Invoice for {invoice.customer_name} has zero amount")
            # Violation: Returns None instead of total (breaks return type contract)
            return None
        return invoice.amount


def generate_report(processor: InvoiceProcessor, invoices: list):
    """
    This function expects any InvoiceProcessor
    But it breaks when using FinalInvoiceProcessor or ZeroAmountInvoiceProcessor!
    """
    print("\n=== Generating Report ===")
    total_revenue = 0
    
    for invoice in invoices:
        try:
            # This will crash for FinalInvoiceProcessor
            total = processor.process(invoice)
            
            # This will crash for ZeroAmountInvoiceProcessor (None + number)
            total_revenue += total
            
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    print(f"Total Revenue: {total_revenue}")
    return total_revenue



invoice1 = Invoice("Nirbhay", 1000)
invoice2 = Invoice("Rahul", 2000)
invoice3 = Invoice("Priya", 0)

print("=== Test 1: Regular Processor (Works Fine) ===")
regular_processor = RegularInvoiceProcessor()
generate_report(regular_processor, [invoice1, invoice2])

print("\n=== Test 2: Final Processor (BREAKS!) ===")
final_processor = FinalInvoiceProcessor()
generate_report(final_processor, [invoice1, invoice2])  # Crashes!

print("\n=== Test 3: Zero Amount Processor (BREAKS!) ===")
zero_processor = ZeroAmountInvoiceProcessor()
generate_report(zero_processor, [invoice3, invoice1])  # Crashes with None!

# Problem: Child classes cannot substitute parent class without breaking functionality