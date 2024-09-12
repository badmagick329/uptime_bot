import json
from pathlib import Path

from consts import CONF_FILE


class Config:
    _config_file: Path
    _smtp_user: str
    _smtp_password: str
    _smtp_host: str
    _timeout: int

    def __init__(self) -> None:
        assert CONF_FILE.is_file, "Config file not found"
        self._config_file = CONF_FILE
        with open(self._config_file, "r", encoding="utf-8") as f:
            conf = json.load(f)
        self._smtp_user = conf["SMTP_USER"]
        self._smtp_password = conf["SMTP_PASSWORD"]
        self._smtp_host = conf["SMTP_HOST"]
        self._test_address = conf["TEST_ADDRESS"]
        self._timeout = conf["TIMEOUT"]

    @property
    def config_file(self) -> Path:
        return self._config_file

    @property
    def smtp_user(self) -> str:
        return self._smtp_user

    @property
    def smtp_password(self) -> str:
        return self._smtp_password

    @property
    def smtp_host(self) -> str:
        return self._smtp_host

    @property
    def test_address(self) -> str:
        return self._test_address

    @property
    def timeout(self) -> int:
        return self._timeout
