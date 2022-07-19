from sanic import Blueprint, Request
from sanic.response import json
from sanic.exceptions import BadRequest

from aiohttp import ClientSession
from urllib.parse import urlencode


Auth = Blueprint("auth", url_prefix="/auth")


def create_url(url: str, **kwargs) -> str:
    return url + urlencode(kwargs)


@Auth.get("/login/google")
async def google_login(request: Request):
    return json({
        "login_url": create_url(
            "https://accounts.google.com/o/oauth2/v2/auth?",
            scope="email profile",
            state="",
            redirect_uri=f"{request.app.config.BASE_URL}{request.app.url_for('auth.google_callback')}",
            response_type="code",
            client_id=request.app.config.AUTH["GOOGLE_CLIENT_ID"],
            access_type="online"
        )
    })


@Auth.get("/login/naver")
async def naver_login(request: Request):
    return json({
        "login_url": create_url(
            "https://nid.naver.com/oauth2.0/authorize?",
            scope="email name",
            state="",
            redirect_uri=f"{request.app.config.BASE_URL}{request.app.url_for('auth.naver_callback')}",
            response_type="code",
            client_id=request.app.config.AUTH["NAVER_CLIENT_ID"]
        )
    })


@Auth.get("/callback/google")
async def google_callback(request: Request):
    async with ClientSession() as session:
        try:
            async with session.post(
                "https://www.googleapis.com/oauth2/v4/token",
                data={
                    "client_id": request.app.config.AUTH["GOOGLE_CLIENT_ID"],
                    "client_secret": request.app.config.AUTH["GOOGLE_CLIENT_SECRET"],
                    "redirect_uri": f"{request.app.config.BASE_URL}{request.app.url_for('auth.google_callback')}",
                    "grant_type": "authorization_code",
                    "code": request.args.get("code")
                }
            ) as response:
                data = await response.json()
                token = data["access_token"]
        except Exception as _:
            raise BadRequest

        async with session.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            data = await response.json()
            return json(data)


@Auth.get("/callback/naver")
async def naver_callback(request: Request):
    async with ClientSession() as session:
        try:
            async with session.post(
                "https://nid.naver.com/oauth2.0/token",
                data={
                    "client_id": request.app.config.AUTH["NAVER_CLIENT_ID"],
                    "client_secret": request.app.config.AUTH["NAVER_CLIENT_SECRET"],
                    "grant_type": "authorization_code",
                    "code": request.args.get("code"),
                    "state": ""
                }
            ) as response:
                data = await response.json()
                token = data["access_token"]
        except Exception as _:
            raise BadRequest

        async with session.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            data = await response.json()
            return json(data["response"])
