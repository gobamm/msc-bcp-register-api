from typing import Optional
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from v2.endpoint import api_router

load_dotenv()
app = FastAPI(
    title="BCP APIs",
    docs_url="/api/v2/docs",
    openapi_url="/api/v2/docs/openapi.json",
    description="API for Common Service BCP"+" register",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api")

# Set all CORS enabled origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
