from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import engine, Base
from app.routers import paciente, especialidad, medico, turno
from sqlalchemy.ext.asyncio import AsyncEngine

app = FastAPI(
    title="Clinica Medica",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#@app.on_event("startup")
#async def startup():
    #async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.create_all)

app.include_router(paciente.router, prefix="/pacientes", tags=["Pacientes"])
app.include_router(especialidad.router, prefix="/especialidades", tags=["Especialidades"])
app.include_router(medico.router, prefix="/medicos", tags=["Medicos"])
app.include_router(turno.router, prefix="/turnos", tags=["Turnos"])

@app.get("/")
async def root():
    return {"message": "API Clínica conectada a MySQL correctamente"}
