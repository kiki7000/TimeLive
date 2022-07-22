from sanic import Sanic
from sanic.response import text, redirect

from TimeLive.config import TomlConfig

from TimeLive.api.auth import Auth

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


@app.get("/")
async def main(request):
    return redirect("/docs")