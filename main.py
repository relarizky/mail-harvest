#!/usr/bin/env python3
# MailHarvest
#
# Author : Relarizky
# Github : @relarizky (https://github.com/relarizky)
# File   : main.py
# Last Modified : 12/05/20, 00:37 AM
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


from sys import argv, exit, setrecursionlimit
from random import choice
from typing import Callable
from mailharvest.general.interface import banner, current_time, help
from mailharvest.general.logger import check_default_dir, DEFAULT_DIR
from mailharvest.harvester.request import MailHarvest, create_request
from mailharvest.harvester.url import (
    filter_url_input, get_url_list,
    create_chunk
)


# set default amount of recursion can be done
setrecursionlimit(300)


done_url = []   # list of url that has been scraped


def validate_url(func: Callable) -> Callable:
    """ decorator for validating given url input from user """

    def validate(*args: list):
        if not filter_url_input(args[0]):
            print(current_time(), "your given URL is invalid!")
        else:
            return func(*args)

    return validate


def validate_connection(func: Callable) -> Callable:
    """ decorator for validating target connection """

    def validate(*args: list):
        request = create_request(args[0], 5)

        if request is False:
            print(current_time(), "target website seems to be down")
        else:
            return func(*args)

    return validate


@validate_url
@validate_connection
def main(url: str, thread_size: int, timeout: int) -> None:
    """ main function of MailHarvest """

    done_url.append(url)
    print(current_time(), f"looking for available url on {url}")

    request_text = create_request(url, timeout)
    if request_text is False:
        print(
            current_time(),
            "there were some error occured while making request"
        )
        exit(0)

    url_list1 = get_url_list(url, request_text)
    url_list2 = url_list1.copy()
    url_chunk = create_chunk(url_list1, thread_size)

    print(current_time(), f"found {len(url_list2)} urls on {url}")

    while True:
        thread_list = []
        stop_signal = False

        for count in range(thread_size):
            try:
                thread = MailHarvest(url, url_chunk.__next__(), timeout)
                thread.daemon = True
                thread.start()
                thread_list.append(thread)
            except StopIteration:
                stop_signal = True
                break

        for thread in thread_list:
            try:
                # wait for all the thread to be done
                # before creating other threads
                thread.join()
            except KeyboardInterrupt:
                if thread.is_alive():
                    thread.stop()
                print(current_time(), "all the threads are stopped")
                print(current_time(), "successfully stopped the program")
                exit(0)

        if stop_signal is True:
            break

    if url_list2 != []:
        while url_list2 != []:
            next_url = url_list2.pop(0)
            if next_url in done_url:
                continue
            else:
                break
    else:
        next_url = choice(done_url)

    main(next_url, thread_size, timeout)


if __name__ == "__main__":
    banner()

    if not check_default_dir():
        print(current_time(), f"can't find default dir {DEFAULT_DIR}")
        exit(1)

    if argv.__len__() != 4:
        help()
        exit(0)

    try:
        url, thread, timeout = argv[1], int(argv[2]), int(argv[3])
        main(url, thread, timeout)
    except RecursionError:
        print(current_time(), "you have reached maximum recursion depth")
    except KeyboardInterrupt:
        print(current_time(), "successfully stopped the program")
