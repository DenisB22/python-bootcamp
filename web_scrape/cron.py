import schedule
from schedule import every, repeat
import time as tm

from web_scrape.controller import controller


@repeat(every(5).seconds)
def job() -> None:
    controller()


while True:

    schedule.run_pending()
    tm.sleep(1)