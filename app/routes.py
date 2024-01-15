from weasyprint import HTML
from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
import json
from sqlalchemy.orm import joinedload
from datetime import datetime

import os

from app.funcs.email_funcs import *
from app.funcs.pdf_funcs import *
from app.funcs.chart_funcs import *

@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/dashboard', endpoint='dashboard')
def index():
    revenue_json = get_revenue_over_time()
    service_json = get_service_popularity()
    customer_json = get_customer_segmentation()

    return render_template(
        'dashboard.html',
        revenue_json=revenue_json,
        service_json=service_json,
        customer_json=customer_json,
    )


@app.route('/invoices', endpoint='invoices')
def invoices():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    paginated_invoices = Bill.query.options(
        joinedload(Bill.customer)
    ).paginate(page, per_page, error_out=False)

    return render_template('invoices.html', invoices=paginated_invoices.items, pagination=paginated_invoices)


@app.route('/createinvoice', endpoint='createinvoice')
def createinvoice():
    services = get_services()
    customers = get_customers()
    companies = get_companies()
    return render_template('createinvoice.html', services=services, customers=customers, companies=companies)


###### CUSTOMERS ######
@app.route('/customers', methods=['GET'])
def customers():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    paginated_customers = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('customers.html', customers=paginated_customers.items, pagination=paginated_customers)

@app.route('/update_customer', methods=['POST'])
def update_customer():
    data = request.get_json()
    customer = Customer.query.get(data['id'])
    if customer:
        customer.email = data['email']
        customer.name = data['name']
        if data['company_name']:
            company = Company.query.filter_by(name=data['company_name']).first()
            if not company:
                company = Company(name=data['company_name'], company_number=data['company_number'])
                db.session.add(company)
                db.session.flush()
            customer.company_id = company.id
        customer.address = data['address']
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'})
    return jsonify({'message': 'Customer not found'}), 404
###### CUSTOMERS ######

###### SERVICES ######
@app.route('/services', endpoint='services')
def services():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    paginated_services = Service.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('services.html', services=paginated_services.items, pagination=paginated_services)


@app.route('/update_service', methods=['POST'])
def update_service():
    data = request.json
    service = Service.query.get(data['id'])
    if service:
        service.name = data['name']
        service.description = data['description']
        db.session.commit()
        return jsonify({"message": "Service updated successfully"}), 200
    return jsonify({"message": "Service not found"}), 404
###### SERVICES ######

@app.route('/generatepdf', methods=['POST'])
def generatepdf():
    data = request.get_json()
    
    # Extract company and customer data
    company = data['company']
    customer = data['customer']


    global bill_number1
    bill_number1 = invoice_id_generator()


    total_amount = 0
    for item in data['line_items']:
        item['line_total'] = item['quantity'] * item['unit_price']
        total_amount += item['line_total']

    bill = {
        'bill_number': bill_number1,
        'bill_date': datetime.utcnow().strftime('%Y-%m-%d'),
        'due_date': data['invoice']['due_date'],
        'total_amount': total_amount
    }

    user_data = getusersettings()
    rendered_html = render_template('invoice_template.html',
                                    company=company,
                                    customer=customer,
                                    bill=bill,
                                    line_items=data['line_items'],
                                    bank_details=user_data
                                    )
    pdf = HTML(string=rendered_html).write_pdf()

    invoices_dir = os.path.join(app.static_folder, 'invoices')

    pdf_filename = f"invoice_{bill['bill_number']}.pdf"
    pdf_file_path = os.path.join(invoices_dir, pdf_filename)
    with open(pdf_file_path, 'wb') as f:
        f.write(pdf)

    pdf_url = url_for('static', filename=f'invoices/{pdf_filename}')

    return jsonify({'pdfPath': pdf_url})


def record_invoice(data):
    company_data = data['formData']['company']
    customer_data = data['formData']['customer']
    invoice_data = data['formData']['invoice']
    line_items_data = data['formData']['line_items']
    pdf_path = convert_url_to_file_path(data['attachmentPath'])

    bill = Bill(
        bill_number = bill_number1,
        customer_id=customer_data['id'],
        bill_date=datetime.utcnow(),
        due_date=datetime.strptime(invoice_data['due_date'], '%Y-%m-%d'),
        pdf_path=pdf_path
    )

    for item in line_items_data:
        line_item = BillLineItem(
            bill=bill,
            service_id=item['service_id'],
            quantity=item['quantity'],
            unit_price=item['unit_price']
        )
        db.session.add(line_item)

    db.session.add(bill)
    db.session.commit()


@app.route('/sendinvoice', methods=['POST'])
def sendinvoice():
    data = request.get_json()
    record_invoice(data)
    path = convert_url_to_file_path(data['attachmentPath'])

    send_email_with_attachment(
        smtp_host='smtp.gmail.com',
        smtp_port=465,
        username='',
        password='',
        subject=data['subject'],
        body=data['body'],
        recipient=data['recipient'],
        attachment_path=path
    )
    return jsonify({"message": "Email sent successfully!"})


def getusersettings():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'userdata.json')

    user_data = {
        'name': '',
        'sort_code': '',
        'account_number': ''
    }

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if data:
                user_data = data[0]
    return user_data


@app.route('/usersettings')
def usersettings():
    user_data = getusersettings()
    return render_template('usersettings.html', user_data=user_data)



@app.route('/edituserdata', methods=['POST'])
def edituserdata():
    name = request.form.get('name')
    sort_code = request.form.get('sort_code')
    account_number = request.form.get('account_number')

    user_data = {
        'name': name,
        'sort_code': sort_code,
        'account_number': account_number
    }

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'userdata.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            data[0] = user_data
    else:
        data = [user_data]

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    return redirect(url_for('index'))