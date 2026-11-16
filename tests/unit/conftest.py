from unittest.mock import patch

import pytest


@pytest.fixture
def mock_client_serial():
    with patch("tab5.client.serial.Serial") as mock_serial:
        fake_device = mock_serial.return_value.__enter__.return_value

        yield mock_serial, fake_device
