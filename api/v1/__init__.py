from sanic import Blueprint

from api.v1.split import bp_split
from api.v1.word_freq import bp_word_freq

bp_v1 = Blueprint.group(bp_split, bp_word_freq, url_prefix="/v1")
