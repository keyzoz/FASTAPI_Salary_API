from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from api.routers.user_router import user_router
from api.routers.login_router import login_router


app = FastAPI(title="shift_task")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["tags"])
main_api_router.include_router(login_router, prefix="/login", tags=["tags"])

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8003)