from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers.notes import router as notes_router
from backend.app.routers.auth import router as auth_router

app = FastAPI(title="Note App Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc cấu hình domain frontend cụ thể cho bảo mật hơn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router)
app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    paths = [r.path for r in app.routes if isinstance(r.path, str)]
    filtered = [p for p in paths if not p.startswith("/openapi") and not p.startswith("/docs") and not p.startswith("/redoc")]
    return {"service": "Note App Backend", "endpoints": sorted(set(filtered))}