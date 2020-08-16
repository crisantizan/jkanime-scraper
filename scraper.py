from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os
import sys


class Scraper:
    def __init__(self, headless=False):
        # regular expressions
        self._regex = {
            'valid_link': r'https://jkanime.net/',
            'episode': r'^EPISODE [0-9]+$'
        }

        # xpath expressions
        self._xpath = {
            'LINKS': '//div[@id="episodes-content"]/div/a[@class="cap-header"]/@href',
            'IFRAME': '//iframe[@class="player_conte"]/@src',
            'SOURCE': '//source/@src',
            'NAVIGATION': '//a[@class="numbers"][last()]/text()'
        }

        self.link = self._input_link()
        self._folder = self._manage_folder()
        self._browser = self._init_browser(headless)
        self.title = re.sub(self._regex.get('valid_link'), '', self.link)

    def _init_browser(self, headless):
        option = webdriver.ChromeOptions()

        if headless:
            option.add_argument('headless')

        browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=option)
        return browser

    def _input_link(self):
        link = input('Enter link: ')

        # validate entered link
        if self._invalid_link(link):
            print(
                '\nError: the link entered is invalid, not comes from https://jkanime.net\n')
            sys.exit(1)

        # if there is in the end a "/" remove it
        return link if not link[-1:] == '/' else link[0:-1]

    def _get_links(self):
        # get pagination number, in this format: 1 - 6, 7 - 13
        pag = self._fetch(url=self.link, xpath=self._xpath['NAVIGATION'])
        # get last number and clean white spaces
        pag = pag[0].split('-')[1].strip()

        pages = int(pag)
        # generate links
        return [f'{self.link}/{num+1}' for num in range(pages)]

    def _fetch(self, url, xpath):
        self._browser.get(url)

        while True:
            time.sleep(0.3)
            data = self._scrape(xpath)
            if data:
                return data

    def _scrape(self, xpath):
        # get the innerhtml from the rendered page
        innerHTML = self._browser.execute_script(
            "return document.body.innerHTML")
        # Now use lxml to parse the page
        parsed = html.fromstring(innerHTML)
        # Get your element with xpath
        return parsed.xpath(xpath)

    def _write_in_file(self, filename, episode, url):
        with open(filename, mode='a', encoding='utf-8') as f:
            f.write(f'EPISODE {episode}\n')
            f.write(f'{url}\n\n')

    def _manage_folder(self):
        folder = 'animes'
        try:
            os.stat(folder)
        except:
            os.mkdir(folder)
        finally:
            return folder

    def _invalid_link(self, link):
        return not re.match(self._regex.get('valid_link'), link)

    def _last_episode(self):
        last = 0
        # if the current anime already locally exists
        try:
            os.stat(self.get_path())
            # open file and read content
            with open(self.get_path(), mode='r') as f:
                lines = f.readlines()
                for line in lines:
                    if not re.match(self._regex.get('episode'), line):
                        continue

                    # get episode number
                    last = int(line.strip().replace('EPISODE ', ''))

            return last

        except:
            # if not, return zero
            return last

    def get_path(self):
        return f'{self._folder}/{self.title}.txt'

    def run(self):
        last_episode = self._last_episode()
        links = self._get_links()

        # remove episodes already downloaded
        if not last_episode == 0:
            links = links[last_episode:]

        # up to date, stop program
        if not links:
            print('\n**** **** You\'re up to date with this anime! **** **** \n')
            self._browser.quit()
            sys.exit(0)

        # get new episodes, start after from the last
        for index, link in enumerate(links, start=last_episode):
            iframe_link = self._fetch(url=link, xpath=self._xpath['IFRAME'])[0]
            src = self._fetch(url=iframe_link, xpath=self._xpath['SOURCE'])[0]
            # write the current episode in file
            self._write_in_file(self.get_path(), episode=index + 1, url=src)
            print(f'Episode {index + 1} done')

        print('**** **** Scraping successfully! **** ****')
        self._browser.quit()
