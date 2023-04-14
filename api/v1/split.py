from typing import Literal, Set, Tuple

from pydantic import ValidationError
from sanic import BadRequest, Blueprint, HTTPResponse, Request
from sspeedup.api import CODE, sanic_response_json

from utils.pydantic_base import BaseModel
from utils.word_split import jieba_posseg_spliter, jieba_search_spliter, jieba_spliter

bp_split = Blueprint("split", url_prefix="/split")


class NormalHandlerRequest(BaseModel):
    library: Literal["jieba"]
    text: str


class NormalHandlerResponse(BaseModel):
    splitted_text: Tuple


@bp_split.post("/normal")
def normal_handler(request: Request) -> HTTPResponse:
    try:
        request_data = NormalHandlerRequest.parse_obj(request.json)
    except BadRequest:
        return sanic_response_json(code=CODE.UNKNOWN_DATA_FORMAT)
    except ValidationError:
        return sanic_response_json(code=CODE.BAD_ARGUMENTS)

    splitted_text = tuple(jieba_spliter.split(request_data.text))

    return sanic_response_json(
        code=CODE.SUCCESS,
        data=NormalHandlerResponse(splitted_text=splitted_text).dict(),
    )


class SearchHandlerRequest(BaseModel):
    library: Literal["jieba"]
    text: str


class SearchHandlerResponse(BaseModel):
    splitted_text: Tuple


@bp_split.post("/search")
def search_handler(request: Request) -> HTTPResponse:
    try:
        request_data = SearchHandlerRequest.parse_obj(request.json)
    except BadRequest:
        return sanic_response_json(code=CODE.UNKNOWN_DATA_FORMAT)
    except ValidationError:
        return sanic_response_json(code=CODE.BAD_ARGUMENTS)

    splitted_text = tuple(jieba_search_spliter.split(request_data.text))

    return sanic_response_json(
        code=CODE.SUCCESS,
        data=SearchHandlerResponse(splitted_text=splitted_text).dict(),
    )


class PossegHandlerRequest(BaseModel):
    library: Literal["jieba"]
    text: str
    allowed_word_types: Set[str] = set()


class PossegHandlerResponse(BaseModel):
    splitted_text: Tuple


@bp_split.post("/posseg")
def posseg_handler(request: Request) -> HTTPResponse:
    try:
        request_data = PossegHandlerRequest.parse_obj(request.json)
    except BadRequest:
        return sanic_response_json(code=CODE.UNKNOWN_DATA_FORMAT)
    except ValidationError:
        return sanic_response_json(code=CODE.BAD_ARGUMENTS)

    if request_data.allowed_word_types:
        jieba_posseg_spliter.set_allowed_word_type(request_data.allowed_word_types)
    else:
        jieba_posseg_spliter.set_allowed_word_types_file(
            "word_split_assets/posseg_default_allow_types.txt"
        )
    splitted_text = tuple(jieba_posseg_spliter.split(request_data.text))

    return sanic_response_json(
        code=CODE.SUCCESS,
        data=PossegHandlerResponse(splitted_text=splitted_text).dict(),
    )
