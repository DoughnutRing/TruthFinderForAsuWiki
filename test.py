from time import sleep
from selenium import webdriver
import undetected_chromedriver as uc

if __name__ == "__main__":
    chrome_options = uc.ChromeOptions()
    chrome_options.headless = False

    chrome_options.add_argument('--lang=zh-CN,zh,zh-TW,en-US,en')
    chrome_options.add_argument(
    '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    chrome_options.add_argument("--proxy-server=120.194.55.139:6969")

    browser = uc.Chrome(options=chrome_options)
    # browser = webdriver.Chrome(options=chrome_options)
    

    browser.get("https://www.baidu.com")
    sleep(5)
    print(browser.page_source)