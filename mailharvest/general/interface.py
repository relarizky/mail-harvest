# MailHarvest
#
# Author : Relarizky
# Github : @relarizky (https://github.com/relarizky)
# File   : interface.py
# Last Modified : 12/05/20, 00:35 AM
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


import sys
import datetime


def banner() -> None:
    print(" __  __       _ _ _    _                           _")
    print("|  \\/  |     (_) | |  | |                         | |")
    print("| \\  / | __ _ _| | |__| | __ _ _ ____   _____  ___| |_")
    print("| |\\/| |/ _` | | |  __  |/ _` | '__\\ \\ / / _ \\/ __| __|")
    print("| |  | | (_| | | | |  | | (_| | |   \\ V /  __/\\__ \\ |_")
    print("|_|  |_|\\__,_|_|_|_|  |_|\\__,_|_|    \\_/ \\___||___/\\__|")
    print("                                        [Version 1.0.1]\n")


def current_time() -> None:
    time = datetime.datetime.now()
    hour = time.hour
    minute = time.minute
    second = time.second

    return f"[{hour}:{minute}:{second}]"


def help() -> None:
    print(f"[+] Usage\t: {sys.argv[0]} <url> <thread> <timeout>")
    print(f"[+] Example\t: {sys.argv[0]} http://target.com 5 15")
