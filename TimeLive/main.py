from sanic import Sanic, Request
from sanic.response import redirect

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from TimeLive.config import TomlConfig

from TimeLive.api.auth import Auth

from contextvars import ContextVar
from textwrap import dedent


toml_config = TomlConfig(path="TimeLive/config.toml")
app = Sanic("TimeLive", config=toml_config)

app.blueprint(Auth)

app.ext.openapi.describe(
    "TimeLive",
    version="1.0.0",
    description=dedent(
        """
        To be written
        """
    )
)

database = create_async_engine(app.config.DATABASE["URL"])
_base_model_session_ctx = ContextVar("session")


@app.middleware("request")
async def inject_session(request: Request):
    request.ctx.session = sessionmaker(database, AsyncSession, expire_on_commit=False)()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


@app.get("/")
async def main(request):
    return redirect("/docs")
