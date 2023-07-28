import json

import requests
import concurrent.futures
import time
from tabulate import tabulate

import os


# Function for handling multiple HTTP calls at the same time
def multithreading(data: dict, urls, usernames=None) -> dict:
    with concurrent.futures.ThreadPoolExecutor() as executor:

        futures = []
        if not usernames:

            for url in urls:
                futures.append(executor.submit(get_status, url=url))

            # Check if we are making a HTTP test to the same website
            same_url = all([x == urls[0] for x in urls])

            if same_url:
                url = urls[0]
                data[url] = []

                for future in concurrent.futures.as_completed(futures):
                    result_url = future.result()[1]
                    result_time = future.result()[2]
                    data[result_url].append(result_time)

                return data

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


# Function for visualizing and creating table with data
def create_table(data: dict) -> None:
    minimum_time = min([x for x in data.values()])
    maximum_time = max([x for x in data.values()])

    if type(minimum_time) == list and type(maximum_time) == list:
        average_time = sum([x for x in maximum_time]) / len(maximum_time)
        minimum_time = min(minimum_time)
        maximum_time = max(maximum_time)

        print(minimum_time)
        print(maximum_time)
        print(average_time)

    elif type(minimum_time == int):
        average_time = sum([x for x in data.values()]) / len([x for x in data.values()])

    col_names = ["Minimum Time", "Maximum Time", "Average Time"]
    data_tab = [[minimum_time, maximum_time, average_time]]

    print(tabulate(data_tab, headers=col_names))


# Function for making POST request, login with user data and measuring time for those requests
def login(url: str, user_info: dict) -> tuple:

    tm1 = time.perf_counter()

    result = requests.post(url, json=user_info)

    tm2 = time.perf_counter()
    total_time = tm2 - tm1

    print(f'Total time elapsed: {total_time:0.2f} seconds')

    result_dict = json.loads(result.text)
    email = result_dict['email']

    return (result, email, total_time)


# Function for making GET requests and measuring time for those requests
def get_status(url: str) -> tuple:

    tm1 = time.perf_counter()

    resp = requests.get(url=url)

    tm2 = time.perf_counter()
    total_time = tm2 - tm1

    print(f'Total time elapsed: {total_time:0.2f} seconds')

    return (resp.status_code, url, total_time)


# Function for organizing and testing HTTP Get
def http_tester() -> dict:
    print("---------------------------------HTTP Get Tester Multiple Websites---------------------------------")

    data = {}

    urls = ['http://webcode.me', 'https://httpbin.org/get',
        'https://google.com', 'https://stackoverflow.com',
        'https://github.com', 'https://clojure.org',
        'https://fsharp.org']

    data = multithreading(data, urls)

    return data


# Function for organizing and testing HTTP Post / Login
def http_tester_login() -> dict:
    print("---------------------------------HTTP Login Tester---------------------------------")

    data = {}

    usernames = [
        {'email': os.getenv('EMAIL_FIRST'), 'password': os.environ.get('PASSWORD_FIRST')},
        {'email': os.environ.get('EMAIL_SECOND'), 'password': os.environ.get('PASSWORD_SECOND')},
        {'email': os.environ.get('EMAIL_THIRD'), 'password': os.environ.get('PASSWORD_THIRD')}
    ]

    data = multithreading(data, 'http://localhost:3030/users/login', usernames)

    return data


def http_tester_multiple_calls_one_website(url: str, count_of_calls: int) -> None:
    print("---------------------------------HTTP Get Tester Same Website---------------------------------")
    multiple_urls = [url] * count_of_calls
    data = {}

    data = multithreading(data, multiple_urls)

    create_table(data)


if __name__ == "__main__":
    http_tester()

    # Should only be executed when local server is running
    http_tester_login()

    count_of_calls = 3
    http_tester_multiple_calls_one_website('https://stackoverflow.com', count_of_calls)