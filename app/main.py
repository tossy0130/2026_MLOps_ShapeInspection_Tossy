from fastapi.responses import HTMLResponse

from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.inspect import router as inspect_router
from app.routers.model import router as model_router

from app.settings import settings

app = FastAPI(title=settings.app_name, version="0.1.0")

app.include_router(health_router)
app.include_router(inspect_router)
app.include_router(model_router)

@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
    <html>
      <head><title>Negi Inspection FastAPI</title></head>
      <body style="font-family: Arial; padding: 24px;">
        <h1>Negi Inspection FastAPI</h1>
        <ul>
          <li><a href="/docs">Swagger UI</a></li>
          <li><a href="/health">Health</a></li>
          <li><a href="/model/current">Current Model</a></li>
        </ul>
      </body>
    </html>
    """