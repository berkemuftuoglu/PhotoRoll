import os
from app import db
from app.models import Customer, Service, Company, Bill, BillLineItem
from datetime import datetime, timedelta
import random

# Function to generate dummy data
def generate_dummy_data():
    # Create a dummy 'Other' company, customer, and service
    other_company = Company(name="Other", company_number="000000", address=None)
    db.session.add(other_company)

    other_customer = Customer(email="other@example.com", name="Other", company_id=None, address=None)
    db.session.add(other_customer)

    other_service = Service(name="Other", description=None)
    db.session.add(other_service)

    # Create dummy companies
    for i in range(5):  # Reduced to 5 companies
        company = Company(name=f"Company {i}", company_number=f"1234560{i}", address=f"100{i} Main St")
        db.session.add(company)

    # Create dummy customers
    for i in range(5):  # Reduced to 5 customers
        customer = Customer(email=f"customer{i}@example.com", name=f"Customer {i}", company_id=random.choice([1, None]))  # Use either a real company or 'None'
        db.session.add(customer)

    # Create dummy services
    for i in range(5):  # Reduced to 5 services
        service = Service(name=f"Service {i}", description=f"Description for service {i}")
        db.session.add(service)

    db.session.commit()

    # Create dummy bills and line items
    for i in range(5):  # Reduced to 5 bills
        bill = Bill(customer_id=random.randint(1, 6), bill_date=datetime.now(), due_date=datetime.now() + timedelta(days=30), pdf_path=f"invoice_{i}.pdf")
        db.session.add(bill)
        db.session.flush()  # Flush to get the bill id for line items

        for _ in range(random.randint(1, 3)):  # Each bill has 1 to 3 line items
            line_item = BillLineItem(bill_id=bill.id, service_id=random.randint(1, 6), quantity=random.randint(1, 10), unit_price=random.uniform(10.0, 100.0))
            db.session.add(line_item)

    db.session.commit()

# Create the database and tables
db.create_all()

# Generate and populate with dummy data
generate_dummy_data()

print("Database populated with dummy data.")
