from flask import Flask, render_template, make_response, url_for
import os
from flask import request
from app.models import *


def get_services():
    services = Service.query.all()
    return [
        {
            "id": service.id,
            "name": service.name,
            "description": service.description
        } for service in services
    ]


def get_customers():
    customers = Customer.query.all()
    return [
        {
            "id": customer.id,
            "email": customer.email,
            "name": customer.name,
            "company_id": customer.company.name if customer.company else None,
            "company_number": customer.company.company_number if customer.company else None,
            "address": customer.address
        } for customer in customers
    ]

def get_companies():
    companies = Company.query.all()
    return [
        {
            "id": company.id,
            "name": company.name,
            "company_number": company.company_number,
            "address": company.address
        } for company in companies]
