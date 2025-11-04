import os
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import SecretStr
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv; 
from langchain_openai import ChatOpenAI

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Firebase Admin only once
    try:
        if not firebase_admin._apps:
            cred_path = os.environ.get("FIREBASE_CREDENTIALS_FILE")
            db_url = os.environ.get("FIREBASE_DB_URL")

            if not cred_path or not db_url:
                raise RuntimeError("FIREBASE_CREDENTIALS_FILE and FIREBASE_DB_URL must be set")

            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {"databaseURL": db_url})
    except Exception as e:
        # Surface init errors clearly at startup
        raise RuntimeError(f"Failed to initialize Firebase: {e}") from e
    try:
        llm = ChatOpenAI(
            model="gpt-5-nano",
             api_key=SecretStr(os.environ.get("api_key", "")))
        app.state.llm = llm  # store in app.state for access elsewhere
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {e}") from e

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/products")
async def read_movements() -> Any:
    try:
        ref = db.reference("api/products")
        data = await run_in_threadpool(ref.get)
        return data if data is not None else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read movements: {e}")


@app.get("/movements/{subpath:path}")
async def read_movements_subpath(subpath: str) -> Any:
    try:
        ref = db.reference(f"api/movements/{subpath}")
        data = await run_in_threadpool(ref.get)
        return data if data is not None else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read movements/{subpath}: {e}")