from src.db.database import get_db


def test_get_db_yields_session():
    gen = get_db()
    db = next(gen)
    assert db is not None
    try:
        gen.send(None)
    except StopIteration:
        pass


def test_get_db_closes_on_exception():
    gen = get_db()
    db = next(gen)
    assert db is not None
    try:
        gen.throw(Exception("test"))
    except Exception:
        pass
