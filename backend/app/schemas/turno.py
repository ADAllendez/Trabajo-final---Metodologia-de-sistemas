from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .medico import MedicoOut
from .paciente import PacienteOut

class TurnoIn(BaseModel):
    id_paciente: int
    id_medico: Optional[int] = None
    fecha_turno: datetime
    estado: str

class TurnoOut(TurnoIn):
    id_turno: int
    fecha_turno: datetime
    estado: str
    paciente: PacienteOut
    medico: Optional[MedicoOut] = None

    class Config:
        from_attributes = True