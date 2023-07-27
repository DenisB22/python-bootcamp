import schedule
from schedule import every, repeat
import time as tm

from web_scrape.controller import controller
from web_scrape.logs.rotating_log import logger


# Setting the CRON time period
@repeat(every(15).minutes)
def job() -> None:

    log_info = 'CRON JOB starting'
    logger.info(log_info)

    controller()


while True:

    schedule.run_pending()
    tm.sleep(1)