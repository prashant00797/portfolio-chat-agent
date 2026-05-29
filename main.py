from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.agent.graph import create_agent_graph
from app.api.routes import chat_router
from app.core.limiter import limiter
from app.services.supabase_service import sc
from app.core.config import get_settings

config = get_settings()

@asynccontextmanager
async def lifespan(app:FastAPI):
    graph = create_agent_graph() # initialize graph once at server startup
    app.state.graph = graph
    yield


app = FastAPI(
    title="Portfolio Assistant API",
    description="Agentic AI backend for portfolio chatbot",
    version="1.0.0",
    lifespan=lifespan,
    )
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler) # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://prashantnathv2.netlify.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router.router,prefix="/api")


@app.api_route("/health",methods=["GET","HEAD"])
def health():
    return {"status": "ok"}


@app.api_route("/health/db",methods=["GET","HEAD"])
def health_db():
    try:
        sc.table("users").select("id").eq("id",config.DUMMY_HEALTH_CHECK_BOT_ID).execute()
        return {"db": "ok"}
    except Exception:
        return JSONResponse(status_code=503,content={"db": "unreachable"})