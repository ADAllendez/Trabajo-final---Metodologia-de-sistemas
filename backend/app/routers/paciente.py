from email import message
from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_db
from app.models.paciente import Paciente
from typing import List
from app.schemas.paciente import PacienteIn, PacienteOut

router = APIRouter(tags=["Pacientes"])

@router.get("/", response_model=List[PacienteOut])
async def listar_pacientes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Paciente))
    pacientes = result.scalars().all()
    return pacientes


#obtenemos los pacientes por su ID
@router.get ("/{id_paciente}",response_model=PacienteOut)
async def obtener_paciente (id_paciente: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Paciente).where(Paciente.id_paciente == id_paciente))
    paciente = result.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code= 404, detail= "Paciente no encontrado")
    return paciente

#creamos un paciente
@router.post("/",response_model=PacienteIn)
async def crear_paciente (datos: PacienteIn, db: AsyncSession = Depends(get_db)):
    nuevo_paciente = Paciente(**datos.dict())
    db.add(nuevo_paciente)
    await db.commit()
    await db.refresh(nuevo_paciente)
    return nuevo_paciente


#actulizamos al paciente
@router.put("/{id_paciente}",response_model=PacienteOut)
async def actulizar_paciente (id_paciente: int , datos:PacienteIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Paciente).where(Paciente.id_paciente == id_paciente))
    paciente = result.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code=404,detail=("Paciente no encontrado"))
    for key, value in datos.dict().items():
        setattr (paciente,key,value)
    await db.commit()
    await db.refresh(paciente)
    return paciente
   

#eliminamos al paciente 
@router.delete ("/{id_paciente}")
async def eliminar_paciente (id_paciente: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Paciente).where(Paciente.id_paciente == id_paciente))
    paciente = result.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    await db.delete(paciente)
    await db.commit()
    return {"message:""Paciente eliminado correctamente"}
  



