import requests
import concurrent.futures
import time
from tabulate import tabulate


def get_status(url: str) -> tuple:

    tm1 = time.perf_counter()

    resp = requests.get(url=url)

    tm2 = time.perf_counter()
    total_time = tm2 - tm1

    print(f'Total time elapsed: {total_time:0.2f} seconds')

    return (resp.status_code, url, total_time)


def http_tester() -> dict:
    data = {}

    urls = ['http://webcode.me', 'https://httpbin.org/get',
        'https://google.com', 'https://stackoverflow.com',
        'https://github.com', 'https://clojure.org',
        'https://fsharp.org']

    with concurrent.futures.ThreadPoolExecutor() as executor:

        futures = []

        for url in urls:
            futures.append(executor.submit(get_status, url=url))

        for future in concurrent.futures.as_completed(futures):
            print(future.result())
            result_url = future.result()[1]
            result_time = future.result()[2]
            data[result_url] = result_time

        print(f"Data: {data}")

        minimum_time = min([x for x in data.values()])
        maximum_time = max([x for x in data.values()])
        average_time = sum([x for x in data.values()]) / len([x for x in data.values()])

        col_names = ["Minimum Time", "Maximum Time", "Average Time"]
        data_tab = [[minimum_time, maximum_time, average_time]]

        print(tabulate(data_tab, headers=col_names))

        return data


if __name__ == "__main__":
    http_tester()