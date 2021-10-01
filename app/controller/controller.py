from flask.blueprints import Blueprint
from .blueprints.getRisk import getRisk

api = Blueprint('api',__name__)

api.register_blueprint(getRisk,url_prefix='/data')
