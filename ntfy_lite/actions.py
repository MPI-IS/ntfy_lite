import typing
from enum import Enum, auto
from .utils import validate_url


class Action:
    """
    Superclass for action buttons.
    See: https://ntfy.sh/docs/publish/#action-buttons

    Args:
      action: name of the action (e.g. 'view', 'http')
      label: description of the action
      url: where the action redirects
      clear: if true, the notification is deleted upon click
    """

    def __init__(self, action: str, label: str, url: str, clear: bool = False):

        validate_url("Action.url", url)

        self.action = action
        self.label = label
        self.url = url
        if clear:
            self.clear = "true"
        else:
            self.clear = "false"

    def _str(self, attrs: typing.Tuple[str, ...]) -> str:
        values = {attr: getattr(self, attr) for attr in attrs}
        return ", ".join(
            [self.action]
            + [f"{attr}={value}" for attr, value in values.items() if value is not None]
        )


class ViewAction(Action):
    """
    Class encapsulating the information of a view action.
    See: https://ntfy.sh/docs/publish/#open-websiteapp
    For arguments: see documentation of the Action superclass
    """

    def __init__(self, label: str, url: str, clear: bool = False) -> None:
        super().__init__("view", label, url, clear)

    def __str__(self) -> str:
        _attrs = ("label", "url", "clear")
        return self._str(_attrs)


class HttpMethod(Enum):
    """
    List of methods supported by instances
    of HttpAction.
    """

    GET = auto()
    POST = auto()
    PUT = auto()


class HttpAction(Action):
    """
    Class encapsulating the information of a view action.
    See: https://ntfy.sh/docs/publish/#send-http-request
    """

    def __init__(
        self,
        label: str,
        url: str,
        clear: bool = False,
        method: HttpMethod = HttpMethod.GET,
        headers: typing.Optional[typing.Mapping[str, str]] = None,
        body: typing.Optional[str] = None,
    ):
        super().__init__("http", label, url, clear)
        self.method = method.value
        self.headers = headers
        self.body = body

    def __str__(self) -> str:
        _attrs = ("label", "url", "clear", "method", "body")
        main = self._str(_attrs)
        if not self.headers:
            return main
        headers_str = ", ".join(
            [f"headers.{key}={value}" for key, value in self.headers.items()]
        )
        return main + ", " + headers_str
