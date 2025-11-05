import os
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Body
from fastapi.concurrency import run_in_threadpool
from pydantic import SecretStr
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv; 
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from my_agent.utils.workflow import graph
from my_agent.utils.llm_store import set_llm
from langchain_core.tracers.context import tracing_v2_enabled
from langchain_core.messages import AIMessage
import json

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Firebase Admin only once
    try:
        if not firebase_admin._apps:
            cred_path = os.environ.get("FIREBASE_CREDENTIALS_FILE")
            db_url = os.environ.get("FIREBASE_DB_URL")
            print(cred_path, db_url)

            if not cred_path or not db_url:
                raise RuntimeError("FIREBASE_CREDENTIALS_FILE and FIREBASE_DB_URL must be set")

            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {"databaseURL": db_url})
    except Exception as e:
        # Surface init errors clearly at startup
        raise RuntimeError(f"Failed to initialize Firebase: {e}") from e
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
             api_key=SecretStr(os.environ.get("api_key", "")))
        set_llm(llm)
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


@app.post("/run")
async def run_supervisor(payload: dict = Body(...)) -> Any:
    try:
        # Build minimal initial state for the graph
        input_text = payload.get("input", "Start")
        state = {
            "messages": [HumanMessage(content=input_text)],
            "productId": payload.get("productId", ""),
            "reason": payload.get("reason", ""),
            "reporterId": payload.get("reporterId", ""),
            "orgId": payload.get("orgId", ""),
            "purchaseDate": payload.get("purchaseDate", ""),
            "token": payload.get("token", ""),
        }

        with tracing_v2_enabled(project_name=os.environ.get("LANGCHAIN_PROJECT", "report-agent")):
            result = await run_in_threadpool(
                graph.invoke,
                state,
                config={
                    "run_name": "ReportAgentGraph",
                    "metadata": {
                        "route": "/run",
                        "orgId": state.get("orgId", ""),
                        "productId": state.get("productId", ""),
                    },
                    "tags": ["fastapi", "report-agent"],
                },
            )

        # return only the final AI message content, parsed if it’s JSON
        msgs = result.get("messages", [])
        answer = next(
            (m.content for m in reversed(msgs) if isinstance(m, AIMessage)),
            msgs[-1].content if msgs else ""
        )
        try:
            return json.loads(answer)
        except Exception:
            return {"result": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run agent: {e}")