from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Inscricao, Vaga, Voluntario
from odmantic import ObjectId

router = APIRouter(
    prefix="/inscricoes",
    tags=["Inscricoes"],
)

engine = get_engine()


@router.post("/inscricao/", response_model=Inscricao)
async def criar_inscricao(inscricao: Inscricao) -> Inscricao:
    await engine.save(inscricao)
    return inscricao

@router.get("/", response_model=list[Inscricao])
async def listar_todas_inscricoes() -> list[Inscricao]:
    inscricoes = await engine.find(Inscricao)
    return inscricoes

@router.get("/{inscricao_id}", response_model=Inscricao)
async def lista_inscricao_por_id(inscricao_id: str) -> Inscricao:
    inscricao = await engine.find_one(Inscricao, Inscricao.id == ObjectId(inscricao_id))
    if not inscricao:
        raise HTTPException(status_code=404, detail="Inscricao not found")
    return inscricao

@router.put("/{inscricao_id}", response_model=Inscricao)
async def atualizar_inscricao(inscricao_id: str, inscricao_data: dict) -> Inscricao:
    inscricao = await engine.find_one(Inscricao, Inscricao.id == ObjectId(inscricao_id))
    if not inscricao:
        raise HTTPException(status_code=404, detail="Inscricao not found")
    for key, value in inscricao_data.items():
        setattr(inscricao, key, value)
    await engine.save(inscricao)
    return inscricao

@router.delete("/{inscricao_id}")
async def deletar_inscricao(inscricao_id: str) -> dict:
    inscricao = await engine.find_one(Inscricao, Inscricao.id == ObjectId(inscricao_id))
    if not inscricao:
        raise HTTPException(status_code=404, detail="Inscricao not found")
    await engine.delete(inscricao)
    return {"message": "Inscricao deleted"}