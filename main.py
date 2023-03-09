import time
import uvicorn
import logging
# import numpy as np
from fastapi import (
    FastAPI,
    status,
    Depends,
    Header,
    HTTPException,
)
from fastapi.responses import JSONResponse

LOG_FORMAT = "%(asctime)s [%(name)s:%(lineno)s] [%(levelname)s]: %(message)s"
logging.basicConfig(level="DEBUG", format=LOG_FORMAT)
app = FastAPI()


@app.get("/")
async def heatlhcheck() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ok"},
    )


def make_response_data() -> JSONResponse:
    # points: np.ndarray = np.random.rand(100, 2)
    points: float = time.monotonic()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "ok",
            "data": points,
        },
    )


@app.get("/data_unsafe")
async def data_unsafe():
    return make_response_data()


async def verify_token(x_token: str = Header()) -> None:
    if x_token != "secret-token":
        raise HTTPException(status_code=403, detail="X-Token header invalid")


@app.get("/data_with_auth", dependencies=[Depends(verify_token)])
async def data_with_auth():
    return make_response_data()


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8088,
                log_config=None,
                log_level="debug",
                access_log=False,
                workers=1)
