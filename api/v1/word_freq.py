from typing import Dict, Literal, Set

from pydantic import ValidationError
from sanic import BadRequest, Blueprint, HTTPResponse, Request
from sspeedup.api import CODE, sanic_response_json

from utils.pydantic_base import BaseModel
from utils.word_split import jieba_posseg_spliter, jieba_search_spliter, jieba_spliter

bp_word_freq = Blueprint("word_freq", url_prefix="/word_freq")


class NormalHandlerRequest(BaseModel):
    library: Literal["jieba"]
    text: str


class NormalHandlerResponse(BaseModel):
    word_freq: Dict[str, int]


@bp_word_freq.post("/normal")
def normal_handler(request: Request) -> HTTPResponse:
    try:
        request_data = NormalHandlerRequest.parse_obj(request.json)
    except BadRequest:
        return sanic_response_json(code=CODE.UNKNOWN_DATA_FORMAT)
    except ValidationError:
        return sanic_response_json(code=CODE.BAD_ARGUMENTS)

    word_freq = dict(jieba_spliter.get_word_freq(request_data.text))

    return sanic_response_json(
        code=CODE.SUCCESS,
        data=NormalHandlerResponse(word_freq=word_freq).dict(),
    )


class SearchHandlerRequest(BaseModel):
    library: Literal["jieba"]
    text: str


class SearchHandlerResponse(BaseModel):
    word_freq: Dict[str, int]


@bp_word_freq.post("/search")
def search_handler(request: Request) -> HTTPResponse:
    try:
        request_data = SearchHandlerRequest.parse_obj(request.json)
    except BadRequest:
        return sanic_response_json(code=CODE.UNKNOWN_DATA_FORMAT)
    except ValidationError:
        return sanic_response_json(code=CODE.BAD_ARGUMENTS)

    word_freq = dict(jieba_search_spliter.get_word_freq(request_data.text))

    return sanic_response_json(
        code=CODE.SUCCESS,
        data=SearchHandlerResponse(word_freq=word_freq).dict(),
    )


class PossegHandlerRequest(BaseModel):
    library: Literal["jieba"]
    text: str
    allow_word_types: Set[str] = set()


class PossegHandlerResponse(BaseModel):
    word_freq: Dict[str, int]


@bp_word_freq.post("/posseg")
def posseg_handler(request: Request) -> HTTPResponse:
    try:
        request_data = PossegHandlerRequest.parse_obj(request.json)
    except BadRequest:
        return sanic_response_json(code=CODE.UNKNOWN_DATA_FORMAT)
    except ValidationError:
        return sanic_response_json(code=CODE.BAD_ARGUMENTS)

    if request_data.allow_word_types:
        jieba_posseg_spliter.set_allowed_word_type(request_data.allow_word_types)
    else:
        jieba_posseg_spliter.set_allowed_word_types_file(
            "word_split_assets/posseg_default_allow_types.txt"
        )
    word_freq = dict(jieba_posseg_spliter.get_word_freq(request_data.text))

    return sanic_response_json(
        code=CODE.SUCCESS,
        data=PossegHandlerResponse(word_freq=word_freq).dict(),
    )
