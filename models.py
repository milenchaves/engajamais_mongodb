from odmantic import Model, Reference, Field
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
    organizacao_id: ObjectId
    
class Inscricao(Model):
    status: str
    vaga_id: ObjectId
    voluntario_id: ObjectId