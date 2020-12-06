# MailHarvest
#
# Author : Relarizky
# Github : @relarizky (https://github.com/relarizky)
# File   : mail.py
# Last Modified : 12/03/20, 18:59 PM
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


def fetch_mail(request_text: str) -> list:
    """ fetch mail of given request text  """

    mail_list = re.findall(
        r"[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-z]{2,3}",
        request_text
    )

    return mail_list


def filter_mail(mail: str) -> bool:
    """ filter found mail to make it sure that it is mail """

    black_list_ext = [
        "ico", "jpg", "png", "jpeg",
        "gif", "svg", "x", "css",
        "js"
    ]

    return mail.split(".")[-1] not in black_list_ext
