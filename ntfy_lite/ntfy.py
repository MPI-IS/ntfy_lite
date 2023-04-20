"""
Module defining the push method, which send a message or the content of a file to an NTFY channel.
"""

import typing
import requests
from pathlib import Path
from enum import Enum, auto
from .ntfy2logging import Priority
from .actions import Action
from .utils import validate_url
from .error import NtfyError


class _DataManager:
    """
    The data pushed to ntfy is either a message (str) or the content of
    a file (i.e. file attachment, see https://ntfy.sh/docs/publish/#attachments).
    An instance of _DataManager ensures that at least message or filepath is not None and
    that only either message or filepath is not None. The context manager
    returns either the message string or the opened file, and ensure the file is closed
    (if data is a file).
    """

    def __init__(
        self, message: typing.Optional[str], filepath: typing.Optional[Path]
    ) -> None:
        # checking the user is at least pushing a message
        # or a file attachment
        if not any((message, filepath)):
            raise ValueError(
                "must push either a message or a filepath"
                " (no message nor filepath argument specified)"
            )

        # checking the user is not pushing both a message
        # and a file attachment
        if all((message, filepath)):
            raise ValueError(
                "can not push a message and a filepath " "at the same time."
            )

        # if pushing a file attachment, making
        # sure the file exists
        if filepath is not None:
            if not filepath.is_file():
                raise FileNotFoundError(f"failed to find file to attach ({filepath})")

        # self._data is either a file to the filepath,
        # or the str corresponding to message
        self._data: typing.Union[typing.IO, str]
        if filepath is not None:
            self._data = open(filepath, "rb")
        elif message is not None:
            self._data = message.encode(encoding="UTF-8", errors="replace").decode()
            self._data = message.encode(encoding="latin-1", errors="replace").decode()

    def __enter__(self) -> typing.Union[typing.IO, str]:
        return self._data

    def __exit__(self, _, __, ___) -> None:
        if not isinstance(self._data, str):
            self._data.close()


class DryRun(Enum):
    """
    An optional value of DryRun may be passed as an argument to the [ntfy_lite.ntfy.push][] function.

    - If 'off' is passed (default), then the [ntfy_lite.ntfy.push][] function will publish to ntfy.

    - If 'on' is passed, then the [ntfy_lite.ntfy.push][] function will *not* publish to ntfy.

    - If 'error' is passed, then the [ntfy_lite.ntfy.push][] function will raise an [ntfy_lite.error.NtfyError][].

    This is meant for testing.
    """

    on = auto()
    off = auto()
    error = auto()


def push(
    topic: str,
    title: str,
    message: typing.Optional[str] = None,
    priority: Priority = Priority.DEFAULT,
    tags: typing.Union[str, typing.Iterable[str]] = [],
    click: typing.Optional[str] = None,
    email: typing.Optional[str] = None,
    filepath: typing.Optional[Path] = None,
    attach: typing.Optional[str] = None,
    icon: typing.Optional[str] = None,
    actions: typing.Union[Action, typing.Sequence[Action]] = [],
    at: typing.Optional[str] = None,
    url: typing.Optional[str] = "https://ntfy.sh",
    dry_run: DryRun = DryRun.off,
) -> None:
    """
    Pushes a notification.

    ```python
    # basic usage
    import ntfy_lite as ntfy

    ntfy.push(
        "my topic", priority=ntfy.Priority.DEFAULT, message="my message"
    )
    ```

    For more documentation of all arguments, visit:
    [https://ntfy.sh/docs/publish/](https://ntfy.sh/docs/publish/)

    Args:
      topic: the ntfy topic on which to publish
      title: the title of the notification
      message: the message. It is optional and if None, then a filepath argument must be provided instead.
      priority: the priority of the notification
      tags (i.e. emojis): either a string (a single tag) or a list of string (several tags). see [supported emojis](https://docs.ntfy.sh)
      click: URL link to be included in the notification
      email: address to which the notification should also be sent
      filepath: path to the file to be sent as attachement.
        It is optional and if None, then a message argument must be provided instead.
      icon: URL to an icon to include in the notification
      actions: An action is either a [ntfy_lite.actions.ViewAction][]
        (i.e. a link to a website) or a [ntfy_lite.actions.HttpAction][]
        (i.e. sending of a HTTP GET, POST or PUT request to a website)
      at: to be used for delayed notification, see [scheduled delivery](https://ntfy.sh/docs/publish/#scheduled-delivery)
      url: ntfy server
      dry_run: for testing purposes, see [ntfy_lite.ntfy.DryRun][]
    """

    # the message manager:
    # - checks that either message or filepath is not None
    # - if filepath is not None, data is a file to the path
    # - else data is the UTF-8 conversion of message
    # This context manager makes sure that data get closed
    # (if a file)
    with _DataManager(message, filepath) as data:
        # checking that arguments that are expected to be
        # urls are urls
        urls = {"click": click, "attach": attach, "icon": icon}
        for attr, value in urls.items():
            # throw value error if not None
            # and not a url
            validate_url(attr, value)

        # some argument can be directly set in the
        # headers dict
        direct_mapping: typing.Dict[str, typing.Any] = {
            "Title": title,
            "At": at,
            "Click": click,
            "Email": email,
            "Icon": icon,
        }
        headers = {key: value for key, value in direct_mapping.items() if value}

        # adding priority
        headers["Priority"] = priority.value

        # adding tags
        if tags:
            if isinstance(tags, str):
                tags = (tags,)
            headers["Tags"] = ",".join([str(t) for t in tags])

        # adding actions
        if actions:
            if isinstance(actions, Action):
                actions = [actions]
            headers["Actions"] = "; ".join([str(action) for action in actions])

        # sending
        if dry_run == DryRun.off:
            response = requests.put(f"{url}/{topic}", data=data, headers=headers)
            if not response.ok:
                raise NtfyError(response.status_code, response.reason)
        elif dry_run == DryRun.error:
            raise NtfyError(-1, "DryRun.error passed as argument")
