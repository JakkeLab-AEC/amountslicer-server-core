from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
app = FastAPI()
@app.get("/")
def home_message():
    content = """
    <body>
        <form action="/uploadfile/" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit">
        </form>
    </body>
    """
    return HTMLResponse(content=content)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    # Here you can process the file_content or save it to disk
    # For demonstration, we'll just return the filename and content size
    return {"filename": file.filename, "content_size": len(file_content)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8800)