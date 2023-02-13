from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import api


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


app.include_router(api.router, prefix="/api/v1")


@app.get("/")
async def index():
    return RedirectResponse(url="/docs", status_code=302)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app",
                host="localhost",
                port=5297,
                reload=False,
                debug=False,
                log_level="info")
