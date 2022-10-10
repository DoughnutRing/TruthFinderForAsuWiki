import re
from lxml import etree
from tqdm import tqdm
import requests
import random
import time
import threading
from Connection import Connection

URL = "https://www.asoulwikisite.com"
LOAD_FROM_TXT = True

class TruthFinder:
    def __init__(self, url, LOAD_FROM_TXT):
        
        self.URL = url
        self.LOAD_FROM_TXT = LOAD_FROM_TXT
        self.flow = 0
        self.group_size = 1000
        self.index = 0 # 搜查网址的下标
        self.urls=[url] # 子网页大全
        self.scratched_website = set(self.urls)

        self.conn = Connection()

        # if self.LOAD_FROM_TXT:
        #     self.__get_proxies()
        # else:
        #     self.__scratch_ip()


    def __check_ip(self, proxies_list):
        headers = {
            'Referer':'https://www.liepin.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        can_use=[]
        print('==========正在检测可用性============')
        for proxy in tqdm(proxies_list):
            try:
                response=requests.get('https://baidu.com',headers=headers,proxies=proxy,timeout=0.1)
                if response.status_code==200:
                    can_use.append(proxy)
                else:
                    # print('不可使用')
                    pass
            except Exception as e:
                print(e)
            finally:
                # print('当前IP',proxy,'通过')
                pass
        # print(can_use)
        return can_use

    def __scratch_ip(self):
        print('==========正在注入代理IP地址============')
        proxies_list = []
        for page in tqdm(range(50,300)):
            # print('==========正在获取第{}页数据============'.format(str(page)))
            base_url='https://www.kuaidaili.com/free/inha/{}/'.format(str(page))
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
            response=requests.get(base_url,headers=headers)
            data=response.text
            html_data = etree.HTML(data)
            
            parse_list=html_data.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
            
            for tr in parse_list:
                dict_proxies={}
                http_type=tr.xpath('./td[4]/text()')
                ip_num=tr.xpath('./td[1]/text()')
                ip_port=tr.xpath('./td[2]/text()')
                dict_proxies[http_type[0]]=ip_num[0]+':'+ip_port[0] 
                # print(dict_proxies)
                proxies_list.append(dict_proxies)
            response.close()
            time.sleep(10)

        self.proxypool=self.__check_ip(proxies_list)

    def __get_flow(self, content):
        # sz = sys.getsizeof(content)
        sz = len(content)
        self.flow += sz
        return f"{round(self.flow / 1024, 2)}KB" if self.flow < 1024**2 else f"{round(self.flow / 1024**2, 2)}MB"
        

    def __find_more_truth(self, html_txt):
        '抓取网页下的所有子网页'
        url_lst = self.__extract_all_urls(html_txt)
        self.index += 1
        new_urls = url_lst - self.scratched_website # 差集获取新链接
        for u in new_urls:
            self.urls.append(u[1:-1]) # 删除双引号
        self.scratched_website |= new_urls # 并集加入

    def find_truth(self):
        '获取真相全集'
        t1 = None
        while self.index < len(self.urls):
            url = self.urls[self.index]
            html_txt = self.conn.connect_truth(url, need_txt=True, num_truth=len(self.urls))
            if t1:
                t1.join()
            t1 = threading.Thread(target=self.__find_more_truth(html_txt))
            t1.start()
            
    def access_truth(self):
        count = 0
        while True:
            t = threading.Thread(target = self.conn.connect_truth, args=[random.choice(self.urls), False, len(self.urls)])
            t.start()

            # 每一组访问中睡眠时间为0.002-0.01s，每组结束后更换组大小和随机数种子
            if count % self.group_size:
                sleeptime = random.randint(1,5) / 100 
            else: 
                # sleeptime = 61 
                sleeptime = random.randint(1,5) 
                random.seed(time.time())
                self.group_size = random.randint(800, 3000)

            count += 1
            time.sleep(sleeptime)
    

    def __extract_all_urls(self, html):
        pattern = re.compile(r'\"' + self.URL + '/[\S]+\"')
        url_lst = pattern.findall(html)
        return set(url_lst)

if __name__ == "__main__":
    truth_finder = TruthFinder(URL, LOAD_FROM_TXT)
    truth_finder.find_truth()
    truth_finder.access_truth()