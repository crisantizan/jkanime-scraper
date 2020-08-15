import requests
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

LINK = 'https://jkanime.net/the-god-of-high-school/'
# XPATH_GET_LINKS = '//div[@id="episodes-content"]/div'
XPATH_GET_LINKS = '//div[@id="episodes-content"]/div/a[@class="cap-header"]/@href'
XPATH_IFRAME = '//iframe[@class="player_conte"]/@src'
XPATH_SOURCE = '//source/@src'


def init_driver():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    return driver


def fetch(browser, url, xpath, sleep=0):
    browser.get(url)

    if not sleep == 0:
        time.sleep(sleep)

     # get the innerhtml from the rendered page
    innerHTML = browser.execute_script("return document.body.innerHTML")
    # Now use lxml to parse the page
    parsed = html.fromstring(innerHTML)

    # Get your element with xpath
    return parsed.xpath(xpath)


def fecth_by_selenium(url):
    # Load in your browser(I use chrome)
    browser = init_driver()
    # get the url with Selenium
    browser.get(url)
    time.sleep(2)

    # get the innerhtml from the rendered page
    innerHTML = browser.execute_script("return document.body.innerHTML")

    # Now use lxml to parse the page
    tree = html.fromstring(innerHTML)
    # Get your element with xpath
    links = tree.xpath(XPATH_GET_LINKS)
    # close the browser
    # browser.quit()

    # for link in links:
    print(links[0])
    browser.get(links[0])
    time.sleep(3)
    text = browser.execute_script("return document.body.innerHTML")
    parsed = html.fromstring(text)
    # Get your element with xpath
    frame = parsed.xpath(XPATH_IFRAME)
    print(frame[0])

    browser.get(frame[0])
    source_html = browser.execute_script("return document.body.innerHTML")
    source_parsed = html.fromstring(source_html)
    src = source_parsed.xpath(XPATH_SOURCE)
    print(src[0])


if __name__ == '__main__':
    driver = init_driver()
    links = fetch(browser=driver, url=LINK, xpath=XPATH_GET_LINKS, sleep=1)

    for link in links:
        iframe_link = fetch(browser=driver, url=link, xpath=XPATH_IFRAME, sleep=1)[0]
        src = fetch(browser=driver, url=iframe_link, xpath=XPATH_SOURCE)[0]
        print(src)
