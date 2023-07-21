import schedule
from schedule import every, repeat
import time as tm

from web_scrape.controller import controller


# Setting the CRON time period
@repeat(every(15).minutes)
def job() -> None:
    controller()


while True:

    schedule.run_pending()
    tm.sleep(1)