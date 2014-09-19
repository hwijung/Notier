from __future__ import absolute_import

from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime
from Notier.celery import app
from alarm.crawler import Crawler
from threading import Lock
 
logger = get_task_logger(__name__)

class TestCrawler(Crawler):
    def __init__(self):
        super(TestCrawler, self).__init__()
        self.process_lock = Lock()

    def process_document(self, doc):
        self.process_lock.acquire()
        print 'GET', doc.status, doc.url
        self.process_lock.release()

@app.task
def add(x,y):
  logger.info("Start task")
  logger.info("Task finished: result = %i" % (x+y) )
  
@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)  

@app.task
def scrap(url):
  c = TestCrawler()
  c.add_url_filter('http://www.ryuniverse.com/blog/[\x21-\x7E]+')
  c.crawl('http://www.ryuniverse.com')  
    
# A periodic task that will run every minute (the symbol "*" means every)
'''
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example():
    logger.info("Start task")
    now = datetime.now()
    result = scrapers.scraper_example(now.day, now.minute)
    logger.info("Task finished: result = %i" % result)
'''