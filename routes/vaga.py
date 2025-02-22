from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Vaga
from odmantic import ObjectId

router = APIRouter(
    prefix="/vagas",
    tags=["Vagas"],
)

engine = get_engine()

@router.get("/", response_model=list[Vaga])
async def get_all_vagas() -> list[Vaga]:
    vagas = await engine.find(Vaga)
    return vagas

@router.get("/{vaga_id}", response_model=Vaga)
async def get_vaga(vaga_id: str) -> Vaga:
    vaga = await engine.find_one(Vaga, Vaga.id == ObjectId(vaga_id))
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga not found")
    return vaga

@router.post("/", response_model=Vaga)
async def create_vaga(vaga: Vaga) -> Vaga:
    await engine.save(vaga)
    return vaga

@router.put("/{vaga_id}", response_model=Vaga)
async def update_vaga(vaga_id: str, vaga_data: dict) -> Vaga:
    vaga = await engine.find_one(Vaga, Vaga.id == ObjectId(vaga_id))
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga not found")
    for key, value in vaga_data.items():
        setattr(vaga, key, value)
    await engine.save(vaga)
    return vaga

@router.delete("/{vaga_id}")
async def delete_vaga(vaga_id: str) -> dict:
    vaga = await engine.find_one(Vaga, Vaga.id == ObjectId(vaga_id))
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga not found")
    await engine.delete(vaga)
    return {"message": "Vaga deleted"}