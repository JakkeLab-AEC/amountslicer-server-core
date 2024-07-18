import os.path
import shutil
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.ifc_utils.ifc_file_utils import IfcUtilsFile

from src.config import SERVER_PORT, SERVER_HOST, ENVIRONMENT

from dotenv import load_dotenv

#Server Setting
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIRECTORY = "temp_files"
ALLOWED_EXTENSIONS = {".ifc"}

#Server file upload functions
def is_allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS

def get_unique_filename(filename: str) -> str:
    unique_id = uuid.uuid4().hex
    _, ext = os.path.splitext(filename)
    unique_filename = f"{unique_id}{ext}"
    return unique_filename

def clear_temp_files():
    if os.path.exists(UPLOAD_DIRECTORY):
        shutil.rmtree(UPLOAD_DIRECTORY)
        print(f"{UPLOAD_DIRECTORY} directory cleared.")

@app.get("/connectionTest")
def connection_test():
    content = {
        "Connection Status" : "Success"
    }
    return JSONResponse(content=content)

@app.get("/")
def home_message():
    content = """
    <body>
        <form action="/uploadfile" enctype="multipart/form-data" method="post">
            <input name="file" type="file" accept=".ifc">
            <input type="submit">
        </form>
    </body>
    """

    return HTMLResponse(content=content)

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    #Extension Check
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file extension. Only .ifc files are allowed.")

    #Make dir if not exist
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    #Set unique filename
    unique_filename = get_unique_filename(file.filename)
    file_location = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ifc_file = IfcUtilsFile.load(file_location)
    if ifc_file:
        categories_json = IfcUtilsFile.seperate_by_category(ifc_file, to_json=True)
        return JSONResponse(content=categories_json)
    else:
        return {"error": "Failed to load IFC file"}

@app.post("/getgeometry")
async def get_geometry(file: UploadFile = File(...)):
    request_body = await file.read()
    request_body_size = len(request_body)
    file.file.seek(0)

    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file extension. Only .ifc files are allowed.")

    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    unique_filename = get_unique_filename(file.filename)
    file_location = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ifc_file = IfcUtilsFile.load(file_location)
    if ifc_file:
        geometry_data = IfcUtilsFile.get_geometry(ifc_file)
        response = JSONResponse(content=geometry_data)
        response_body_size = len(response.body)
    else:
        response = JSONResponse(content={"error": "Failed to load IFC file"})
        response_body_size = len(response.body)

    # 요청 및 응답 크기 로깅
    logging.info(f"Request size: {request_body_size / 1024**2 : .3f} MB")
    logging.info(f"Response size: {response_body_size / 1024**2: .3f} MB")

    return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Start

    yield

    #Shutdown
    clear_temp_files()

#Server On
if __name__ == "__main__":
    import uvicorn
    if ENVIRONMENT == "dev":
        uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
    else:
        uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT)