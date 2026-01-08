class Invoice:
    def __init__(self, customer_name, amount):
        self.customer_name = customer_name
        self.amount = amount

    def calculate_total(self):
        tax = 0.18
        total = self.amount + (self.amount * tax)
        print(f"Calculated total with tax: {total}")
        return total

    def save_to_database(self):
        print("Invoice saved to database")

    def send_email(self):
        print(f"Invoice email sent to {self.customer_name}")


invoice = Invoice("Nirbhay", 1000)

total = invoice.calculate_total()
invoice.save_to_database()
invoice.send_email()
