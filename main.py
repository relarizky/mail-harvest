#!/usr/bin/python3

import os, sys
from emailfinder.color import *
from emailfinder.email_finder import *

color = Color()

def output_format(function):
    def banner(*args, **kwargs):
        print(color.GREEN + '                 _ _ _    _                           _   ')
        print(color.GREEN + '                (_) | |  | |                         | |  ')
        print(color.GREEN + ' _ __ ___   __ _ _| | |__| | __ _ _ ____   _____  ___| |_ ')
        print(color.GREEN + '| \'_ ` _ \ / _\ | | |  __  |/ _` | \'__\ \ / / _ \/ __| __|')
        print(color.GREEN + '| | | | | | (_| | | | |  | | (_| | |   \ V /  __/\__ \ |_ ')
        print(color.GREEN + '|_| |_| |_|\__,_|_|_|_|  |_|\__,_|_|    \_/ \___||___/\__|')
        print(color.YELLOW+ '                                             [Version 1.0]\n')
        function(*args, **kwargs)
    return banner


def valid_url(function): # filtering unvalid url (not with schema)
    def check(*args, **kwargs):
        if len(kwargs) != 0:
            url = kwargs['url']
        else:
            url = args[0]
        if not (url.startswith('http://') or url.startswith('https://')):
            print(color.RED + current_time(), 'Please, input a valid URL.')
        else:
            function(*args, **kwargs)
    return check


@output_format
def usage():
    print('[+] Usage\t: {} <url> <filename>'.format(sys.argv[0]))
    print('[+] Example\t: {} http://target.com/ list_mail.txt'.format(sys.argv[0]))


@output_format
@valid_url
def main(url, file):
    try:
        email_finder = EmailFinder(url_target = url, file_name = file)
        email_finder.start_crawling()
    except KeyboardInterrupt:
        print(color.RED + current_time(), 'you stoped the program.')
        sys.exit(1)


if __name__ == '__main__':

    if os.path.exists(DIRECTORY) != True:
        print(color.RED + current_time(), 'Can\'t find {} directory.'.format(DIRECTORY))
        sys.exit(1)

    if len(sys.argv) != 3:
        usage()
        sys.exit(0)

    url, file = sys.argv[1], sys.argv[2]
    main(url, file)
