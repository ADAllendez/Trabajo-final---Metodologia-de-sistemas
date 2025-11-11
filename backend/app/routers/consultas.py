from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.config.database import get_db


router = APIRouter(prefix="/consultas", tags=["Consultas"])


# CONSULTA 1: JOIN múltiple (turnos con paciente, médico y especialidad)

@router.get("/turnos-detalle")
async def turnos_detalle(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT 
            t.id_turno,
            p.nombre AS nombre_paciente,
            p.apellido AS apellido_paciente,
            m.nombre AS nombre_medico,
            m.apellido AS apellido_medico,
            e.nombre AS especialidad,
            t.fecha_y_hora,
            t.estado
        FROM turno t
        INNER JOIN paciente p ON t.id_paciente = p.id_paciente
        LEFT JOIN medico m ON t.id_medico = m.id_medico
        LEFT JOIN especialidad e ON m.id_especialidad = e.id_especialidad
        ORDER BY t.fecha_y_hora DESC
    """)
    result = await db.execute(query)
    return result.mappings().all()


# CONSULTA 2: SUBQUERY (pacientes con más de un turno)

@router.get("/pacientes-recurrentes")
async def pacientes_recurrentes(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT 
            id_paciente,
            nombre,
            apellido,
            dni,
            correo
        FROM paciente
        WHERE id_paciente IN (
            SELECT id_paciente
            FROM turno
            GROUP BY id_paciente
            HAVING COUNT(id_turno) > 1
        )
    """)
    result = await db.execute(query)
    return result.mappings().all()



# CONSULTA 3: GROUP BY (cantidad de turnos por médico)

@router.get("/turnos-por-medico")
async def turnos_por_medico(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT 
            m.id_medico,
            CONCAT(m.nombre, ' ', m.apellido) AS medico,
            e.nombre AS especialidad,
            COUNT(t.id_turno) AS total_turnos
        FROM medico m
        LEFT JOIN turno t ON m.id_medico = t.id_medico
        LEFT JOIN especialidad e ON m.id_especialidad = e.id_especialidad
        GROUP BY m.id_medico, e.nombre
        ORDER BY total_turnos DESC
    """)
    result = await db.execute(query)
    return result.mappings().all()
