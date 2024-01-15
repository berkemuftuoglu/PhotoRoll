from app.models import Customer, Service, Bill, BillLineItem, Company
from sqlalchemy import func, extract
from datetime import datetime
from app.funcs.db_queries import *

def serialize_date(date):
    if isinstance(date, datetime):
        return date.isoformat()
    return date

def get_revenue_over_time():
    results = get_revenue_over_time_data()

    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    data = [
            {
                "date": f"{month_names[row[1]]}, {row[0]}",
                "revenue": float(row[2] or 0)
            } for row in results
    ]
    return data

def get_service_popularity():
    results = get_service_popularity_data()
    data = [
        {
            "service_name": row[0],
            "count": row[1]
            } for row in results
    ]
    return data

def get_customer_segmentation():
    results = get_customer_segmentation_data()
    data = [
        {
            "customer_name": row[0],
            "bill_count": row[1]
        } for row in results
    ]
    return data

