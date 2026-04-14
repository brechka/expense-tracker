from unittest.mock import patch, MagicMock
from src.helpers.scheduler import start_cleanup_scheduler


@patch("src.helpers.scheduler.threading.Thread")
def test_start_cleanup_scheduler(mock_thread_cls):
    mock_thread = MagicMock()
    mock_thread_cls.return_value = mock_thread
    start_cleanup_scheduler()
    mock_thread_cls.assert_called_once()
    mock_thread.start.assert_called_once()
    assert mock_thread_cls.call_args.kwargs["daemon"] is True
