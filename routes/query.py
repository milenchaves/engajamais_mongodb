from odmantic import AIOEngine
from fastapi import APIRouter, HTTPException, Query, Depends
from bson import ObjectId
from database import get_engine
from models import Vaga, Organizacao, Voluntario, Inscricao

router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"],
)

engine = get_engine()

@router.get("/{id_organizacao}/vagas_por_organizacao")
async def listar_vagas_por_organizacao(
    id_organizacao: str,
    limit: int = Query(10, alias="limit"),
    offset: int = Query(0, alias="offset"),
    engine: AIOEngine = Depends(get_engine) 
):
    try:
        organizacao_id = ObjectId(id_organizacao)
    except Exception as e:
        raise HTTPException(status_code=400, detail="ID da organização inválido")
    
    organizacao = await engine.find_one(Organizacao, Organizacao.id == organizacao_id)
    
    if not organizacao:
        raise HTTPException(status_code=404, detail="Organização não encontrada")
    
    vagas = await engine.find(Vaga, Vaga.organizacao_id == organizacao_id, skip=offset, limit=limit)

    return {"organizacao": organizacao, "vagas": vagas }

@router.get("/voluntarios_por_organizacao")
async def listar_voluntarios_por_organizacao(
    id_organizacao: str,
    limit: int = Query(10, alias="limit"),
    offset: int = Query(0, alias="offset"),
    engine: AIOEngine = Depends(get_engine)  
):
    try:
        organizacao_id = ObjectId(id_organizacao)  
    except Exception:
        raise HTTPException(status_code=400, detail="ID da organização inválido")
    
    organizacao = await engine.find_one(Organizacao, Organizacao.id == organizacao_id)
    
    if not organizacao:
        raise HTTPException(status_code=404, detail="Organização não encontrada")
    
    voluntarios = await engine.find(Voluntario, Voluntario.organizacao_id.in_([organizacao_id]), skip=offset, limit=limit)
    
    return {"organizacao": organizacao, "voluntarios": voluntarios }

@router.get("/total_voluntarios_por_organizacao")
async def total_voluntarios_por_organizacao(
    id_organizacao: str,
    limit: int = Query(10, alias="limit"),
    offset: int = Query(0, alias="offset"),
    engine: AIOEngine = Depends(get_engine)
):
    try:
        organizacao_id = ObjectId(id_organizacao)  
    except Exception:
        raise HTTPException(status_code=400, detail="ID da organização inválido")
    
    pipeline = [{ "$match": { "organizacao_id": organizacao_id}},{"$count": "total_voluntarios"},
                {"$skip": offset},{"$limit": limit}
    ]
    resultado = await engine.client.engajamais["voluntario"].aggregate(pipeline).to_list(length=None)
    
    if not resultado:
        raise HTTPException(status_code=404, detail="Nenhum voluntário encontrado para essa organização")

    return {"total_voluntarios_por_organizacao": resultado}
    

