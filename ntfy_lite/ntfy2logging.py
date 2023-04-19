"""
Module defining:

- LoggingLevel: typing union of all logging levels
- Priority: enumeration over ntfy priority levels
- level2priority: default mapping between logging levels and ntfy priority levels
"""

from enum import Enum
import typing
import logging

LoggingLevel = typing.Literal[  # type: ignore
    logging.DEBUG,  # type: ignore
    logging.INFO,
    logging.NOTSET,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL,
]
"""
Union of all logging levels (DEBUG, INFO, NOTSET,
WARNING, ERROR and CRITICAL)
"""


class Priority(Enum):
    """
    Enumeration of supported ntfy priority levels
    """

    MAX = "5"
    """MAX"""

    HIGH = "4"
    """HIGH"""

    DEFAULT = "3"
    """DEFAULT"""

    LOW = "2"
    """LOW"""

    MIN = "1"
    """MIN"""


level2priority: typing.Dict[LoggingLevel, Priority] = {
    logging.CRITICAL: Priority.MAX,
    logging.ERROR: Priority.HIGH,
    logging.WARNING: Priority.HIGH,
    logging.INFO: Priority.DEFAULT,
    logging.DEBUG: Priority.LOW,
    logging.NOTSET: Priority.MIN,
}
"""
Default mapping from logging level to ntfy priority level
(e.g. a record of level INFO maps to a notification of piority
level 3)
"""
