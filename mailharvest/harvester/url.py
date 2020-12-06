# MailHarvest
#
# Author : Relarizky
# Github : @relarizky (https://github.com/relarizky)
# File   : url.py
# Last Modified : 12/07/20, 00:23 AM
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


import re


def filter_url_input(url: str) -> bool:
    """ filter url schema """

    return url.startswith("http://") or url.startswith("https://")


def filter_url_extension(url: str) -> bool:
    """ filter extension in url """

    end_path = url.split("/")[-1].lower()
    path_ext = end_path.split(".")[-1].lower()

    if path_ext == end_path:
        # this url is using route (without any extension)
        return True

    return path_ext in ["php", "html", "js", "css", "txt"]


def get_url_list(url: str, request_text: str) -> list:
    """ get list of url from request body/text """

    def filter_external_url(url_argument: str) -> bool:
        """ filter external url to be excluded """

        internal_url = re.search(r"http[s]?://[a-zA-Z0-9.]+", url).group()

        return re.search(rf"^{internal_url}", url_argument) is not None

    def add_url_to_path(path: str) -> str:
        """ add url to path """

        if not filter_url_input(path):
            return url + path
        else:
            return path

    # find available url
    url_list = re.findall(r"http[s]?://[a-zA-Z0-9-./=?]*", request_text)
    url_list = filter(filter_external_url, url_list)
    url_list = filter(filter_url_extension, list(url_list))
    url_list = list(url_list)

    # find available path
    path_list = re.findall(r"(src|href)=[\"']?([^\"']+)[\"']?", request_text)
    path_list = set([path[-1] for path in path_list])
    path_list = map(add_url_to_path, path_list)
    path_list = filter(filter_external_url, list(path_list))
    path_list = filter(filter_url_extension, list(path_list))
    path_list = list(path_list)

    return list(set(url_list + path_list))


def create_chunk(url_list: list, thread: int) -> list:
    """ generator for creating chunks of found url list """

    url_total = url_list.__len__()
    chunk_length = url_total // thread if url_total > thread else thread

    while url_list != []:
        chunk = []
        for iter in range(chunk_length):
            try:
                url = url_list.pop(0)
                chunk.append(url)
            except IndexError:
                break

        yield chunk
