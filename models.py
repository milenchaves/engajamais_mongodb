from odmantic import Model, Reference
from datetime import datetime
from bson import ObjectId

class Voluntario(Model):
    nome: str
    email: str
    area_interesse: str
    
class Organizacao(Model):
    nome_organizacao: str
    localizacao: str
    causa_apoiada: str
    
class Vaga(Model):
    titulo_vaga: str
    descricao_vaga: str
    data_publicacao: datetime
    status_vaga: str
    organizacao_id: list[ObjectId]
    
class Inscricao(Model):
    status: str
    vaga_id: list[ObjectId]
    voluntario: list[ObjectId]