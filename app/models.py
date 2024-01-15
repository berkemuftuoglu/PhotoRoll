from app import db
from datetime import datetime
import time
import random

def invoice_id_generator():
    prefix = '1701869'
    timestamp = int(time.time() * 1000000)
    random_component = random.randint(100, 999)
    return prefix + str(timestamp) + str(random_component)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    company_number = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String)

    customers = db.relationship('Customer', backref='company', lazy=True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    address = db.Column(db.String, nullable=True)

  

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_number = db.Column(db.String, unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    bill_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pdf_path = db.Column(db.String)

    customer = db.relationship('Customer', backref='bills')

    @property
    def status(self):
        if self.due_date and datetime.utcnow() > self.due_date:
            return 'Overdue'
        else:
            return 'Pending'

    line_items = db.relationship('BillLineItem', backref='bill', lazy=True, cascade="all, delete-orphan")

    @property
    def total_amount(self):
        return sum(item.line_total for item in self.line_items)


class BillLineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    @property
    def line_total(self):
        return self.quantity * self.unit_price
