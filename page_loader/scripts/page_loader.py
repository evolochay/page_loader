import argparse
import os
import sys
from page_loader.page_loader import download
from logs.log_config import init_logger
from requests import (HTTPError, ConnectionError, Timeout)


logger = init_logger('app')


def make_parser():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('page_adress', metavar='page_adress', type=str)
    parser.add_argument(
        '-o',
        '--output',
        default=os.getcwd(),
        type=str,
        help='set output directory',
    )

    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    try:
        downloaded_page = download(args.page_adress, args.output)
        print(downloaded_page)
    except (ConnectionError,
            HTTPError,
            OSError,
            PermissionError,
            Timeout,
            ):
        sys.exit(1)

    else:
        sys.exit(0)

def create_errors_message(problem_name):
    if problem_name == 'connection error':
        print('IM HERE')
        message = 'Please, check Internet connection'
    elif problem_name == 'HTTP error':
        message = 'You`ve got some problem with HTTP'
    print(message)

if __name__ == '__main__':
    main()