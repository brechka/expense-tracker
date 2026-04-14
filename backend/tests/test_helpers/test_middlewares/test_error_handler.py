import asyncio
from fastapi.exceptions import RequestValidationError
from src.helpers.middlewares.error_handler import validation_exception_handler, app_exception_handler, generic_exception_handler
from src.helpers.exception import AppException, NotFoundException, BadRequestException


class FakeURL:
    def __init__(self, path):
        self.path = path


class FakeRequest:
    def __init__(self, path="/test", method="POST"):
        self.method = method
        self.url = FakeURL(path)


def test_validation_exception_handler():
    errors = [{"type": "value_error", "loc": ("body", "name"), "msg": "bad value", "input": ""}]
    exc = RequestValidationError(errors=errors)
    response = asyncio.run(validation_exception_handler(FakeRequest(), exc))
    assert response.status_code == 422


def test_validation_exception_handler_returns_errors():
    errors = [{"type": "value_error", "loc": ("body", "name"), "msg": "bad value", "input": ""}]
    exc = RequestValidationError(errors=errors)
    response = asyncio.run(validation_exception_handler(FakeRequest(), exc))
    import json
    body = json.loads(response.body)
    assert "errors" in body
    assert body["errors"][0]["field"] == "body.name"


def test_app_exception_handler():
    exc = AppException("Something went wrong", status_code=400)
    response = asyncio.run(app_exception_handler(FakeRequest(), exc))
    assert response.status_code == 400
    import json
    body = json.loads(response.body)
    assert body["detail"] == "Something went wrong"


def test_app_exception_handler_not_found():
    exc = NotFoundException("Expense not found")
    response = asyncio.run(app_exception_handler(FakeRequest(), exc))
    assert response.status_code == 404


def test_app_exception_handler_bad_request():
    exc = BadRequestException("Invalid input")
    response = asyncio.run(app_exception_handler(FakeRequest(), exc))
    assert response.status_code == 400


def test_generic_exception_handler():
    exc = RuntimeError("something broke")
    response = asyncio.run(generic_exception_handler(FakeRequest(), exc))
    assert response.status_code == 500
    assert b"Internal server error" in response.body


def test_generic_exception_handler_different_error():
    exc = ValueError("bad value")
    response = asyncio.run(generic_exception_handler(FakeRequest(), exc))
    assert response.status_code == 500
