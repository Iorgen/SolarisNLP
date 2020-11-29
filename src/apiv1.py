from flask import Blueprint
from flask_restplus import Api
from api.api_v1.recognizer.endpoints import api as recognizer_namespace

blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api = Api(
    blueprint,
    version="2.0",
    title="Intellegent Science Employee search v1.0",
    description="Face detection",
    doc='/docs',
    default='',
    default_label='')

api.add_namespace(recognizer_namespace)
