import re
from tkinter.messagebox import NO
from lxml import etree
from tqdm import tqdm
import sys
import requests
import random
import time
import threading

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]
URL = "https://www.asoulwikisite.com"
LOAD_FROM_TXT = True
proxypool = []
flow = 0

proxies_list=[]
def check_ip(proxies_list):
    headers = {
        'Referer':'https://www.liepin.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    can_use=[]
    print('==========?????????????????????============')
    for proxy in tqdm(proxies_list):
        try:
            
            response=requests.get('https://baidu.com',headers=headers,proxies=proxy,timeout=0.1)
            if response.status_code==200:
                can_use.append(proxy)
            else:
                # print('????????????')
                pass
        except Exception as e:
            print(e)
        finally:
            # print('??????IP',proxy,'??????')
            pass
    # print(can_use)
    return can_use

def scratch_ip():
    print('==========??????????????????IP??????============')
    for page in tqdm(range(50,100)):
        # print('==========???????????????{}?????????============'.format(str(page)))
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
    global proxypool
    proxypool=check_ip(proxies_list)

def get_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }

def get_proxies():
    with open('ippool.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            proxypool.append({'HTTP': line[:-1]})
    print(f"Proxy pool loading complete with {len(proxypool)} IPs.")

def get_proxy():
    return random.choice(proxypool)

def get_flow(content):
    # sz = sys.getsizeof(content)
    sz = len(content)
    global flow
    flow += sz
    return f"{round(flow / 1024, 2)}KB" if flow < 1024**2 else f"{round(flow / 1024**2, 2)}MB"

analysed_website = set()
urls = [URL]
scratched_website = set(urls)
def access_truth(url):
    header = get_header()
    prox = get_proxy()
    global count, scratched_website

    response = session.get(url,headers=header,proxies=prox)
    if response.status_code == 200 and len(response.text):
        count += 1
        # flow_txt = get_flow(response.content)
        # print(str(count) + ": from " + prox['HTTP'] + " to " + URL + " successfully. Used " + flow_txt + ".")
        print(f"IP????????????{prox['HTTP']}????????????????????????????????????{count}??????????????????????????????????????????{len(urls)}??????\n", end = None)
        html_txt = response.text
        response.close()
        if url not in analysed_website:
            # ?????????????????????????????????
            url_lst = extract_all_urls(html_txt)
            analysed_website.add(url)
            new_urls = url_lst - scratched_website
            for u in new_urls:
                urls.append(u[1:-1]) # ???????????????
            scratched_website |= new_urls
    else:
        # print(str(count) + ": from " + prox['HTTP'] + " to " + URL + " failed.")
        print(f"IP????????????{prox['HTTP']}?????????????????????????????????\n", end=None)
        response.close()

def extract_all_urls(html):
    pattern = re.compile(r'\"' + URL + '/[\S]+\"')
    url_lst = pattern.findall(html)
    return set(url_lst)

if __name__ == "__main__":
    if LOAD_FROM_TXT:
        get_proxies()
    else:
        scratch_ip()
    count = 0
    session = requests.session()
    session.keep_alive = False
    group_size = 1000

    while True:
        t = threading.Thread(target = access_truth, args=[random.choice(urls)])
        t.start()

        # ?????????????????????????????????0.05-0.25s???????????????????????????????????????????????????
        if count % group_size:
            sleeptime = random.randint(1,5) / 50 
        else: 
            # sleeptime = 61 
            sleeptime = random.randint(1,5) 
            random.seed(time.time())
            group_size = random.randint(800, 3000)

        # print(f"Wait {round(sleeptime, 2)} seconds.")
        # print(f"{round(sleeptime, 2)}?????????????????????????????????")
        time.sleep(sleeptime)