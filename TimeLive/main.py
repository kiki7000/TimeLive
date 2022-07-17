from sanic import Sanic
from sanic.response import text

from TimeLive.config import TomlConfig


toml_config = TomlConfig(path="TimeLive/config.toml")
app = Sanic("TimeLive", config=toml_config)


@app.get("/")
async def hello_world(request):
    return text("Hello, World!")


@app.get("/test")
async def test(request):
    return text(app.config.OWNER["OWNER_NAME"])
