from flask.blueprints import Blueprint
from ...utils.utils import getRisk3ndComplete
from ...constants.constants import constantsRegions
from flask import request
import json

getRisk = Blueprint('getRisk', __name__)


@getRisk.route('getRisk', methods=['POST'])
def getRiskF():
    body = request.json

    city = body['city']  # type: ignore
    dose = body['dose']  # type: ignore
    brand = body['brand']  # type: ignore
    covidBefore = body['brand'] == 1 # type: ignore

    if city in constantsRegions:
        return json.dumps({'result': getRisk3ndComplete(city, dose, brand, covidBefore)})
    else:
        return json.dumps({'error': 'city not recognised'})
