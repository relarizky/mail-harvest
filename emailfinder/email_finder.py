import re
import sys
import tld
import requests as Request
from datetime import datetime
from random import choice
from .color import *

DIRECTORY = 'saved/' # Change this to your wanted dirname

def filter_url(real_url, found_url):
    # filter_url is for checking whether the found url is the part of the target's url
    # Or its just a part of third-party's url
    try:
        real_url =  tld.get_tld(real_url, as_object = True)
        found_url = tld.get_tld(found_url, as_object = True)
    except (tld.exceptions.TldBadUrl, tld.exceptions.TldDomainNotFound,
            tld.exceptions.MissingSchema) as Ex:
        print('[-] Domain {} is invalid'.format(real_url))
        sys.exit(1)

    return real_url.parsed_url.netloc == found_url.parsed_url.netloc


def filter_path(url_path):
    # filter_path is for checking whether the url path is file with these extensions or not.
    try:
        extension = [
            'jpg', 'css', 'js', 'jpeg',
            'png', 'svg', 'pdf', 'xml',
            'zip', 'txt', 'rss', 'ico',
            'mp4', 'gif'
        ]
        url = tld.get_tld(url_path, as_object = True)
        path = url.parsed_url.path.split('.')
        return path[-1].lower() not in extension
    except (tld.exceptions.TldBadUrl, tld.exceptions.TldDomainNotFound) as Ex:
        pass


def valid_url(url):
    # valid_url is for checking whether the choiced url is a valid url (with schema) or not.
    return 'http://' in url.lower() or 'https://' in url.lower()


def current_time():
    time = datetime.now()
    hour = time.hour
    minute = time.minute
    second = time.second
    return '[{}:{}:{}]'.format(hour, minute, second)


# this lambda function is for deleting all None in a list
delete_none = lambda element : element != None


# this lambda function is for deleting all files that's the shape similar with mail format (with @).
filter_mail = lambda element : element.split('.')[-1] not in ['jpg', 'png', 'jpeg', 'gif', 'x']


class EmailFinder( Color ):

    saved_mail = set() # we store the found mail into set for preventing the same mail in the saved file.
    done_url = set() # this is a list of url that has been crawled.
    first_url = None # this is the first url that user input

    def __init__(self, url_target = None, file_name = 'mails.txt'):
        self.file_name = file_name
        self.first_url = url_target
        self.url_target = url_target
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

    def save_mail(self, mail):
        ' Saving the found mail into the file '
        file_name = DIRECTORY + self.file_name

        if mail not in self.saved_mail: # Checking whether the mail has been saved before or not
            with open(file_name, 'a+') as saved_file:
                saved_file.write(mail + '\n')
            saved_file.close()
            self.saved_mail.add(mail)

    def fetch_mail(self, url):
        ' Fetch the available mail in web page '
        regex = re.compile(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)')
        headers = {'user-agent' : self.user_agent}
        requests = Request.Session()

        with requests.get(url, headers = headers) as request:
            if request.status_code != 404: # If response code is not 404, we can fetch the mail
                source = request.text
                found_mail = regex.findall(source)
                found_mail = list(filter(filter_mail, found_mail))

                for mail in found_mail: # Saving all the found mail(s) into the file.
                    print(
                        self.BOLD + self.GREEN + current_time(),
                        'found', self.BOLD + self.GREEN + '{}'.format(mail),
                        'in', self.GREEN + '{}'.format(url)
                    )
                    self.save_mail(mail)

    def start_crawling(self):
        ' Fetch the available url in href and src attributes of web page, then send it to fetch_mail '
        regex = re.compile(r'(href|src|action)="(.*?)"', re.IGNORECASE)
        headers = {'user-agent' : self.user_agent}
        requests = Request.Session()

        with requests.get(self.url_target, headers = headers, allow_redirects = True) as request:
            if request.status_code != 404:
                source = request.text
                found_url = regex.findall(source) # Fetch url with regex
                found_url = [url[-1] for url in found_url] # Fetch url from regex's result
                found_url = set(filter(filter_path, found_url)) # filter the file in url, we use set for preventing same url
                found_url = set(filter(valid_url, found_url)) # filter the unvalid url (not with schema)
                found_url = [
                    url if filter_url(self.url_target, url) == True else None for url in found_url
                ] # filtering third-party url
                found_url = list(filter(delete_none, found_url)) # deleting all None values in list found_url

                print(self.BOLD + self.GREEN + current_time(), 'found {} url from {}'.format(
                    str(len(found_url)), self.url_target
                    )
                )

                for url in found_url: # Fetch email of all found url(s)
                    if url != None:
                        print(self.GREEN + current_time(), 'start crawling from {}'.format(url))
                        self.fetch_mail(url)
                else:
                    self.done_url.add(self.url_target) # put url_target to done_url cuz it has finished its job :D

                loop = 0

                while True: # select the new url_target
                    if len(found_url) == 0: # if none url found, repeat crawling from the first_url
                        self.url_target = self.first_url
                        break
                    elif loop == 3:
                        self.url_target = self.first_url
                        break
                    self.url_target = choice(list(found_url)) # select url randomly
                    if self.url_target in self.done_url: # if the selected url is in done_url, repeat.
                        loop += 1
                        continue
                    break

                self.start_crawling()
