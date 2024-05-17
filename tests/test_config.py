import sys
from pathlib import Path


DIR_PROJECT = Path(__file__).parent.parent
DIR_GLOBAL = DIR_PROJECT.parent
if DIR_GLOBAL.name != 'Trading':
    raise FileNotFoundError(f'Project must be in `Trading` directory.')
sys.path.append(str(DIR_GLOBAL.absolute()))

DIR_CANDLES = None, None, None, None, None
from config_global import DIR_CANDLES # noqa
