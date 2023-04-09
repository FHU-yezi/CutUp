from sanic import Blueprint

from api.v1 import bp_v1

bp_api = Blueprint.group(bp_v1, url_prefix="/api")
