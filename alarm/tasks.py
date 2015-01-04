from __future__ import absolute_import

from celery.utils.log import get_task_logger
from Notier.celery import app
from alarm.crawler import Crawler
from alarm.models import *
from alarm.utils import mail

import urllib2
from bs4 import BeautifulSoup
from threading import Lock
 
logger = get_task_logger(__name__)

class TestCrawler(Crawler):
    def __init__(self):
        super(TestCrawler, self).__init__()
        self.process_lock = Lock()

    def process_document(self, doc):
        self.process_lock.acquire()
        # print 'GET', doc.status, doc.url, doc.text
        
        # if any keyword found in text notify it to users 
        
        self.process_lock.release()
 
@app.task
def scrap():
    all_usersettings = UserSettings.objects.filter( beat = 1 );
    
    for usersettings in all_usersettings:
        u = usersettings.user
        entries = MonitoringEntry.objects.filter(user = u)
        
        for entry in entries:
            print entry.title
            print entry.keyword.text
            
            response = urllib2.urlopen(entry.site.url)
            html = response.read().decode("cp949", "ignore").encode("utf-8", "ignore")
     
            bs = BeautifulSoup(html)
            titles = bs.findAll('font', { 'class':'list_title' })
            
            for title in titles:
                print title.parent['href']
                print title.get_text()
                    
            # print bs.title
            # print bs.title.string
            # print bs.title.string.encode("UTF-8")

  # c = TestCrawler()
  # c.add_url_filter('http://www.ryuniverse.com/blog/[\x21-\x7E]+')
  # c.set_max_depth(1);
  # c.crawl(url)
  
  #mail.send_gmail(to = 'hwijung.ryu@gmail.com', subject = 'Test', text = 'hello world',
  #                html = "", attach = "")  
  
    
# A periodic task that will run every minute (the symbol "*" means every)
'''
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example():
    logger.info("Start task")
    now = datetime.now()
    result = scrapers.scraper_example(now.day, now.minute)
    logger.info("Task finished: result = %i" % result)
'''