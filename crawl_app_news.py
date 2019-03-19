# coding=utf-8
#! /usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os
from console_logging import console
import argparse
import codecs
from collections import defaultdict

class Crawler:
    def __init__(self, pageUrl, totalPageNum , filename):
        self.pageUrl = pageUrl
        self.totalPageNum = totalPageNum
        self.filename = filename

    def process(self, data_str):
        data = data_str.split('\n')
        new_data = []
        for i in range(len(data)):
            if re.search(r'[0-9] \.[0-9]', data[i]):
                data[i], data[i+1], data[i+2] = '', '', ''
        for i in range(len(data)-2): 
            if data[i] == '' and data[i+2] == '':
                new_data.append(data[i-1])
        new_data = filter(lambda x:x!='', new_data)
        return new_data

    def getLinkLi(self, pageIndex, link_xpath):
        link_li = []
        for i in range(1, 19):
            try:
                element = self.driver.find_element_by_xpath(link_xpath % i)
                # element = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[2]/strong/a')
                link = element.get_attribute("href")
                link_li.append(link)
            except:
                console.error('get link {} failly!'.format(i))
                continue
        return link_li
    def getDetails(self, pageIndex, link_xpath):
        '''
        :param pageIndex: 页索引
        :param id: 标签对应的id
        :return:
        '''
        console.info('crawling page {}'.format(pageIndex))
        link_li = self.getLinkLi(pageIndex, link_xpath)
        print('link list is {}'.format(link_li))
        for link in set(link_li):
            try:
                console.info('crawling data from link {}'.format(link))
                self.driver.get(link)
                self.driver.implicitly_wait(10)             
                title = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/h1')
                title = title.text.encode('utf-8')
                context = []
                for i in range(1, 10):
                    try:
                        context_p = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/p[{}]'.format(i))
                        context_p = context_p.text.encode('utf-8')
                        context.append(context_p)
                    except: 
                        break
                self.data[title] = '\n'.join(context)
            except:
                console.error('crawling element {} failly!'.format(link))
                continue
    def saveData(self, filename, data_dict):
        with open(filename, 'a') as outputf:
            for k , v in data_dict.iteritems():
                outputf.write('{}\n'.format(v))
                outputf.write('\n')

    def CatchData(self,link_xpath):
        '''
        抓取数据
        :param id:获取数据的标签id
        :param totalpageCountLable:获取总页数标记
        :return:
        '''
        start = time.clock()
        console.success('open webdriver !')
        self.driver = webdriver.PhantomJS(executable_path=r"/usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
        pageNum = self.totalPageNum
        print 'total page is {}'.format(pageNum)
        for i in range(1, self.totalPageNum+1):
            self.data = defaultdict()
            self.driver.implicitly_wait(15)
            self.driver.get(self.pageUrl % i)
            try:
                self.getDetails(i, link_xpath)
                console.success('crawling page {} successfully'.format(i))
                print 'saving data...'
                self.saveData(self.filename, self.data)
            except:
                console.error('Crawling page {} failly!'.format(i))
                erro_file = self.filename.split('.', 1)[0] + '_error.txt'
                with open(erro_file, 'a') as outputf:
                	error_url = self.pageUrl % (i)
                	outputf.write(error_url)
                	outputf.write('\n')
            time.sleep(5)  # 延迟5秒,防止获取数据过快而被封ＩＰ
        print 'Load Over'       
        end = time.clock()
        print "Time: %f s" % (end - start)

def main():

    parser = argparse.ArgumentParser(description='Crawl text data from http://app.hiapk.com for writing guidelines.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--output_file', help='output file')
    parser.add_argument('--pageUrl', type=str, help='Url template.')
    parser.add_argument('--totalPageNum', type=int, help='total pageUrl numbers.')
    args = parser.parse_args()
    #下一页的url
    pageUrl = args.pageUrl
    cw = Crawler(pageUrl, args.totalPageNum, args.output_file)
    #获取数据的标签ID 
    link_xpath = '/html/body/div[2]/div[2]/div[2]/div[1]/div/div[%d]/strong/a'
    cw.CatchData(link_xpath)
#测试
main()
