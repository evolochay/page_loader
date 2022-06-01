from main.page_loader import download

RESULT = 'here will be something'


def test():
    result = download()
    assert result == RESULT
