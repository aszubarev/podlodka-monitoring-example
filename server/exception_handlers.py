from starlette.requests import Request
from starlette.responses import Response, JSONResponse


# noinspection PyUnusedLocal
def zero_division_error_handler(request: Request, exc: Exception) -> Response:
    content = {
        'success': False,
        'errors': [
            {
                'code': 'invalid',
                'message': "Can't divide by zero",
                'meta': None
            }
        ]
    }
    return JSONResponse(content, status_code=400)
