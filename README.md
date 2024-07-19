# AmoutSlicer - IFC Operation Server
The FastAPI based python app for handling IFC file
(Under construction)

Used Library : IfcOpenShell

---

Actually, I've created this server for local use first. <br/>
When I first used Jupyter Notebook before, I've realized that it's a kind of Client-Server based application.<br/>
The local server of Jupyter Notebook is running on the local, and the user can access services via browser.<br/>
After that, I've designed this server app as parsing server of IFC File, using IfcOpenShell.

---

### How to run
1. Before run server, please make your .env file on the root direct.
   This app uses dotenv.

```python
#src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
SERVER_HOST = os.getenv("SERVER_HOST")
```

```python
#src/main.py

...
#Server On
if __name__ == "__main__":
    import uvicorn
    if ENVIRONMENT == "dev":
        uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
    else:
        uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT)
```


```dotenv
#.env
ENVIRONMENT=dev #if you set this as dev, you can see the log on the python console.
SERVER_PORT=<YOUR PORT>
SERVER_HOST=<YOUR HOST>
```

2. Please add your client host to pass CORS.
```python
#src/main.py
#Server Setting
app = FastAPI()

origins = [
    #Add your host here
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```
3. Run src/main.py

---

### Current parsable element:

- Slab (IfcSlab)

<br/>Parsable elements will be updated gradually.

---

### Client App
FrontEnd (Next.js + React) repository : https://github.com/JakkeLab-AEC/amountslicer-fe/tree/main
