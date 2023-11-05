from app.server.server import Request, Response
from app.server.types import HttpStatusCode
from app.utils.response import get_response, get_response_not_found


def index(request: Request) -> Response:
    return get_response(request=request)


def echo(request: Request) -> Response:
    message = request.path.split('/echo/')[1]
    return get_response(request=request, message=message)


def user_agent(request: Request) -> Response:
    message = request.headers.get('User-Agent')
    return get_response(request=request, message=message)


def post_file(request: Request, directory: str) -> Response:
    path = request.path.split('/files/')[1]
    with open(f"{directory}/{path}", "w", encoding='UTF-8') as file:
        file.write(request.body)
        file.close()
    return Response(request=request, code=HttpStatusCode.CREATED)


def get_file(request: Request, directory: str) -> Response:
    path = request.path.split('/files/')[1]
    try:
        with open(f"{directory}/{path}", 'r', encoding='UTF-8') as file:
            response = get_response(
                request=request,
                message=file.read(),
                content_type="application/octet-stream")
            file.close()
    except FileNotFoundError:
        response = get_response_not_found(request)
    return response
