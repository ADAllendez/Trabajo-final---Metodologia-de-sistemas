from pydantic import BaseModel
from typing import Optional

class PacienteIn(BaseModel):
    nombre: str
    apellido: str
    dni: Optional[str] = None
    correo: Optional[str] = None

class PacienteOut(PacienteIn):
    id_paciente: int
    
class Config:
    from_attributes = True