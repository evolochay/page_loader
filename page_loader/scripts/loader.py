import argparse
import os
import sys
from page_loader.loader import download
from logs.log_config import init_logger


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
        sys.exit(0)
    except Exception:
        sys.exit(1)
    except FileExistsError:
        sys.exit(2)


if __name__ == '__main__':
    main()
