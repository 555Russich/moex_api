import logging
import sys
from pathlib import Path


def get_logger(filepath: Path) -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        encoding='utf-8',
        format="[{asctime},{msecs:03.0f}]:[{levelname}]:{message}",
        datefmt='%d.%m.%Y %H:%M:%S',
        style='{',
        handlers=[
            logging.FileHandler(filepath, mode='a'),
            logging.StreamHandler(sys.stdout),
        ]
    )

    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('tinkoff').setLevel(logging.WARNING)
    logging.getLogger('grpc').setLevel(logging.WARNING)
