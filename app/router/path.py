from app.server.server import Response
from app.server.types import HttpMethod


class Path:
    def __init__(
        self,
        path: str,
        view: Response,
        start: bool = False,
        directory: bool = False,
        method: HttpMethod = HttpMethod.GET,
    ) -> None:
        self.path = path
        self.view = view
        self.start = start
        self.directory = directory
        self.method = method
