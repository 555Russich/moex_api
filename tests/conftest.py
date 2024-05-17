from pathlib import Path

from tests.my_logging import get_logger

TEST_DIR = Path(__file__).parent
TEST_DIR_CANDLES = TEST_DIR / 'candles'
TEST_DIR_CANDLES.mkdir(exist_ok=True)


def pytest_configure(config):
    """ https://stackoverflow.com/a/35394239/15637940 """
    import sys
    from tests import test_config
    sys.modules['config'] = test_config

    get_logger(TEST_DIR / 'test_log.log')
