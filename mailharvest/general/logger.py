# MailHarvest
#
# Author : Relarizky
# Github : @relarizky (https://github.com/relarizky)
# File   : logger.py
# Last Modified : 12/03/20, 18:31 PM
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


import os
import re


DEFAULT_DIR = "saved/"  # change this if you'd like to


def get_domain_name(url: str) -> str:
    """ get domain name of given url """

    domain = re.findall("http[s]?://([a-zA-Z0-9.]+)", url)

    return domain[0] if domain != [] else "unknown"


def create_log_file(url: str, mail: str) -> None:
    """ create log file of found mail in default dir """

    file_name = DEFAULT_DIR + get_domain_name(url)

    with open(file_name, "a+") as log_file:
        log_file.write(mail + "\n")


def check_default_dir() -> bool:
    """ check existence of default dir """

    return os.path.isdir(DEFAULT_DIR)
