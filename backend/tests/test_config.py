import os
import importlib
from unittest.mock import patch


def test_default_config():
    from src.config import PORT, HOST, DATABASE_URL, ENV, LOG_FILE
    assert isinstance(PORT, int)
    assert isinstance(HOST, str)
    assert isinstance(DATABASE_URL, str)
    assert isinstance(ENV, str)
    assert isinstance(LOG_FILE, str)


def test_config_env_override():
    with patch.dict(os.environ, {
        "PORT": "9999",
        "HOST": "127.0.0.1",
        "DATABASE_URL": "sqlite:///custom.db",
        "ENV": "production",
        "ENVIRONMENT": "local",
        "LOG_FILE": "custom.log"
    }):
        import src.config
        importlib.reload(src.config)
        assert src.config.PORT == 9999
        assert src.config.HOST == "127.0.0.1"
        assert src.config.DATABASE_URL == "sqlite:///custom.db"
        assert src.config.ENV == "production"
        assert src.config.LOG_FILE == "custom.log"


def test_default_env_is_development():
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///test.db", "ENVIRONMENT": "local"}, clear=True):
        import src.config
        importlib.reload(src.config)
        assert src.config.ENV == "development"


def test_postgres_url_from_env_vars():
    with patch("dotenv.load_dotenv"), patch.dict(os.environ, {
        "POSTGRES_SERVER": "myhost",
        "POSTGRES_USER": "myuser",
        "POSTGRES_PASSWORD": "mypass",
        "POSTGRES_PORT": "5433",
        "POSTGRES_DB": "mydb",
        "ENVIRONMENT": "local",
    }, clear=True):
        import src.config
        importlib.reload(src.config)
        assert "myhost" in src.config.DATABASE_URL
        assert "myuser" in src.config.DATABASE_URL
        assert "5433" in src.config.DATABASE_URL


def test_secret_key_fails_in_non_local():
    import pytest
    with patch.dict(os.environ, {
        "ENVIRONMENT": "production",
        "SECRET_KEY": "dev-secret-key-change-in-production",
    }):
        import src.config
        with pytest.raises(ValueError, match="SECRET_KEY"):
            importlib.reload(src.config)
