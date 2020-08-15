import requests
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os

XPATH_LINKS = '//div[@id="episodes-content"]/div/a[@class="cap-header"]/@href'
XPATH_IFRAME = '//iframe[@class="player_conte"]/@src'
XPATH_SOURCE = '//source/@src'
XPATH_NAVIGATION = '//a[@class="numbers"][last()]/text()'


def init_driver(headless=True):
    option = webdriver.ChromeOptions()

    if headless:
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
    # get pagination number, in this format: 1 - 6, 7 - 13
    pag = fetch(browser=browser, url=link, xpath=XPATH_NAVIGATION)
    # get last number and clean white spaces
    pag = pag[0].split('-')[1].strip()

    pages = int(pag)
    # generate links
    return [f'{link}/{num+1}' for num in range(pages)]


def fetch(browser, url, xpath):
    browser.get(url)

    while True:
        time.sleep(0.2)
        data = scrape(browser, xpath)
        if data:
            return data


def input_link():
    link = input('Enter link: ')
    # if there is in the end a "/" remove it
    return link if not link[-1:] == '/' else link[0:-1]


def manage_folder():
    folder = 'animes'
    try:
        os.stat(folder)
    except:
        os.mkdir(folder)
    finally:
        return folder


def write_in_file(filename, episode, url):
    with open(filename, mode='a', encoding='utf-8') as f:
        f.write(f'EPISODE {episode}\n')
        f.write(f'{url}\n\n')


def main():
    link = input_link()
    folder = manage_folder()
    title = re.sub(r'https://jkanime.net/', '', link)

    driver = init_driver(headless=False)
    links = get_links(browser=driver, link=link)

    for index, link in enumerate(links):
        iframe_link = fetch(browser=driver, url=link, xpath=XPATH_IFRAME)[0]
        src = fetch(browser=driver, url=iframe_link, xpath=XPATH_SOURCE)[0]

        write_in_file(f'{folder}/{title}.txt', index + 1, src)
        print(f'Episode {index + 1} done')

    print('**** **** Scraping successfully! **** ****')
    driver.quit()


if __name__ == '__main__':
    main()
