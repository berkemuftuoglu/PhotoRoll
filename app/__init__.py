from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

#Config details
app = Flask(__name__)
app.config.from_object(Config)

#Database
db = SQLAlchemy(app)
db.create_all()

#API
api = Api(app)

from app.resources import *

api.add_resource(RevenueAPI, '/api/revenue')
api.add_resource(ServicePopularityAPI, '/api/service-popularity')
api.add_resource(CustomerSegmentationAPI, '/api/customer-segmentation')


from app import routes
