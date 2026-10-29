from fastapi import FastAPI
from app.api.v1.endpoints import router as api_v1_router

app = FastAPI(
    title="CPF Validador API",
    description="API para validação, enriquecimento geográfico e análise de risco de CPF.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Registra as rotas da v1
app.include_router(api_v1_router, prefix="/api/v1", tags=["CPF Validation"])

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "service": "CPF Validador API", "version": "1.0.0"}