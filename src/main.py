import json
import logging
from dataclasses import dataclass

import httpx

from consts import UPTIME_FILE
from sender import SMTPSender

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

    def __str__(self) -> str:
        return f"{self.address} {self.status}"


def main():
    with open(UPTIME_FILE, "r", encoding="utf-8") as f:
        uptime_checks = json.load(f)

    sender = SMTPSender()

    for check in uptime_checks:
        addresses = check.get("addresses")
        email = check.get("email")
        results = check_addresses(addresses)
        failed_checks = get_failed_checks(results)
        if failed_checks:
            failed_checks_str = "\n".join([str(r) for r in failed_checks])
            sender.send_mail(
                email,
                "Uptime check failed",
                f"{failed_checks_str}",
            )


def get_failed_checks(results: list[Result]) -> list[Result]:
    failed_checks = []
    for result in results:
        if result.status != 200:
            logging.error(result)
            failed_checks.append(result)
        else:
            logging.info(result)
    return failed_checks


def check_addresses(addresses: list[str]) -> list[Result]:
    results: list[Result] = []
    for address in addresses:
        try:
            results.append(check_status(address))
        except httpx.TimeoutException:
            results.append(Result(address, 408))
        except Exception:
            results.append(Result(address, 500))
    return results


def check_status(address: str) -> Result:
    resp = httpx.get(address, timeout=0.5)
    return Result(address, resp.status_code)


if __name__ == "__main__":
    main()
