# MailHarvest
#
# Author : Relarizky
# Github : @relarizky (https://github.com/relarizky)
# File   : request.py
# Last Modified : 12/05/20, 00:34 AM
#
# Copyright (c) 2020 Relarizky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from mailharvest.harvester.mail import fetch_mail, filter_mail
from mailharvest.general.logger import create_log_file
from mailharvest.general.interface import current_time
from requests.exceptions import RequestException
from typing import Union
import threading
import requests


def create_request(url: str, timeout: int) -> Union[str, bool]:
    """ create request and return request text/body """

    header = {"user-agent": "Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1"}

    try:
        with requests.get(url, headers=header, timeout=timeout) as request:
            if request.status_code == 200:
                return_value = request.text
            else:
                return_value = ""
    except RequestException:
        return_value = False

    return return_value


class MailHarvest(threading.Thread):

    _signal = threading.Event()

    def __init__(self, url: str, urls: list, timeout: int):
        self.url = url
        self.urls = urls
        self.timeout = timeout
        threading.Thread.__init__(self)

    def _harvest_mail(self) -> None:
        """ perform mail harvesting to given url """

        timeout = self.timeout
        url_list = self.urls

        for url in url_list:
            print(current_time(), f"start crawling on {url}")
            request_text = create_request(url, timeout)
            if self.is_stopped():
                # user stopped the program with CTRL + C
                break
            if request_text is False:
                # there was an error while making a request
                break
            if request_text is not None and request_text is not False:
                found_mail = fetch_mail(request_text)
                found_mail = filter(filter_mail, found_mail)
                for mail in found_mail:
                    print(current_time(), f"found {mail} on {url}")
                    create_log_file(self.url, mail)

    def run(self):
        """ represents the thread activity """

        self._harvest_mail()

    def stop(self):
        """ give signal to all the threads to stop """

        self._signal.set()

    def is_stopped(self):
        """ check the signal for all threads """

        return self._signal.is_set()
