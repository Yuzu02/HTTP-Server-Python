from app.server.server import Response, Request
from app.server.types import HttpStatusCode


def get_response(request: Request, message: str = "", content_type: str = "text/plain") -> Response:
    """Create an OK response"""
    return Response(
        body=message,
        code=HttpStatusCode.OK,
        headers={
            'Content-Type': content_type,
            'Content-Length': len(message),
        },
        request=request,
    )


def get_response_not_found(request: Request) -> Response:
    """Create an 404 response"""
    return Response(
        code=HttpStatusCode.NOT_FOUND,
        request=request,
    )
