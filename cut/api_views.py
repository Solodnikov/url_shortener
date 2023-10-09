from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    original_url = URLMap.get_or_404(short)

    return jsonify(original_url.url_to_dict()), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    url_map = URLMap.from_dict(data)
    url_map.save()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
