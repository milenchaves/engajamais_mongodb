from odmantic import Model, Reference
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Voluntario(Model):
    nome: str
    email: str
    area_interesse: str
    organizacao_id: Optional[list[ObjectId]] = []
    
class Organizacao(Model):
    nome_organizacao: str
    localizacao: str
    causa_apoiada: str
    
class Vaga(Model):
    titulo_vaga: str
    descricao_vaga: str
    data_publicacao: datetime
    status_vaga: str
    organizacao: Organizacao = Reference()
    
class Inscricao(Model):
    status: str
    vaga: Vaga = Reference()
    voluntario: Voluntario = Reference()