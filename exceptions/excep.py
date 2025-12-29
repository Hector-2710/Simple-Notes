from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse

class AppBaseError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class DatabaseError(AppBaseError):
    def __init__(self):
        super().__init__(status_code=500, detail="A database error occurred")
        
class EmailAlreadyExists(AppBaseError):
    def __init__(self, email: str):
        super().__init__(status_code=409, detail=f"User with email {email} already exists")

def register_exception_handlers(app):
    @app.exception_handler(AppBaseError)
    async def app_base_error_handler(request: Request, exc: AppBaseError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

