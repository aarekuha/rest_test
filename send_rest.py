import time
import requests
from requests.sessions import HTTPAdapter
from tqdm import tqdm


# HOST = "localhost:8080"
HOST = "85.30.248.28:8088"
URL_UNSAFE = f"http://{HOST}/data_unsafe"
URL_SAFE = f"http://{HOST}/data_with_auth"
COUNT = 1_000
TOKEN = "secret-token"

StatusCodeType = int
CountType = int
StatusesType = dict[StatusCodeType, CountType]


def report(header: str, statuses: StatusesType, start_time: float, end_time: float) -> None:
    total_time: float = end_time - start_time
    print(f"{header}:")
    print(f"\tTotal time: {total_time} sec")
    print("\tAVG:")
    for response_status, statuses_count in statuses.items():
        print(f"\t\t{response_status}: {total_time / statuses_count}")


def sync_without_session(header: str, count: int, token: str | None = None):
    result_statuses: StatusesType = {}
    response: requests.models.Response
    start_time: float = time.monotonic()
    url: str = URL_SAFE if token else URL_UNSAFE
    headers: dict | None = None if not token else {"x-token": token}
    for _ in tqdm(range(count)):
        response = requests.get(url=url, headers=headers)
        if not response.status_code in result_statuses:
            result_statuses[response.status_code] = 0
        result_statuses[response.status_code] += 1
    report(
        header=header,
        statuses=result_statuses,
        start_time=start_time,
        end_time=time.monotonic(),
    )


def sync_with_session(header: str, count: int, token: str | None = None):
    result_statuses: StatusesType = {}
    response: requests.models.Response
    result_statuses = {}
    session: requests.Session = requests.Session()
    url: str = URL_SAFE if token else URL_UNSAFE
    if token:
        headers: dict = {"x-token": token}
        session.headers.update(headers)
    session.mount(url, HTTPAdapter())
    start_time: float = time.monotonic()
    for _ in tqdm(range(count)):
        response = session.get(url=url)
        if not response.status_code in result_statuses:
            result_statuses[response.status_code] = 0
        result_statuses[response.status_code] += 1
    report(
        header=header,
        statuses=result_statuses,
        start_time=start_time,
        end_time=time.monotonic(),
    )


if __name__ == "__main__":
    sync_without_session(header="Without session (unsafe)", count=COUNT)
    sync_with_session(header="With session (unsafe)", count=COUNT)
    sync_without_session(header="With session (with token)", count=COUNT, token=TOKEN)
    sync_with_session(header="With session (with token)", count=COUNT, token=TOKEN)
