from flask_restful import Resource
from app.models import Bill, BillLineItem, Customer, Service
from app.funcs.chart_funcs import *

class RevenueAPI(Resource):
    def get(self):
        revenue_data = get_revenue_over_time()
        return revenue_data

class ServicePopularityAPI(Resource):
    def get(self):
        service_popularity_data = get_service_popularity()
        return service_popularity_data

class CustomerSegmentationAPI(Resource):
    def get(self):
        customers = get_customer_segmentation()
        return customers
