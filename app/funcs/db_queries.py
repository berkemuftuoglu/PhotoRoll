from app import db
from app.models import *
from sqlalchemy import func, extract

'''Get all'''

def get_all_services():
    return Service.query.all()

def get_all_companies():
    return Company.query.all()

def get_all_customers():
    return Customer.query.all()

def get_all_bills():
    return Bill.query.all()

'''For charts'''
def get_revenue_over_time_data():
    results = db.session.query(
            extract('year', Bill.bill_date).label('year'),
            extract('month', Bill.bill_date).label('month'),
            func.sum(BillLineItem.unit_price * BillLineItem.quantity).label('total')
        ).join(BillLineItem).group_by('year', 'month').all()

    return results

def get_service_popularity_data():
    results = results = db.session.query(Service.name, func.count(BillLineItem.service_id)).join(BillLineItem).group_by(Service.name).all()
    return results

def get_customer_segmentation_data():
    results = db.session.query(
        Customer.name, func.count(Bill.id)
    ).join(Bill, Bill.customer_id == Customer.id) \
     .group_by(Customer.name) \
     .all()
    return results
