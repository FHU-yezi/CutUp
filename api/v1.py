from dataclasses import asdict

from sanic import Blueprint, HTTPResponse, Request
from sspeedup.api import CODE, sanic_response_json

from models import GetWordFreqRequest, GetWordFreqResponse, SplitRequest, SplitResponse
from utils.word_split import jieba_posseg_spliter, jieba_search_spliter, jieba_spliter

v1 = Blueprint("v1", url_prefix="/v1")


@v1.post("/split")
def split_handler(request: Request) -> HTTPResponse:
    try:
        request_json = SplitRequest(**request.json)
    except TypeError:
        return sanic_response_json(code=CODE.MISSED_ARGUMENTS_OR_BAD_TYPES)

    if request_json.library != "jieba":
        return sanic_response_json(
            code=CODE.ARGUMENTS_CHECK_FAILED,
            message="库名称无效",
        )
    if request_json.variant not in ("normal", "search", "posseg"):
        return sanic_response_json(
            code=CODE.ARGUMENTS_CHECK_FAILED,
            message="变种名称无效",
        )

    if request_json.variant == "normal":
        data = SplitResponse(text=tuple(jieba_spliter.split(request_json.text)))
    elif request_json.variant == "search":
        data = SplitResponse(text=tuple(jieba_search_spliter.split(request_json.text)))
    elif request_json.variant == "posseg":
        data = SplitResponse(text=tuple(jieba_posseg_spliter.split(request_json.text)))
    else:
        raise ValueError

    return sanic_response_json(code=CODE.SUCCESS, data=asdict(data))


@v1.post("/get_word_freq")
def get_word_freq_handler(request: Request) -> HTTPResponse:
    try:
        request_json = GetWordFreqRequest(**request.json)
    except TypeError:
        return sanic_response_json(code=CODE.MISSED_ARGUMENTS_OR_BAD_TYPES)

    if request_json.library != "jieba":
        return sanic_response_json(
            code=CODE.ARGUMENTS_CHECK_FAILED,
            message="库名称无效",
        )
    if request_json.variant not in ("normal", "search", "posseg"):
        return sanic_response_json(
            code=CODE.ARGUMENTS_CHECK_FAILED,
            message="变种名称无效",
        )

    if request_json.variant == "normal":
        data = GetWordFreqResponse(
            text=dict(jieba_spliter.get_word_freq(request_json.text))
        )
    elif request_json.variant == "search":
        data = GetWordFreqResponse(
            text=dict(jieba_search_spliter.get_word_freq(request_json.text))
        )
    elif request_json.variant == "posseg":
        data = GetWordFreqResponse(
            text=dict(jieba_posseg_spliter.get_word_freq(request_json.text))
        )
    else:
        raise ValueError

    return sanic_response_json(code=CODE.SUCCESS, data=asdict(data))
