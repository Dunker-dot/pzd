from __future__ import annotations

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.config import SECRET_KEY, SESSION_COOKIE
from app.database import get_user_by_username, init_db
from app.security import verify_password

app = FastAPI(title="ESL门店演示系统 M1")
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie=SESSION_COOKIE,
    https_only=False,
    same_site="lax",
)

templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup() -> None:
    init_db()


def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return None
    return user


@app.get("/")
def home() -> RedirectResponse:
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)


@app.get("/login")
def login_page(request: Request):
    if get_current_user(request):
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password_hash"]):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "用户名或密码错误"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    request.session["user"] = {"id": user["id"], "username": user["username"]}
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)


@app.get("/dashboard")
def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": user["username"],
        },
    )


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
