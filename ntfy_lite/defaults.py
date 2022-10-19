import typing
import logging
from .ntfy2logging import LoggingLevel

level2tags: typing.Dict[LoggingLevel, typing.Tuple[str, ...]] = {
    logging.CRITICAL: ("fire",),
    logging.ERROR: ("broken_heart",),
    logging.WARNING: ("warning",),
    logging.INFO: ("artificial_satellite",),
    logging.DEBUG: ("speech_balloon",),
    logging.NOTSET: tuple(),
}
"""
Default mapping from logging level to tags, i.e. tags
that will be added to notifications corresponding to the
key logging level.
"""
