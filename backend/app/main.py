from app.routers import paciente, especialidad,medico, turno
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import engine,Base
from app.routers import paciente
from app.routers import consultas
from app.routers import medico
from app.routers import turno
from app.routers import especialidad

#Creamos la app FastAPI

app = FastAPI(
    title= "Clinica Medica",
    description= "Aplicacion para la gestion de turno de un centro medico",
    version="1.0.0"
)


#configuracion de CORS

origins= [
    "http://localhost:3000", #Front local
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers = ["*"]
)

#crear las tablas si es que no existen'

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


#incluir los routers

app.include_router(paciente.router, prefix="/pacientes", tags=["Pacientes"])
app.include_router(especialidad.router, prefix="/especialidades", tags=["Especialidades"])
app.include_router(medico.router, prefix="/medicos", tags=["Medicos"])
app.include_router(turno.router, prefix="/turnos", tags=["Turnos"])
app.include_router(consultas.router)

#Iniciamos la app 
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de la Clínica"}