from pydantic import BaseModel

class EspecialidadBase(BaseModel):
    nombre: str

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadOut(EspecialidadBase):
    id_especialidad: int

    class Config:
        from_attributes = True
