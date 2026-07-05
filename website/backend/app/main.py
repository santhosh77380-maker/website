from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.config import settings
from app.utils.response import error_response

app = FastAPI(title=settings.APP_NAME)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(StarletteHTTPException)
async def http_exc(req, exc): return JSONResponse(status_code=exc.status_code, content=error_response(exc.detail))
@app.exception_handler(RequestValidationError)
async def val_exc(req, exc): return JSONResponse(status_code=422, content=error_response("Validation error", {"errors": exc.errors()}))
@app.exception_handler(Exception)
async def gen_exc(req, exc): return JSONResponse(status_code=500, content=error_response("Server error"))

from app.routers import auth, admin, student, attendance, marks, timetable
# We will add other routers here
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/api/v1/admins", tags=["Admins"])
app.include_router(student.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(attendance.router, prefix="/api/v1/attendance", tags=["Attendance"])
app.include_router(marks.router, prefix="/api/v1/marks", tags=["Marks"])
app.include_router(timetable.router, prefix="/api/v1/timetable", tags=["Timetable"])