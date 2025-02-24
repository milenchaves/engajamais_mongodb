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

@router.get("/vagas_por_organizacao")
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
    
    vagas = await engine.find(Vaga, Vaga.organizacao == organizacao_id, skip=offset, limit=limit)

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

@router.get("/vagas_por_localizacao")
async def listar_vagas_por_localizacao(
    localizacao: str = Query(..., description="Localização da organização"),
    limit: int = Query(10, alias="limit"),
    offset: int = Query(0, alias="offset"),
    engine: AIOEngine = Depends(get_engine)
):
    organizacoes = await engine.find(
        Organizacao,
        {"localizacao": {"$regex": localizacao, "$options": "i"}}, skip=offset,limit=limit)
    
    if not organizacoes:
        raise HTTPException(status_code=404, detail="Nenhuma organização encontrada para essa localização.")

    resultado = []
    for org in organizacoes:
        vagas = await engine.find(Vaga, Vaga.organizacao == org.id)
        for vaga in vagas:
            resultado.append({
                "vaga": vaga,
                "organizacao": org
            })
            
    return {"vagas": resultado}

@router.get("/organizacoes_ordenadas")
async def listar_organizacoes_ordenadas(
    ordem: str = Query(..., description="Ordem de classificação (asc ou desc)"),
    limit: int = Query(10, alias="limit"),
    offset: int = Query(0, alias="offset"),
    engine: AIOEngine = Depends(get_engine)
):
    if ordem.lower() == "asc":
        sort_order = 1 
    elif ordem.lower() == "desc":
        sort_order = -1  
    else:
        raise HTTPException(status_code=400, detail="Ordem inválida. Use 'asc' ou 'desc'.")

    organizacoes = await engine.client.engajamais["organizacao"].find({}, skip=offset, limit=limit  
    ).sort("nome_organizacao", sort_order).to_list(length=None)
    
    if not organizacoes:
        raise HTTPException(status_code=404, detail="Nenhuma organização encontrada.")

    for org in organizacoes:
        org["_id"] = str(org["_id"])

    return {"organizacoes": organizacoes}



