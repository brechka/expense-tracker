import logging


def test_request_logging(client, caplog):
    with caplog.at_level(logging.INFO, logger="expense_tracker"):
        client.get("/api/ping")
    assert any("GET" in r.message and "/api/ping" in r.message for r in caplog.records)
