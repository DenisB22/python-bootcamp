import json

import requests
import concurrent.futures
import time
from tabulate import tabulate


def multithreading(data: dict, urls, usernames=None) -> dict:
    with concurrent.futures.ThreadPoolExecutor() as executor:

        futures = []
        if not usernames:
            for url in urls:
                futures.append(executor.submit(get_status, url=url))

            for future in concurrent.futures.as_completed(futures):
                print(future.result())
                result_url = future.result()[1]
                result_time = future.result()[2]
                data[result_url] = result_time

        else:
            for user_info in usernames:
                futures.append(executor.submit(login, url='http://localhost:3030/users/login', user_info=user_info))

            for future in concurrent.futures.as_completed(futures):
                print(future.result())
                result_email, result_time = future.result()[1], future.result()[2]

                data[result_email] = result_time

        print(f"Data: {data}")

        create_table(data)

        return data


def create_table(data: dict) -> None:
    minimum_time = min([x for x in data.values()])
    maximum_time = max([x for x in data.values()])
    average_time = sum([x for x in data.values()]) / len([x for x in data.values()])

    col_names = ["Minimum Time", "Maximum Time", "Average Time"]
    data_tab = [[minimum_time, maximum_time, average_time]]

    print(tabulate(data_tab, headers=col_names))


def login(url: str, user_info: dict) -> tuple:

    tm1 = time.perf_counter()

    result = requests.post(url, json=user_info)

    tm2 = time.perf_counter()
    total_time = tm2 - tm1

    print(f'Total time elapsed: {total_time:0.2f} seconds')

    result_dict = json.loads(result.text)
    email = result_dict['email']

    return (result, email, total_time)


def get_status(url: str) -> tuple:

    tm1 = time.perf_counter()

    resp = requests.get(url=url)

    tm2 = time.perf_counter()
    total_time = tm2 - tm1

    print(f'Total time elapsed: {total_time:0.2f} seconds')

    return (resp.status_code, url, total_time)


def http_tester() -> dict:
    print("---------------------------------HTTP Get Tester---------------------------------")

    data = {}

    urls = ['http://webcode.me', 'https://httpbin.org/get',
        'https://google.com', 'https://stackoverflow.com',
        'https://github.com', 'https://clojure.org',
        'https://fsharp.org']

    data = multithreading(data, urls)

    return data


def http_tester_login() -> dict:
    print("---------------------------------HTTP Login Tester---------------------------------")

    data = {}

    usernames = [
        {'email': 'peter@abv.bg', 'password': '123456'},
        {'email': 'george@abv.bg', 'password': '123456'},
        {'email': 'admin@abv.bg', 'password': 'admin'}
    ]

    data = multithreading(data, 'http://localhost:3030/users/login', usernames)

    return data


if __name__ == "__main__":
    http_tester()
    http_tester_login()