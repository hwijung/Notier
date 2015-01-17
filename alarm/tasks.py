from __future__ import absolute_import

from celery.utils.log import get_task_logger
from Notier.celery import app
from alarm.crawler import Crawler
from alarm.models import *
# from alarm.utils import mail
from alarm.notiers import NotierAgent
from alarm.utils.ppomppu_tools import PpomppuParsor

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
    
    pParsor = PpomppuParsor()
    fp_title_objects = pParsor.get_foreign_ppomppu_titles()
    
    # extract users if there beat flag is on
    all_usersettings = UserSettings.objects.filter( beat = 1 );
    
    for usersettings in all_usersettings:
        u = usersettings.user
        entries = MonitoringEntry.objects.filter(user = u)
        
        # pick each entries and try to find whether the keyword is included or not 
        for entry in entries:
            for fp_title in fp_title_objects:
                
                # If there is keyword in the title...
                if fp_title.find(entry.keyword.text) != -1:
                    print "Found"
                    
                    # Send Notifying message 
                    NotierAgent.noty(user = u, fp_title )
                    
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