import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import httpx

from router import realtor_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserAgentMiddleware:
    async def __call__(self, request: Request, call_next):
        user_agent = request.headers.get('user-agent')
        if not user_agent:
            raise HTTPException(status_code=403, detail="Invalid Headers")
        response = await call_next(request)
        return response


app.middleware("http")(UserAgentMiddleware())


@app.get("/")
async def main():
    return {"message": "Welcome to the PropertyPulse. visit /docs for endpoints"}


@app.get("/check")
async def check_internet_connection():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://www.google.com", timeout=5)
            if response.status_code == 200:
                return {"message": "Internet connection is active."}
            else:
                return {"message": "Unable to establish internet connection."}
    except Exception as e:
        return {"message": f"Error: {e}"}


app.include_router(realtor_router, prefix="/realtor", tags=["Realtor"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)