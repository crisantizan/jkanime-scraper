import requests
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

LINK = 'https://jkanime.net/the-god-of-high-school'
LINK_2 = 'https://jkanime.net/major-2nd-tv-2nd-season'
# XPATH_GET_LINKS = '//div[@id="episodes-content"]/div'
XPATH_GET_LINKS = '//div[@id="episodes-content"]/div/a[@class="cap-header"]/@href'
XPATH_IFRAME = '//iframe[@class="player_conte"]/@src'
XPATH_SOURCE = '//source/@src'
XPATH_NAVIGATION = '//a[@class="numbers"]'
XPATH_LAST_NAVIGATION = '//a[@class="numbers"][last()]/text()'


def init_driver():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    return driver


def scrape(browser, xpath):
    # get the innerhtml from the rendered page
    innerHTML = browser.execute_script("return document.body.innerHTML")
    # Now use lxml to parse the page
    parsed = html.fromstring(innerHTML)
    # Get your element with xpath
    return parsed.xpath(xpath)


def get_links(browser, link):
    browser.get(link)
    time.sleep(1)

    links = []

    last_page = scrape(browser, XPATH_LAST_NAVIGATION)[0]
    pages = int(last_page.split('-')[1].strip())

    for num in range(pages):
        links.append(f'{link}/{num+1}')

    return links


def fetch(browser, url, xpath, sleep=0):
    browser.get(url)

    if not sleep == 0:
        time.sleep(sleep)

    return scrape(browser, xpath)


def input_data():
    link = input('Enter link: ')
    embed = input('Do you want get embed url\'s? [y]es - [n]o: ')[0]

    get_embed = embed.lower() == 'y'

    # remove last /
    if link[-1:] == '/':
        return {'link': link[0:-1], 'embed': get_embed}

    return {'link': link, 'embed': get_embed}


if __name__ == '__main__':
    input_data = input_data()

    link = input_data['link']
    embed = input_data['embed']
    title = re.sub(r'https://jkanime.net/', '', link)

    driver = init_driver()
    links = get_links(browser=driver, link=link)

    for index, link in enumerate(links):
        iframe_link = fetch(browser=driver, url=link,
                            xpath=XPATH_IFRAME, sleep=1)[0]
        src = fetch(browser=driver, url=iframe_link, xpath=XPATH_SOURCE)[0]

        with open(f'{title}.txt', mode='a', encoding='utf-8') as f:
            f.write('**** **** **** **** **** **** **** **** **** ****\n')
            f.write(f'EPISODE {index + 1}:\n')
            f.write(f'  LINK: {src}\n')
            f.write(f'  EMBED: {iframe_link}\n')
            f.write('**** **** **** **** **** **** **** **** **** ****\n\n')

        print(f'Episode {index + 1} done')

    driver.quit()
