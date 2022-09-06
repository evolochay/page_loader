import argparse
import os
import sys
import requests
from page_loader.page_loader import download
from requests import (HTTPError, ConnectionError)
from page_loader.user_messages import create_errors_message


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
    except ConnectionError:
        create_errors_message('connection error')
        sys.exit(1)
    except HTTPError:
        create_errors_message('HTTP error')
        sys.exit(1)
    except PermissionError:
        create_errors_message('permission denied')
        sys.exit(1)
    except requests.Timeout:
        create_errors_message('timeout')
        sys.exit(1)
    except Exception:
        create_errors_message('unexpected_err')
        sys.exit(1)

    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
