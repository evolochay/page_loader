import argparse
import os
import sys
from page_loader.loader import download
from logs.log_config import init_logger
import requests


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

    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)

    except PermissionError as pe:
        print(pe)
        sys.exit(1)

    except NotADirectoryError as nade:
        print(nade)
        sys.exit(1)

    except requests.exceptions.ConnectionError:
        print(f'Unable to connect to {args.page_adress}')
        sys.exit(1)

    except ConnectionAbortedError as cae:
        print(cae)
        sys.exit(1)

    except FileExistsError as fee:
        print(fee)
        sys.exit(1)

    except Exception as e:
        print(e)
        sys.exit(1)

    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
