from sanic import Blueprint

from api.v1.freq import bp_freq
from api.v1.split import bp_split

bp_v1 = Blueprint.group(bp_split, bp_freq, url_prefix="/v1")
