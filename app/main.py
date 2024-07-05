from typing import Union

from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from mimetypes import guess_type
from os.path import isfile
import markdown

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))),
          name="static")

app.add_middleware(GZipMiddleware, minimum_size=1000)

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@app.get("/")
def home(request: Request):
    filename = str(Path(BASE_DIR, 'static')) + "/md/home.md" 

    with open(filename) as f:
        content = f.read()

    return templates.TemplateResponse(
        request=request, name="layout.html", context={
            "path": "home",  
            "name": "@redentor_dev",
            "content": markdown.markdown(content),
        }
    )

@app.get("/{slug}")
def pages(slug: str, request: Request):
    filename = str(Path(BASE_DIR, 'static')) + "/md" 
    if (request.url.path == "/"):
        filename = filename + "/home.md"
    else:
        filename = filename + request.url.path + ".md"

    print(filename)

    if not isfile(filename):
        return templates.TemplateResponse(
            status_code=404,
            request=request,
            name="layout.html",
            context={
                "path": "404",
                "name": "@redentor_dev",
                "content": markdown.markdown("# 404 Page" +
                    "\n" +
                    "There's nothing here. You're lost... [Go Back](/)")
            }
        )

    with open(filename) as f:
        content = f.read()

    return templates.TemplateResponse(
        request=request, name="layout.html", context={
            "path": slug,  
            "name": "@redentor_dev",
            "content": markdown.markdown(content),
        }
    )
