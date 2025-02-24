from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Organizacao
from odmantic import ObjectId

router = APIRouter(
    prefix="/organizacoes",
    tags=["Organizacoes"],
)

engine = get_engine()


@router.post("/", response_model=Organizacao)
async def criar_organizacao(organizacao: Organizacao) -> Organizacao:
    await engine.save(organizacao)
    return organizacao

@router.get("/", response_model=list[Organizacao])
async def listar_todas_organizacoes() -> list[Organizacao]:
    organizacoes = await engine.find(Organizacao)
    return organizacoes

@router.get("/{organizacao_id}", response_model=Organizacao)
async def listar_organizacao_por_id(organizacao_id: str) -> Organizacao:
    organizacao = await engine.find_one(Organizacao, Organizacao.id == ObjectId(organizacao_id))
    if not organizacao:
        raise HTTPException(status_code=404, detail="Organizacao not found")
    return organizacao

@router.put("/{organizacao_id}", response_model=Organizacao)
async def atualizar_organizacao(organizacao_id: str, organizacao_data: dict) -> Organizacao:
    organizacao = await engine.find_one(Organizacao, Organizacao.id == ObjectId(organizacao_id))
    if not organizacao:
        raise HTTPException(status_code=404, detail="Organizacao not found")
    for key, value in organizacao_data.items():
        setattr(organizacao, key, value)
    await engine.save(organizacao)
    return organizacao

@router.delete("/{organizacao_id}")
async def deletar_organizacao(organizacao_id: str) -> dict:
    organizacao = await engine.find_one(Organizacao, Organizacao.id == ObjectId(organizacao_id))
    if not organizacao:
        raise HTTPException(status_code=404, detail="Organizacao not found")
    await engine.delete(organizacao)
    return {"message": "Organizacao deleted"}