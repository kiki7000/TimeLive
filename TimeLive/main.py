from sanic import Sanic
from sanic.response import text, redirect

from TimeLive.config import TomlConfig

from TimeLive.api.auth import Auth


toml_config = TomlConfig(path="TimeLive/config.toml")
app = Sanic("TimeLive", config=toml_config)

app.blueprint(Auth)


@app.get("/")
async def main(request):
    return redirect("/docs")


@app.get("/test")
async def test(request):
    return text(app.config.OWNER["OWNER_NAME"])
