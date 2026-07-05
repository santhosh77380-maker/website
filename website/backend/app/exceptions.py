from fastapi import HTTPException, status
class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not found"): super().__init__(status_code=404, detail=detail)
class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"): super().__init__(status_code=400, detail=detail)
class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized"): super().__init__(status_code=401, detail=detail, headers={"WWW-Authenticate": "Bearer"})
class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden"): super().__init__(status_code=403, detail=detail)
class DuplicateResourceException(HTTPException):
    def __init__(self, detail: str = "Conflict"): super().__init__(status_code=409, detail=detail)