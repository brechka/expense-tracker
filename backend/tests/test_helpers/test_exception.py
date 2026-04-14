from src.helpers.exception import AppException, NotFoundException, BadRequestException


def test_app_exception():
    exc = AppException("error", status_code=500)
    assert exc.message == "error"
    assert exc.status_code == 500
    assert str(exc) == "error"


def test_app_exception_default_status():
    exc = AppException("fail")
    assert exc.status_code == 500


def test_not_found_exception():
    exc = NotFoundException("not here")
    assert exc.message == "not here"
    assert exc.status_code == 404


def test_not_found_exception_default_message():
    exc = NotFoundException()
    assert exc.message == "Resource not found"
    assert exc.status_code == 404


def test_bad_request_exception():
    exc = BadRequestException("bad input")
    assert exc.message == "bad input"
    assert exc.status_code == 400


def test_bad_request_exception_default_message():
    exc = BadRequestException()
    assert exc.message == "Bad request"
    assert exc.status_code == 400


def test_exceptions_are_subclass_of_app_exception():
    assert issubclass(NotFoundException, AppException)
    assert issubclass(BadRequestException, AppException)


def test_exceptions_are_subclass_of_exception():
    assert issubclass(AppException, Exception)
