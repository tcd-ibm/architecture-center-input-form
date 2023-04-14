from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import api


# Create FastAPI app and add CORS middleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Total-Pages"]
)

templates = Jinja2Templates(directory="dist")

app.mount("/assets", StaticFiles(directory="dist/assets"), name="static")

# Add API routes
app.include_router(api.router)

@app.get("/{rest_of_path:path}")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app",
                host="localhost",
                port=5297,
                reload=False,
                log_level="info")