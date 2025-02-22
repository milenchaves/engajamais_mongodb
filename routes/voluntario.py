from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Voluntario
from odmantic import ObjectId

router = APIRouter(
    prefix="/voluntarios",
    tags=["Voluntarios"],
)

engine = get_engine()

@router.get("/", response_model=list[Voluntario])
async def get_all_voluntarios() -> list[Voluntario]:
    voluntarios = await engine.find(Voluntario)
    return voluntarios

@router.get("/{voluntario_id}", response_model=Voluntario)
async def get_voluntario(voluntario_id: str) -> Voluntario:
    voluntario = await engine.find_one(Voluntario, Voluntario.id == ObjectId(voluntario_id))
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario not found")
    return voluntario

@router.post("/", response_model=Voluntario)
async def create_voluntario(voluntario: Voluntario) -> Voluntario:
    await engine.save(voluntario)
    return voluntario

@router.put("/{voluntario_id}", response_model=Voluntario)
async def update_voluntario(voluntario_id: str, voluntario_data: dict) -> Voluntario:
    voluntario = await engine.find_one(Voluntario, Voluntario.id == ObjectId(voluntario_id))
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario not found")
    for key, value in voluntario_data.items():
        setattr(voluntario, key, value)
    await engine.save(voluntario)
    return voluntario

@router.delete("/{voluntario_id}")
async def delete_voluntario(voluntario_id: str) -> dict:
    voluntario = await engine.find_one(Voluntario, Voluntario.id == ObjectId(voluntario_id))
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario not found")
    await engine.delete(voluntario)
    return {"message": "Voluntario deleted"}