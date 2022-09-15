from config import APP_HOST, APP_PORT, TEMP_DIR
from endpoints.api import router as api_router
from fastapi import FastAPI
import uvicorn
from pathlib import Path

tmp_dir = Path(TEMP_DIR)
tmp_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(docs_url='/api/docs',
              openapi_url='/api/openapi.json')
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
