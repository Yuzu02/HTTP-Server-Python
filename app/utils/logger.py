from app.server.server import Response

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
BOLD = "\033[1m"


def logger(response: Response) -> None:
    """A simple logger."""
    if response.code.name == 'OK':
        message = f"{GREEN}"
    else:
        message = f"{RED}"
    message += f"{BOLD}{response.rq.method.name} {response.code.name} "
    message += f"{response.rq.path}"
    message += RESET
    print(message)
