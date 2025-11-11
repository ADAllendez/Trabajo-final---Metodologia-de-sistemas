from pydantic import BaseModel

# --- ESPECIALIDAD ---
class EspecialidadBase(BaseModel):
    nombre: str

class EspecialidadOut(EspecialidadBase):
    id_especialidad: int
    class Config:
        from_attributes = True


# --- MEDICO ---
class MedicoBase(BaseModel):
    nombre: str
    apellido: str
    matricula: str
    id_especialidad: int | None = None

class MedicoIn(MedicoBase):
    pass

class MedicoOut(MedicoBase):
    id_medico: int
    especialidad: EspecialidadOut | None = None

    class Config:
        from_attributes = True
