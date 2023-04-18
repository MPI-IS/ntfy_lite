"""
Module defining the NtfyHandler class.

The NtfyHandler is a logging handler, i.e. an handler suitable for the
[python logging package](https://docs.python.org/3/library/logging.html)

``` python
# Basic usage

import logging
import ntfy_lite as ntfy

ntfy_handler = ntfy.NtfyHandler("my_topic")

logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s | %(name)s |  %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        handlers=(ntfy_handler,),
)
```


"""

import logging
import typing
from pathlib import Path
from .ntfy2logging import LoggingLevel, Priority, level2priority
from .defaults import level2tags
from .ntfy import DryRun, push


class NtfyHandler(logging.Handler):
    """Subclass of [logging.Handler](https://docs.python.org/3/library/logging.html#handler-objects)
    that pushes ntfy notifications.

    The notification title will be the record name, and the
    notification message will be either the record message or a
    file attachment (depending on the level2filepath argument).
    """

    def __init__(
        self,
        topic: str,
        url: str = "https://ntfy.sh",
        twice_in_a_row: bool = True,
        error_callback: typing.Optional[
            typing.Callable[[Exception], typing.Any]
        ] = None,
        level2tags: typing.Dict[LoggingLevel, typing.Tuple[str, ...]] = level2tags,
        level2priority: typing.Dict[LoggingLevel, Priority] = level2priority,
        level2filepath: typing.Dict[LoggingLevel, Path] = {},
        level2email: typing.Dict[LoggingLevel, str] = {},
        dry_run: DryRun = DryRun.off,
    ):
        """
        Args:
          topic: Topic on which the notifications will be pushed.
          url: https://ntfy.sh by default.
          twice_in_a_row: If False, if several similar records (similar: same name
            and same message) are emitted, only the first one will result in notification
            being pushed (to avoid the channel to reach the accepted limits of notifications).
          error_callback: It will be called if a NtfyError is raised when pushing a notification.
          level2tags: mapping between logging level and tags to be associated with the notification
          level2priority: mapping between the logging level and the notification priority.
          level2filepath: If for the logging level of the record a corresponding filepath is set,
            the notification will contain no message but a correspondinf file attachment
            (be aware of the size limits, see https://ntfy.sh/docs/publish/#attach-local-file).
          level2email: If an email address is specified for the logging level of the record,
            the ntfy notification will also request a mail to be sent.
          dry_run: For testing. If 'on', no notification will be sent. If 'error', no notification will be sent,
            instead a NtfyError are raised.
        """
        super().__init__()
        self._url = url
        self._topic = topic
        self._last_messages: typing.Optional[typing.Dict[str, str]]
        self._last_messages = None if twice_in_a_row else {}
        self._level2tags = level2tags
        self._level2priority = level2priority
        self._level2filepath = level2filepath
        self._level2email = level2email
        self._error_callback = error_callback
        self._dry_run = dry_run

        for logging_level in level2priority:
            if logging_level not in self._level2priority:
                raise ValueError(
                    f"NtfyHandler, level2priority argument: missing mapping from "
                    f"logging level {logging_level} to ntfy priority level"
                )

    def _is_new_record(self, record: logging.LogRecord) -> bool:
        if self._last_messages is None:
            return True
        try:
            previous_message = self._last_messages[record.name]
        except KeyError:
            self._last_messages[record.name] = record.msg
            return True
        if record.msg == previous_message:
            return False
        self._last_messages[record.name] = record.msg
        return True

    def emit(self, record: logging.LogRecord) -> None:
        """
        Push the record as an ntfy message.
        """
        if self._last_messages and not self._is_new_record(record):
            return
        try:
            filepath = self._level2filepath[record.levelno]
            message = None
        except KeyError:
            filepath = None
            message = record.msg
        try:
            email = self._level2email[record.levelno]
        except KeyError:
            email = None
        try:
            tags = self._level2tags[record.levelno]
        except KeyError:
            tags = tuple()
        try:
            push(
                self._topic,
                record.name,
                message=message,
                priority=self._level2priority[record.levelno],
                tags=tags,
                email=email,
                filepath=filepath,
                url=self._url,
                dry_run=self._dry_run,
            )
        except Exception as e:
            if self._error_callback is not None:
                self._error_callback(e)
            self.handleError(record)
