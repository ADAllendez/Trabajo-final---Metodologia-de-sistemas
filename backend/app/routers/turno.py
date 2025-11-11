from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_db
from app.models.turno import Turno
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.schemas.turno import TurnoIn, TurnoOut
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from sqlalchemy.orm import selectinload
import tempfile

router = APIRouter(tags=["Turnos"])

#listar todos los turnos
@router.get("/", response_model=list[TurnoOut])
async def list_turnos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Turno)
        .options(
            selectinload(Turno.paciente),#esta linea es para cargar las relaciones en una consulta separada, antes de devolver los resultados
            selectinload(Turno.medico).selectinload(Medico.especialidad)
        )
    )
    turnos = result.scalars().all()
    return turnos

#obtener turno por ID
@router.get("/{id_turno}",response_model=TurnoOut)
async def obtener_turno(id_turno :int, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Turno).where(Turno.id_turno == id_turno))
    turno = result.scalar_one_or_none()
    if not turno:
        raise HTTPException(status_code=404,detail="Turno no encontrado")
    return turno

#crear turno
@router.post("/",response_model=TurnoOut)
async def crear_turno(datos: TurnoIn,db: AsyncSession = Depends(get_db)):
    
    # Verificar paciente
    paciente_res =  await db.execute(select(Paciente).where(Paciente.id_paciente == datos.id_paciente))
    paciente = paciente_res.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code=400,detail="Paciente no encontrado")
    
    # Verificar médico (si aplica)
    if datos.id_medico:
        medico_res = await db.execute(select(Medico).where(Medico.id_medico == datos.id_medico))
        medico = medico_res.scalar_one_or_none()
        if not medico:
            raise HTTPException(status_code=400,detail="Medico no encontrado")

    #Verificar si hay conflicto en el horario elegido
    conflicto_res = await db.execute(select(Turno).where(Turno.id_medico == datos.id_medico,
                                                         Turno.fecha_turno == datos.fecha_turno,
                                                         Turno.estado != "Cancelado"))
    conflicto = conflicto_res.scalar_one_or_none()
    if conflicto:
        raise HTTPException(status_code=404,detail="El medico ya tiene turno a esa hora")   

    nuevo_turno = Turno(**datos.dict())
    db.add(nuevo_turno)
    await db.commit()
    await db.refresh(nuevo_turno)
    return nuevo_turno 

#actulizar turno
@router.put("/{id_turno}")
async def actualizar_turno(id_turno : int,datos: TurnoIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Turno).where(Turno.id_turno == id_turno))
    turno = result.scalar_one_or_none()
    if not turno:
        raise HTTPException(status_code=404,detail="Turno no encontrado")
    
    for key, value in datos.dict().items():
        setattr(turno,key,value)
    await db.commit()
    await db.refresh(turno)
    return turno

#eliminar turno
@router.delete("/{id_turno}")
async def eliminar_turno(id_turno:int, db:AsyncSession = Depends (get_db)):
    result = await db.execute(select(Turno).where(Turno.id_turno == id_turno))
    turno = result.scalar_one_or_none()
    if not turno:
        raise HTTPException(status_code=404,detail="Turno no encontrado")
    await db.delete(turno)
    await db.commit()
    return {"message": "Turno eliminado correctamente"}

#actualizar estado del turno
@router.put("/{id_turno}/estado")
async def actualizar_estado_turno(id_turno: int, nuevo_estado: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Turno).where(Turno.id_turno == id_turno))
    turno = result.scalar_one_or_none()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    # Validar el nuevo estado
    if nuevo_estado not in ["Programado", "Atendido", "Cancelado"]:
        raise HTTPException(status_code=400, detail="Estado no válido")

    turno.estado = nuevo_estado
    await db.commit()
    await db.refresh(turno)

    return {"message": f"Turno actualizado a {nuevo_estado}", "estado": turno.estado}


#generar un comprobante del turno
@router.get("/{id_turno}/reporte")
async def generar_reporte_turno(id_turno: int, formato: str = "pdf", db: AsyncSession = Depends(get_db)):
    # Buscar turno
    result = await db.execute(
        select(Turno, Paciente, Medico)
        .join(Paciente, Turno.id_paciente == Paciente.id_paciente)
        .join(Medico, Turno.id_medico == Medico.id_medico, isouter=True)
        .where(Turno.id_turno == id_turno)
    )
    data = result.first()
    if not data:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    turno, paciente, medico = data

    # PDF
    if formato.lower() == "pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            c = canvas.Canvas(tmp.name, pagesize=letter)
            c.setTitle("Comprobante de Turno")

            c.drawString(100, 750, f"Comprobante de Turno #{turno.id_turno}")
            c.drawString(100, 720, f"Paciente: {paciente.nombre} {paciente.apellido} (DNI: {paciente.dni})")
            c.drawString(100, 690, f"Médico: {medico.nombre} {medico.apellido}" if medico else "Médico: Sin asignar")
            c.drawString(100, 660, f"Fecha: {turno.fecha_turno.strftime('%d/%m/%Y %H:%M')}")
            c.drawString(100, 630, f"Estado: {turno.estado}")
            c.drawString(100, 590, "Este comprobante es solo de uso interno del sistema de la clínica.")
            
            c.showPage()
            c.save()
            return FileResponse(tmp.name, filename=f"turno_{turno.id_turno}.pdf", media_type="application/pdf")

    # Excel
    elif formato.lower() == "xlsx":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            wb = Workbook()
            ws = wb.active
            ws.title = "Comprobante Turno"

            ws.append(["ID Turno", "Paciente", "Médico", "Fecha", "Estado"])
            ws.append([
                turno.id_turno,
                f"{paciente.nombre} {paciente.apellido}",
                medico.nombre, medico.apellido if medico else "Sin asignar",
                turno.fecha_turno.strftime("%d/%m/%Y %H:%M"),
                turno.estado
            ])

            wb.save(tmp.name)
            return FileResponse(tmp.name, filename=f"turno_{turno.id_turno}.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    else:
        raise HTTPException(status_code=400, detail="Formato no soportado")
