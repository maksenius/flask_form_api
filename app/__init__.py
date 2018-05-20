from flask_restful import Api

from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# initialize db
db = SQLAlchemy()


def create_app(config_name):
    """ Create app for run Flask."""

    # import model
    from app.models import Form, Field, IntegerField, StringField, DateField
    # import api views
    from app.api.v0.views import FormView, FormDetailView, FieldView, FormSubmitView

    app = Flask(__name__)

    api = Api(app)

    # urls
    api.add_resource(FormView, '/api/v0/form')
    api.add_resource(FormDetailView, '/api/v0/form/<int:id>')
    api.add_resource(FieldView, '/api/v0/field')
    api.add_resource(FormSubmitView, '/api/v0/form/<int:id>/submit')

    app.config.from_object(app_config.get(config_name))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app
