""" ntfy lite: ntfy logging Handler example """

import time
import typing
import logging
import tempfile
import ntfy_lite as ntfy
from pathlib import Path

logger = logging.getLogger("ntfy_lite")

topic = "ntfy_lite_demo"  # or something else
email = None  # write your email here if you wish


def _error_callback(e: Exception):
    """
    Will be called if the system fails to send ntfy notification,
    for any reason.
    """
    print(f"failed to send ntfy notification: {e}")


def _configure_log(logfile: Path) -> None:
    """
    Configure logging: logs will be printed in the terminal,
    printed to logfile, and sent as ntfy notification.
    """

    # configuration for the ntfy handler #

    # tags associated to the logging level
    level2tags = {
        logging.ERROR: ("broken_heart", "ant"),
        logging.INFO: ("left_speech_bubble",),
        logging.DEBUG: ("hammer_and_wrench",),
    }

    # mapping from logging level to ntfy priority
    level2priority = {
        logging.CRITICAL: ntfy.Priority.MAX,
        logging.ERROR: ntfy.Priority.HIGH,
        logging.WARNING: ntfy.Priority.HIGH,
        logging.INFO: ntfy.Priority.DEFAULT,
        logging.DEBUG: ntfy.Priority.LOW,
        logging.NOTSET: ntfy.Priority.MIN,
    }

    # sending email on errors
    level2email: typing.Dict[ntfy.LoggingLevel, str]
    if email is not None:
        level2email = {logging.ERROR: email}
    else:
        level2email = {}

    # when error: sending the content of the log file
    level2filepath = {logging.ERROR: logfile}

    # the handler that will send ntfy notifications
    # note: most arguments are optionals and default
    #       to reasonable values
    ntfy_handler = ntfy.NtfyHandler(
        topic,
        error_callback=_error_callback,
        level2tags=level2tags,
        level2priority=level2priority,
        level2filepath=level2filepath,
        level2email=level2email,
    )

    # other handlers #

    # printing to terminal
    stream_handler = logging.StreamHandler()

    # printing to file
    file_handler = logging.FileHandler(logfile)

    # setting up logs #

    handlers: typing.Optional[typing.Iterable[logging.Handler]]
    handlers = [stream_handler, file_handler, ntfy_handler]

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s | %(name)s |  %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        handlers=handlers,
    )


def _do(error: bool, iteration: int) -> None:
    """
    Dummy function that prints to debug, and
    to info (if not error) or to error (otherwise).
    """

    logger.debug(f"doing iteration {iteration}")
    if not error:
        logger.info(f"did iteration {iteration}")
    else:
        logger.error(f"failed to do iteration {iteration}")


def _run(logfile=Path) -> None:
    """
    Calls the dummy function '_do' every 2 seconds for 20 seconds,
    setting errors to be logged every 4 seconds
    """

    logger = logging.getLogger("run function")
    logger.info(f"running for 20 seconds, visit: https://ntfy.sh/{topic}")

    # running for 10 seconds
    iteration = 1
    count = 0
    start = time.time()
    error = False
    while time.time() - start < 20:
        _do(error, iteration)
        iteration += 1
        count += 1
        if error:
            error = False
        elif count >= 4:
            error = True
            count = 0
        time.sleep(2)

    logger.info("exit")


def run() -> None:
    print(f"logging to htts://ntfy.sh/{topic}")

    with tempfile.TemporaryDirectory() as tmp:
        logfile = Path(tmp) / "ntfy_lite_demo_handler.txt"

        # setting up the logs
        _configure_log(logfile)

        # running for 20 seconds
        try:
            _run(logfile)
        except Exception as e:
            print(f"failed with error: {e}")
