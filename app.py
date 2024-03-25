from IowaFoodHubSpider import IowaFoodHubSpider
from FreshThymeSpider import FreshThymeSpider
from JoiaFoodFarmSpider import JoiaFoodFarmSpider
from multiprocessing import Process, Queue
from twisted.internet import reactor
import scrapy.crawler as crawler
import sys

# the wrapper to make it run more times
def f(spider):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
    except Exception as e:
        print(sys.exc_info())
        
def run_spider(spider):
    # p = Process(target=f, args=(spider, ))
    # p.start()
    # p.join()
    f(spider=spider)
if __name__ == '__main__':
    run_spider(IowaFoodHubSpider)
    # run_spider(FreshThymeSpider)
    # run_spider(JoiaFoodFarmSpider)
