import json
import logging
from dataclasses import dataclass

import httpx

from consts import UPTIME_FILE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="uptime_bot.log",
    filemode="a",
)


@dataclass
class Result:
    address: str
    status: int


def main():
    with open(UPTIME_FILE, "r", encoding="utf-8") as f:
        uptime_checks = json.load(f)

    for check in uptime_checks:
        addresses = check.get("addresses")
        email = check.get("email")
        results = []
        for address in addresses:
            print(f"Checking {address}")
            try:
                results.append(check_status(address))
            except httpx.TimeoutException:
                results.append(Result(address, 408))
            except Exception:
                results.append(Result(address, 500))
        for result in results:
            logging.info(result)


def check_status(address: str) -> Result:
    resp = httpx.get(address, timeout=0.5)
    return Result(address, resp.status_code)


if __name__ == "__main__":
    main()
