import argparse
import os
import sys
from page_loader.page_loader import download
from requests import HTTPError, ConnectionError
from page_loader.user_messages import Message


def make_parser():
    parser = argparse.ArgumentParser(description="Page loader")
    parser.add_argument("page_adress", metavar="page_adress", type=str)
    parser.add_argument(
        "-o",
        "--output",
        default=os.getcwd(),
        type=str,
        help="set output directory",
    )

    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    try:
        downloaded_page = download(args.page_adress, args.output)
        print(downloaded_page)
    except ConnectionError:
        print(Message.CONNECTION_ERROR)
        sys.exit(1)
    except HTTPError:
        print(Message.HTTP_ERROR)
        sys.exit(1)
    except PermissionError:
        print(Message.PERMISSION_DENIED)
        sys.exit(1)
    except Exception:
        print(Message.UNEXPECTED)
        sys.exit(1)

    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
