"""
Модуль функций автозапуска при старте пакета
"""

from . import __version__
from . import cmd


if __name__ == '__main__':
    cmd.start()
