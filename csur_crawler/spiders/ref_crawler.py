import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.http import Response
import os
from os import path
import logging
import logging.config
import traceback
import datetime
import time


Root_Path = '/Users/wenzhiyuan/Desktop/csur_crawler/csur_crawler/csur_crawler/spiders'
config_file = 'logging.ini'
# path.join(path.dirname(path.abspath(__file__)), log_path)
logging.config.fileConfig(path.join(Root_Path, config_file), disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class RefSpider(scrapy.Spider):
    name = "ref_extraction"
    allowed_domains = ["scholar.google.com"]
    start_urls = []
    urls = []
    current_survey = []
    url_cnt = 0
    survey_cnt = 0
    next_flag = 'next_survey'
    fopen = ""

    def __init__(self):
        link_path = "../link/"
        files = os.listdir(path.join(Root_Path, link_path))
        urls = []
        for file in files:
            f = open(path.join(Root_Path, link_path) + "/" + file)
            iter_f = iter(f)
            for line in iter_f:
                urls.append(line)
            urls.append(self.next_flag)
            self.current_survey.append(file)
            self.start_urls.append(urls[0])
            self.urls = urls[1:]

        # file i/o
        self.fopen = open('result.txt', 'w')
        self.fopen.write(self.current_survey[self.survey_cnt])
        self.fopen.write('\n')

    def parse(self, response):
        logger.info(response.request.headers['User-Agent'])
        soup = BeautifulSoup(response.body, 'html.parser')
        # self.fopen.write(str(soup))
        pdf_link = soup.find("div", class_='gs_ggs gs_fl')
        # self.fopen.write(str(pdf_link))
        # logger.info(pdf_link.find_all('a')[0]['href'])

        try:
            self.fopen.write(pdf_link.find_all('a')[0]['href'])
            self.fopen.write('\n')

        except:
            err_msg = 'Under ' + self.current_survey[self.survey_cnt] + ' ' + str(response.url) + '\n'
            logger.error(err_msg)
            self.fopen.write(err_msg)
            # self.fopen.write('\n')

        url = self.urls[self.url_cnt]
        if url == self.next_flag:
            self.url_cnt += 1
            self.survey_cnt += 1
            self.fopen.write(self.current_survey[self.survey_cnt])
            url = self.urls[self.url_cnt]

        self.url_cnt += 1
        time.sleep(2)
        yield Request(url)


