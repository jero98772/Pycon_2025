import jpype
import jpype.imports
from jpype.types import JString
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

# Define the path to your Clojure uberjar
JAR_PATH = "target/uberjar/clojure_hackasembler_web-0.1.0-SNAPSHOT-standalone.jar"

# Initialize JVM globally, so it's only started once
jpype.startJVM(classpath=[JAR_PATH])

# Import Clojure classes and functions
asembler = jpype.JClass("clojure_hackasembler_web.core")
clojure = jpype.JPackage("clojure")
assemble_func = clojure.java.api.Clojure.var("clojure_hackasembler_web.core", "assemble")

app = FastAPI()

# Configure Jinja2Templates to look for templates in the "templates" directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/assemble/")
async def assemble_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    result = assemble_func.invoke(JString(code))
    return {"result": str(result)}
