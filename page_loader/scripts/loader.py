import argparse
import os
from page_loader.loader import download
from logs.log_config import init_logger


logger = init_logger('app')


def make_parser():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument(
         '-o',
         '--output',
         default=os.getcwd(),
         type=str,
         help='set output directory',
     )
    parser.add_argument('page_adress', metavar='page_adress', type=str)

    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()

    downloaded_page = download(args.output, args.page_adress)
    print(downloaded_page)


if __name__ == '__main__':
    main()
