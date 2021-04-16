import concurrent.futures
import logging

import ally

logger = logging.getLogger(__name__)

a = ally.Ally()


def job():
    logger.info("Submitting job")
    return a.timesales("spy", startdate="2020-06-19", enddate="2020-06-19", block=False)


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    logger.info("Submitting requests")
    # Submit all our orders
    futures = {executor.submit(job): i for i in range(200)}
    logger.info("Submitted!")

    logger.info("Getting results...")
    for future in concurrent.futures.as_completed(futures):
        logger.info("%s #%s", future.result(), futures[future])
