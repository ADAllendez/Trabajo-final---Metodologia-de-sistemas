from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.config.database import engine, Base, get_db
from app.routers import paciente, especialidad, medico, turno, consultas

app = FastAPI(
    title="Clinica Medica",
    version="1.0.0",
    redirect_slashes=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://localhost:5173",
        "https://127.0.0.1:5173",
        "https://localhost:3000",
        "https://127.0.0.1:3000",
        "https://trabajo-final-metodologia-de-sistem.vercel.app"

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚫 NO crear tablas automáticamente en Railway
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# 📌 ROUTERS
app.include_router(paciente.router, prefix="/pacientes", tags=["Pacientes"])
app.include_router(especialidad.router, prefix="/especialidades", tags=["Especialidades"])
app.include_router(medico.router, prefix="/medicos", tags=["Medicos"])
app.include_router(turno.router, prefix="/turnos", tags=["Turnos"])
app.include_router(consultas.router)

# 🧪 TEST DE CONEXIÓN A MYSQL
@app.get("/db-test")
async def db_test(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db": result.scalar()}

@app.get("/")
async def root():
    return {"message": "API Clínica conectada a MySQL correctamente"}
